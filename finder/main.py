from asyncio import as_completed

import aiohttp
from aiohttp import web
from aiohttp.web_request import Request

from finder.app import app
from finder.resolver import generate_check_chunks, count_subdomains


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                data = msg.json()
                check_chunks = generate_check_chunks(data['host'], data.get('deep', 1))
                await ws.send_json({'action': 'check_start', 'data': {'count': count_subdomains(data.get('deep', 1))}})
                for chunk_num, chunk in enumerate(check_chunks, 1):
                    for check_num, check in enumerate(as_completed(chunk)):
                        host = await check
                        if host:
                            await ws.send_json({'action': 'new_host', 'data': {'host': host}})
                    await ws.send_json({'action': 'progress', 'data': {'count': chunk_num*1000}})
                await ws.send_json({'action': 'check_over', 'data': None})
                await ws.close()
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws

app.add_routes([web.get('/ws', websocket_handler)])
web.run_app(app, port=10001)

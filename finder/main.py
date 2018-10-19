from asyncio import as_completed

import aiohttp
from aiohttp import web
from aiohttp.web_request import Request

from finder.app import app
from finder.resolver import generate_check_set


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                async_checks = generate_check_set(msg.data, 1)
                full_count = len(async_checks)
                await ws.send_json({'action': 'check_start', 'data': {'count': full_count}})
                for i, check in enumerate(as_completed(async_checks)):
                    host = await check
                    if host:
                        await ws.send_json({'action': 'new_host', 'data': {'host': host}})
                    if i % 100 == 0:
                        await ws.send_json({'action': 'progress', 'data': {'num': i/full_count}})
                await ws.send_json({'action': 'check_over', 'data': None})
                await ws.close()
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws

app.add_routes([web.get('/ws', websocket_handler)])
web.run_app(app, port=10001)

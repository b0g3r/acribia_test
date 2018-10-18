from asyncio import as_completed

import aiohttp
from aiohttp import web
from aiohttp.web_request import Request

from finder.app import app
from finder.resolver import generate_check_set


async def get_handler(request: Request):
    host = request.match_info['host']
    hosts = []
    for check in as_completed(generate_check_set(host, 1)):
        result = await check
        if result:
            hosts.append(result)
    return web.Response(text='\n'.join(hosts))


async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                for check in as_completed(generate_check_set(msg.data, 1)):
                    result = await check
                    if result:
                        await ws.send_str(result)

        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws

app.add_routes([web.get('/get/{host}', get_handler)])
app.add_routes([web.get('/ws', websocket_handler)])
web.run_app(app, port=10001)

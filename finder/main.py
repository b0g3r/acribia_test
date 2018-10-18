from asyncio import as_completed

from aiohttp import web

from finder.app import app
from finder.resolver import generate_check_set


async def hello(request):
    hosts = []
    for check in as_completed(generate_check_set('google.com', 1)):
        result = await check
        if result:
            hosts.append(result)
    return web.Response(text='\n'.join(hosts))

app.add_routes([web.get('/', hello)])
web.run_app(app, port=10001)

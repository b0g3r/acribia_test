import aiodns
from aiohttp import web

app = web.Application(debug=True)
resolver = aiodns.DNSResolver(loop=app.loop)
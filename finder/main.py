from asyncio import as_completed

import aiodns
from aiohttp import web

from finder.subdomains import subdomains

app = web.Application()
resolver = aiodns.DNSResolver(loop=app.loop)


async def async_check(host: str, sub_domain: str):
    query = f'{sub_domain}.{host}'
    try:
        await resolver.query(query, 'A')
    except (aiodns.error.DNSError, UnicodeError):
        return None
    return query


async def hello(request):
    result = ""
    tasks = [async_check('google.com', subdomain) for subdomain in subdomains]
    for task in as_completed(tasks):
        a = await task
        if a:
            result+=a+'\n'
    return web.Response(text=result)

app.add_routes([web.get('/', hello)])
web.run_app(app, port=10001)

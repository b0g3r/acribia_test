import itertools
from typing import List, Optional, Awaitable

import aiodns

from finder.app import resolver
from finder.subdomains import subdomains


async def async_check(domain: str) -> Optional[str]:
    try:
        await resolver.query(domain, 'A')
    except (aiodns.error.DNSError, UnicodeError):
        return None
    return domain


def generate_check_set(host: str, deep: int = 2) -> List[Awaitable[Optional[str]]]:
    return [
        async_check(f"{'.'.join(r)}.{host}")
        for r in itertools.product(subdomains, repeat=deep)
    ]
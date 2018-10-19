import itertools
from typing import Optional, Awaitable, Iterable, List

import aiodns

from finder.app import resolver
from finder.subdomains import most_popular_subdomains

CHUNK_LEN = 1000


async def check_domain(domain: str) -> Optional[str]:
    try:
        await resolver.query(domain, 'A')
    except (aiodns.error.DNSError, UnicodeError):
        return None
    return domain


def count_subdomains(deep: int) -> int:
    return sum([len(most_popular_subdomains)**i for i in range(1, deep+1)])


def generate_check_chunks(host: str, deep: int = 1) -> Iterable[Awaitable[Optional[str]]]:
    """
    Генерирует чанки по 1000 проверок, которые удобно обрабатывать через `as_completed`
    """
    for repeat_num in range(1, deep+1):
        subdomains_combo = itertools.product(most_popular_subdomains, repeat=repeat_num)
        full_count = len(most_popular_subdomains) ** repeat_num
        # TODO: использовать что-нибудь адекватное, не писать свой чанкователь, fancy?
        for chunk_i in range(full_count // CHUNK_LEN):
            chunk = []
            for _ in range(chunk_i * CHUNK_LEN, min((chunk_i + 1) * CHUNK_LEN, full_count)):
                s = '.'.join(next(subdomains_combo))
                chunk.append(check_domain(f"{s}.{host}"))
            yield chunk

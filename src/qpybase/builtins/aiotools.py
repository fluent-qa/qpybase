"""
Asyncio equivalents to regular Python functions.

"""
from typing import AsyncIterator
from typing import Optional

import asyncio
import itertools


async def acount(
    start: float = 0,
    step: float = 1,
    delay: float = 0,
    stop: Optional[float] = None,
) -> AsyncIterator[float]:
    """Asyncio version of itertools.count()"""
    for item in itertools.count(start, step):  # pragma: no branch
        if stop is not None and item >= stop:
            break

        yield item
        await asyncio.sleep(delay)

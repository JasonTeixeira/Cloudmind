from __future__ import annotations

from typing import Any, Callable, Iterable, List, Optional, Tuple, TypeVar

T = TypeVar("T")


def paginate(
    fetch_page: Callable[[Optional[str]], Tuple[List[T], Optional[str]]],
    *,
    max_pages: int = 100,
) -> List[T]:
    items: List[T] = []
    token: Optional[str] = None
    pages = 0
    while pages < max_pages:
        page_items, token = fetch_page(token)
        items.extend(page_items)
        pages += 1
        if not token:
            break
    return items



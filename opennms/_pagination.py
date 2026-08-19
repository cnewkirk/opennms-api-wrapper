"""Pagination helper mixin."""
from typing import Any, Callable, Generator


class PaginationMixin:
    def paginate(
        self,
        method: Callable,
        key: str,
        page_size: int = 100,
        **kwargs: Any,
    ) -> Generator[Any, None, None]:
        """Yield every item from a paginated list endpoint.

        Handles ``limit``/``offset`` pagination transparently, stopping
        when ``totalCount`` is reached or a partial page is returned.

        Args:
            method: A bound client method that accepts ``limit`` and
                ``offset`` keyword arguments and returns a dict containing
                a list under *key* (e.g. ``client.get_alarms``).
            key: The response dict key that holds the list of items
                (e.g. ``"alarm"`` for alarms, ``"node"`` for nodes).
            page_size: Items to request per page. Defaults to ``100``.
            **kwargs: Additional keyword arguments forwarded to *method*
                on every call (e.g. ``severity="MAJOR"``).

        Yields:
            Individual items from each page, in order.

        Example:
            Fetch every critical alarm without writing a pagination loop::

                for alarm in client.paginate(
                    client.get_alarms, "alarm", severity="CRITICAL"
                ):
                    print(alarm["id"], alarm["nodeLabel"])
        """
        offset = 0
        while True:
            page = method(limit=page_size, offset=offset, **kwargs)
            items = page.get(key, [])
            yield from items
            offset += len(items)
            total = page.get("totalCount")
            if total is not None and offset >= total:
                break
            if len(items) < page_size:
                break

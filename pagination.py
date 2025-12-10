"""
Pagination Utility for Manajet
Simple pagination for list views
"""

from typing import List, Any, Dict
from math import ceil


class Pagination:
    """Simple pagination helper"""

    def __init__(self, items: List[Any], page: int = 1, per_page: int = 20):
        """
        Initialize pagination

        Args:
            items: List of items to paginate
            page: Current page number (1-indexed)
            per_page: Items per page
        """
        self.items = items
        self.page = max(1, page)  # Ensure page is at least 1
        self.per_page = per_page
        self.total = len(items)
        self.pages = ceil(self.total / per_page) if per_page > 0 else 1

        # Calculate slice indices
        start = (self.page - 1) * per_page
        end = start + per_page

        self.items_on_page = items[start:end]
        self.has_prev = self.page > 1
        self.has_next = self.page < self.pages
        self.prev_num = self.page - 1 if self.has_prev else None
        self.next_num = self.page + 1 if self.has_next else None

    def iter_pages(self, left_edge=2, left_current=2, right_current=3, right_edge=2):
        """
        Generate page numbers for pagination display

        Args:
            left_edge: Pages to show at the start
            left_current: Pages to show before current
            right_current: Pages to show after current
            right_edge: Pages to show at the end

        Yields:
            Page numbers or None (for ellipsis)
        """
        last = 0
        for num in range(1, self.pages + 1):
            if (num <= left_edge or
                (num >= self.page - left_current and num <= self.page + right_current) or
                num > self.pages - right_edge):
                if last + 1 != num:
                    yield None  # Ellipsis
                yield num
                last = num

    def to_dict(self) -> Dict:
        """
        Convert pagination to dictionary for templates

        Returns:
            Dictionary with pagination info
        """
        return {
            'page': self.page,
            'per_page': self.per_page,
            'total': self.total,
            'pages': self.pages,
            'has_prev': self.has_prev,
            'has_next': self.has_next,
            'prev_num': self.prev_num,
            'next_num': self.next_num,
            'items': self.items_on_page
        }


def paginate(items: List[Any], page: int = 1, per_page: int = 20) -> Pagination:
    """
    Convenience function to paginate a list

    Args:
        items: List to paginate
        page: Page number (1-indexed)
        per_page: Items per page

    Returns:
        Pagination object
    """
    return Pagination(items, page, per_page)

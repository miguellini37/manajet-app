"""
Unit tests for date_utils module
Run with: pytest test_date_utils.py -v
"""

import pytest
from datetime import datetime, timedelta
from date_utils import (
    parse_datetime, format_datetime, is_past, is_future,
    is_between, days_until, hours_until
)


class TestParseDatetime:
    def test_parse_iso_format(self):
        result = parse_datetime("2025-12-31 23:59:00")
        assert result is not None
        assert result.year == 2025
        assert result.month == 12
        assert result.day == 31

    def test_parse_date_only(self):
        result = parse_datetime("2025-06-15")
        assert result is not None
        assert result.year == 2025
        assert result.month == 6

    def test_parse_us_format(self):
        result = parse_datetime("12/31/2025")
        assert result is not None
        assert result.month == 12
        assert result.day == 31

    def test_parse_invalid(self):
        result = parse_datetime("not a date")
        assert result is None

    def test_parse_empty(self):
        result = parse_datetime("")
        assert result is None


class TestFormatDatetime:
    def test_format_with_time(self):
        dt = datetime(2025, 12, 31, 23, 59, 0)
        result = format_datetime(dt, include_time=True)
        assert result == "2025-12-31 23:59"

    def test_format_date_only(self):
        dt = datetime(2025, 12, 31, 23, 59, 0)
        result = format_datetime(dt, include_time=False)
        assert result == "2025-12-31"

    def test_format_none(self):
        result = format_datetime(None)
        assert result == ""


class TestIsPast:
    def test_past_date(self):
        past = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        assert is_past(past) is True

    def test_future_date(self):
        future = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        assert is_past(future) is False

    def test_invalid_date(self):
        assert is_past("not a date") is False


class TestIsFuture:
    def test_future_date(self):
        future = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        assert is_future(future) is True

    def test_past_date(self):
        past = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        assert is_future(past) is False


class TestIsBetween:
    def test_date_in_range(self):
        start = "2025-01-01"
        end = "2025-12-31"
        test = "2025-06-15"
        assert is_between(test, start, end) is True

    def test_date_before_range(self):
        start = "2025-01-01"
        end = "2025-12-31"
        test = "2024-12-31"
        assert is_between(test, start, end) is False

    def test_date_after_range(self):
        start = "2025-01-01"
        end = "2025-12-31"
        test = "2026-01-01"
        assert is_between(test, start, end) is False


class TestDaysUntil:
    def test_future_date(self):
        future = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        result = days_until(future)
        assert result == 4 or result == 5  # Allow for timing differences

    def test_past_date(self):
        past = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        result = days_until(past)
        assert result < 0

    def test_invalid_date(self):
        result = days_until("not a date")
        assert result is None


class TestHoursUntil:
    def test_future_datetime(self):
        future = (datetime.now() + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M')
        result = hours_until(future)
        assert result is not None
        assert 23 <= result <= 25  # Allow for timing differences

    def test_invalid_datetime(self):
        result = hours_until("not a datetime")
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

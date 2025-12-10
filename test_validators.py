"""
Unit tests for validators module
Run with: pytest test_validators.py -v
"""

import pytest
from validators import (
    validate_email, validate_phone, validate_passport, validate_name,
    validate_username, validate_password, validate_date, validate_integer,
    validate_tail_number, validate_license_number, validate_aircraft_capacity,
    validate_text_field, sanitize_string
)


class TestEmailValidation:
    def test_valid_email(self):
        valid, error = validate_email("user@example.com")
        assert valid is True
        assert error is None

    def test_invalid_email_no_at(self):
        valid, error = validate_email("userexample.com")
        assert valid is False
        assert "Invalid email format" in error

    def test_invalid_email_no_domain(self):
        valid, error = validate_email("user@")
        assert valid is False

    def test_empty_email(self):
        valid, error = validate_email("")
        assert valid is False
        assert "required" in error.lower()


class TestPhoneValidation:
    def test_valid_us_phone(self):
        valid, error = validate_phone("+1-555-123-4567")
        assert valid is True

    def test_valid_international(self):
        valid, error = validate_phone("+44-20-1234-5678")
        assert valid is True

    def test_too_short(self):
        valid, error = validate_phone("123")
        assert valid is False

    def test_invalid_characters(self):
        valid, error = validate_phone("555-ABCD")
        assert valid is False


class TestPassportValidation:
    def test_valid_passport(self):
        valid, error = validate_passport("AB123456")
        assert valid is True

    def test_too_short(self):
        valid, error = validate_passport("AB12")
        assert valid is False

    def test_invalid_characters(self):
        valid, error = validate_passport("AB-123456")
        assert valid is False


class TestNameValidation:
    def test_valid_name(self):
        valid, error = validate_name("John Smith")
        assert valid is True

    def test_too_short(self):
        valid, error = validate_name("J")
        assert valid is False

    def test_xss_attempt(self):
        valid, error = validate_name("<script>alert('xss')</script>")
        assert valid is False


class TestUsernameValidation:
    def test_valid_username(self):
        valid, error = validate_username("john_smith123")
        assert valid is True

    def test_too_short(self):
        valid, error = validate_username("ab")
        assert valid is False

    def test_invalid_characters(self):
        valid, error = validate_username("john-smith")
        assert valid is False


class TestPasswordValidation:
    def test_valid_password(self):
        valid, error = validate_password("password123")
        assert valid is True

    def test_too_short(self):
        valid, error = validate_password("pass1")
        assert valid is False

    def test_no_number(self):
        valid, error = validate_password("password")
        assert valid is False

    def test_no_letter(self):
        valid, error = validate_password("12345678")
        assert valid is False


class TestDateValidation:
    def test_valid_date(self):
        valid, error = validate_date("2025-12-31")
        assert valid is True

    def test_valid_datetime(self):
        valid, error = validate_date("2025-12-31 23:59")
        assert valid is True

    def test_invalid_format(self):
        valid, error = validate_date("31-12-2025")
        assert valid is False

    def test_unreasonable_year(self):
        valid, error = validate_date("1800-01-01")
        assert valid is False


class TestIntegerValidation:
    def test_valid_integer(self):
        valid, error = validate_integer("42")
        assert valid is True

    def test_with_min_max(self):
        valid, error = validate_integer("50", "Value", min_val=1, max_val=100)
        assert valid is True

    def test_too_low(self):
        valid, error = validate_integer("0", "Value", min_val=1)
        assert valid is False

    def test_too_high(self):
        valid, error = validate_integer("200", "Value", max_val=100)
        assert valid is False

    def test_not_integer(self):
        valid, error = validate_integer("abc")
        assert valid is False


class TestTailNumberValidation:
    def test_valid_us_tail(self):
        valid, error = validate_tail_number("N123AB")
        assert valid is True

    def test_valid_international(self):
        valid, error = validate_tail_number("G-ABCD")
        assert valid is True

    def test_invalid_us_format(self):
        valid, error = validate_tail_number("N123ABC")  # Too many letters
        assert valid is False


class TestAircraftCapacity:
    def test_valid_capacity(self):
        valid, error = validate_aircraft_capacity("150")
        assert valid is True

    def test_too_high(self):
        valid, error = validate_aircraft_capacity("1000")
        assert valid is False

    def test_zero(self):
        valid, error = validate_aircraft_capacity("0")
        assert valid is False


class TestSanitization:
    def test_removes_null_bytes(self):
        result = sanitize_string("hello\x00world")
        assert "\x00" not in result

    def test_strips_whitespace(self):
        result = sanitize_string("  hello  ")
        assert result == "hello"

    def test_truncates_long_text(self):
        long_text = "a" * 2000
        result = sanitize_string(long_text, max_length=100)
        assert len(result) == 100


class TestTextFieldValidation:
    def test_valid_text(self):
        valid, error = validate_text_field("This is valid text", "Description")
        assert valid is True

    def test_xss_detection(self):
        valid, error = validate_text_field("<script>alert('xss')</script>", "Field")
        assert valid is False

    def test_javascript_detection(self):
        valid, error = validate_text_field("javascript:alert('xss')", "Field")
        assert valid is False

    def test_optional_field_empty(self):
        valid, error = validate_text_field("", "Field", required=False)
        assert valid is True

    def test_required_field_empty(self):
        valid, error = validate_text_field("", "Field", required=True)
        assert valid is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

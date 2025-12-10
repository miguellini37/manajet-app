# Testing Guide for Manajet

## Running Tests

This project uses `pytest` for unit testing.

### Install Test Dependencies

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest test_validators.py -v
pytest test_date_utils.py -v
```

### Run with Coverage

```bash
pytest --cov=. --cov-report=html
```

This generates an HTML coverage report in `htmlcov/index.html`.

### Run Tests and Show Warnings

```bash
pytest -v -W all
```

## Test Structure

### Validator Tests (`test_validators.py`)

Tests for input validation functions:
- Email validation
- Phone number validation
- Passport number validation
- Name validation (XSS prevention)
- Username/password validation
- Date validation
- Integer validation
- Aircraft-specific validations

### Date Utility Tests (`test_date_utils.py`)

Tests for date/time parsing and manipulation:
- Date parsing from multiple formats
- Date formatting
- Past/future date checking
- Date range validation
- Days/hours until calculations

## Writing New Tests

### Test Class Structure

```python
class TestFeatureName:
    def test_valid_case(self):
        # Test the happy path
        result = function_to_test(valid_input)
        assert result == expected_output

    def test_invalid_case(self):
        # Test error handling
        result = function_to_test(invalid_input)
        assert result is None  # or appropriate error
```

### Assertions

Use descriptive assertions:
```python
# Good
assert valid is True
assert error is None

# Better with message
assert valid is True, f"Expected valid email but got: {error}"
```

### Test Data

Keep test data realistic and edge-case focused:
- Empty strings
- XSS attempts
- SQL injection attempts
- Boundary values
- Invalid formats

## Continuous Integration

For CI/CD, add this to your pipeline:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest --cov=. --cov-report=xml --cov-report=term

# Fail if coverage below 80%
pytest --cov=. --cov-fail-under=80
```

## Test Coverage Goals

Target coverage by module:
- `validators.py`: > 95%
- `date_utils.py`: > 90%
- `web_app.py`: > 70% (focus on business logic)
- `jet_manager.py`: > 80%

## Common Test Patterns

### Testing Validation Functions

```python
def test_validation():
    valid, error = validate_function(input)
    assert valid is True/False
    if not valid:
        assert "expected error message" in error.lower()
```

### Testing Date Functions

```python
from datetime import datetime, timedelta

def test_date_function():
    future = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    result = date_function(future)
    assert result is not None
```

### Testing Sanitization

```python
def test_sanitization():
    malicious = "<script>alert('xss')</script>"
    result = sanitize_function(malicious)
    assert "<script>" not in result
```

## Debugging Tests

### Run Single Test

```bash
pytest test_file.py::TestClass::test_method -v
```

### Show Print Statements

```bash
pytest -s
```

### Stop at First Failure

```bash
pytest -x
```

### Enter Debugger on Failure

```bash
pytest --pdb
```

## Best Practices

1. **Test one thing per test** - Each test should verify one specific behavior
2. **Use descriptive names** - Test names should describe what they test
3. **Keep tests independent** - Tests shouldn't depend on each other
4. **Test edge cases** - Empty strings, nulls, very large/small values
5. **Test error conditions** - Ensure errors are handled properly
6. **Mock external dependencies** - Don't rely on external services
7. **Keep tests fast** - Unit tests should run in milliseconds

## Example: Adding a New Test

Let's say you add a new validation function in `validators.py`:

```python
def validate_aircraft_model(model: str) -> Tuple[bool, Optional[str]]:
    if not model:
        return False, "Aircraft model is required"
    if len(model) < 3:
        return False, "Model name too short"
    return True, None
```

Add tests in `test_validators.py`:

```python
class TestAircraftModelValidation:
    def test_valid_model(self):
        valid, error = validate_aircraft_model("Gulfstream G650")
        assert valid is True
        assert error is None

    def test_empty_model(self):
        valid, error = validate_aircraft_model("")
        assert valid is False
        assert "required" in error.lower()

    def test_too_short(self):
        valid, error = validate_aircraft_model("G6")
        assert valid is False
        assert "too short" in error.lower()
```

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [Python testing best practices](https://docs.python-guide.org/writing/tests/)
- [Coverage.py documentation](https://coverage.readthedocs.io/)

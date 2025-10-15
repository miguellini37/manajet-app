# Bug Fix: Dashboard Date Parsing Issue

## Problem
Flights scheduled for tomorrow (or within the next 7 days) were not appearing in the dashboard's "Upcoming Flights" section.

## Root Cause
The date parsing function in `web_app.py` was using `split()[0]` to extract the date portion from datetime strings. This approach only works with space-separated formats like `"2025-10-16 12:15"` but fails with ISO 8601 format using T separator like `"2025-10-16T12:15"`.

When the datetime string uses the T separator:
- `"2025-10-16T12:15".split()[0]` returns `"2025-10-16T12:15"` (unchanged - no spaces to split on)
- `datetime.strptime("2025-10-16T12:15", '%Y-%m-%d')` then fails because the time portion is still present

## Solution
Modified the `parse_date()` helper function to handle both datetime formats by replacing 'T' with a space before splitting:

### Before (lines 171-176):
```python
def parse_date(date_str):
    try:
        return datetime.strptime(date_str.split()[0], '%Y-%m-%d')
    except:
        return None
```

### After:
```python
def parse_date(date_str):
    try:
        # Handle both 'YYYY-MM-DD HH:MM' and 'YYYY-MM-DDThh:mm' formats
        date_part = date_str.replace('T', ' ').split()[0]
        return datetime.strptime(date_part, '%Y-%m-%d')
    except:
        return None
```

## Additional Improvement
Also normalized the `today` variable to midnight (removing time components) to ensure consistent date comparisons:

### Before (line 166):
```python
today = datetime.now()
```

### After:
```python
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
```

## Testing
Verified the fix works correctly:
- Flight FL001 scheduled for 2025-10-16T12:15 (tomorrow) now correctly appears in "Upcoming Flights"
- The flight is properly filtered as Status='Scheduled' and within the next 7 days

## Files Modified
- [web_app.py](web_app.py) lines 166 and 171-176

## Impact
- ✅ Flights with ISO 8601 datetime format (YYYY-MM-DDThh:mm) now display correctly
- ✅ Backward compatible with space-separated format (YYYY-MM-DD HH:MM)
- ✅ All dashboard activity sections benefit from the fix:
  - Flights This Week
  - Upcoming Flights (Next 7 Days)
  - Maintenance This Week
  - Recently Completed Flights

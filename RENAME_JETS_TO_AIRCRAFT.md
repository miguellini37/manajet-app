# Rename "Jets" to "Aircraft" - Complete

## Summary
Renamed all user-facing references from "Jets" to "Aircraft" throughout the application for more professional terminology.

## Changes Made

### 1. Navigation Menu ([templates/base.html](templates/base.html#L497))
**Before**: `<li><a href="{{ url_for('jets') }}">Jets</a></li>`
**After**: `<li><a href="{{ url_for('jets') }}">Aircraft</a></li>`

### 2. Dashboard Template ([templates/dashboard.html](templates/dashboard.html))

#### Stats Cards (Lines 12, 23, 39)
- **Line 12**: "Total Jets" → "Total Aircraft"
- **Line 23**: "jets in flight" → "aircraft in flight"
- **Line 39**: "Jets under maintenance" → "Aircraft under maintenance"

#### Table Headers
- **Line 58**: Active Flights table - "Jet" → "Aircraft"
- **Line 153**: Active Maintenance table - "Jet" → "Aircraft"
- **Line 184**: Maintenance This Week table - "Jet" → "Aircraft"

#### Quick Actions Button (Line 269)
- **Line 269**: "View All Jets" → "View All Aircraft"

### 3. Customer Management Templates

#### customers.html ([templates/customers.html](templates/customers.html))
- **Line 23**: Table header "Jets" → "Aircraft"
- **Line 38**: Badge text "jets" → "aircraft"

#### customer_detail.html ([templates/customer_detail.html](templates/customer_detail.html))
- **Line 59**: Stat card "Total Jets" → "Total Aircraft"
- **Line 69**: Summary "Jets" → "Aircraft"
- **Line 77**: Section heading "Associated Aircraft" (already correct)
- **Line 83**: Table header "Jet ID" → "Aircraft ID"
- **Line 101**: Confirmation message "this jet" → "this aircraft"
- **Line 112**: Empty state "No jets" → "No aircraft"
- **Line 117**: Form heading "Assign New Jet" → "Assign New Aircraft"
- **Line 120**: Label "Select Jet to Assign" → "Select Aircraft to Assign"
- **Line 122**: Dropdown placeholder "-- Choose Jet --" → "-- Choose Aircraft --"
- **Line 128**: Button "Assign Jet" → "Assign Aircraft"

## Passenger Unassign Button Issue

The user reported not seeing the unassign button for passengers. Investigation shows:

**Status**: ✅ Button exists in template and is correctly implemented

**Location**: [templates/customer_detail.html](templates/customer_detail.html#L159-L163)

```html
<form method="POST" action="{{ url_for('unassign_passenger_from_customer', customer_id=customer.customer_id, passenger_id=passenger.passenger_id) }}" style="display: inline;">
    <button type="submit" class="btn btn-small btn-warning" onclick="return confirm('Remove {{ passenger.name }} from {{ customer.name }}?');">
        Unassign
    </button>
</form>
```

**Verification**:
- Button code exists on line 160
- CSS class `.btn-warning` is defined (lines 226-231)
- Same structure as aircraft unassign button (line 101)
- Both buttons use identical styling

**Possible reasons if still not visible**:
1. No passengers assigned to customer (shows empty state instead)
2. Browser cache needs refresh (Ctrl+F5)
3. User viewing as non-admin (requires admin role)

## Backend Notes

**Important**: While user-facing text now says "Aircraft", the backend code still uses variable names like:
- `jets` (route: `/jets`)
- `customer_jets` (variable name)
- `jet_id` (parameter name)
- `manager.jets` (data structure)

This is **intentional** to maintain backward compatibility and avoid breaking:
- Database schemas
- API endpoints
- Route URLs
- Variable names in Python code

## Testing Checklist

- ✅ Navigation menu shows "Aircraft" instead of "Jets"
- ✅ Dashboard stat cards use "Aircraft" terminology
- ✅ Dashboard tables use "Aircraft" column headers
- ✅ Customer list shows "Aircraft" counts
- ✅ Customer detail page uses "Aircraft" throughout
- ✅ All forms and buttons updated
- ✅ Passenger unassign button verified present in code

## Files Modified

1. [templates/base.html](templates/base.html) - Navigation menu (1 change)
2. [templates/dashboard.html](templates/dashboard.html) - Stats, tables, buttons (7 changes)
3. [templates/customers.html](templates/customers.html) - Table header and badge (2 changes)
4. [templates/customer_detail.html](templates/customer_detail.html) - Stats, forms, labels (9 changes)

**Total changes**: 19 user-facing text updates across 4 templates

## Screenshots of Changes (Text Examples)

### Before → After

| Location | Before | After |
|----------|--------|-------|
| Nav Menu | Jets | Aircraft |
| Dashboard Stats | Total Jets | Total Aircraft |
| Dashboard Stats | 2 jets in flight | 2 aircraft in flight |
| Dashboard Stats | Jets under maintenance | Aircraft under maintenance |
| Dashboard Table | Jet | Aircraft |
| Customer List | 2 jets | 2 aircraft |
| Customer Detail | Total Jets | Total Aircraft |
| Customer Detail | Assign New Jet | Assign New Aircraft |
| Quick Actions | View All Jets | View All Aircraft |

## User Impact

✅ **Positive**: More professional terminology
✅ **No Breaking Changes**: All URLs and backend code unchanged
✅ **Immediate**: Changes visible on next page load
✅ **Consistent**: Updated across all admin and user views

---

**Completed**: All "Jets" references renamed to "Aircraft" in user-facing templates
**Date**: 2025-10-15

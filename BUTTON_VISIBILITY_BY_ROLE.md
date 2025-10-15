# Button Visibility by User Role - Complete Reference

## Overview
All templates updated to show only buttons and actions that users have permission to use. This prevents confusion and improves security by hiding unauthorized actions.

## Role-Based Button Visibility Matrix

### Dashboard Quick Actions

| Button | Admin | Customer | Crew | Mechanic |
|--------|-------|----------|------|----------|
| Add Passenger | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| Schedule Flight | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Schedule Maintenance | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| Manage Customers | ✅ Yes | ❌ No | ❌ No | ❌ No |
| View All Aircraft | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |

### Maintenance Pages

#### Maintenance List Page
| Button | Admin | Customer | Crew | Mechanic |
|--------|-------|----------|------|----------|
| Schedule Maintenance | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| Edit (per record) | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| Delete (per record) | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| View (per record) | ✅ Yes | ✅ Yes* | ✅ Yes | ✅ Yes |

*Customers can only view maintenance for their own aircraft

#### Maintenance Detail Page
| Element | Admin | Customer | Crew | Mechanic |
|---------|-------|----------|------|----------|
| Edit Maintenance Button | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| Delete Maintenance Button | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| Update Status Form | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |

### Passenger Pages

#### Passenger List Page
| Button | Admin | Customer | Crew | Mechanic |
|--------|-------|----------|------|----------|
| Add New Passenger | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| Edit (per record) | ✅ Yes | ✅ Yes* | ❌ No | ❌ No |
| Delete (per record) | ✅ Yes | ✅ Yes* | ❌ No | ❌ No |
| View (per record) | ✅ Yes | ✅ Yes* | ✅ Yes | ✅ Yes |

*Customers can only edit/delete their own passengers

### Customer Management Pages (Admin Only)

#### Customer List
| Button | Admin | Others |
|--------|-------|--------|
| Add New Customer | ✅ Yes | ❌ No Access |
| View Details | ✅ Yes | ❌ No Access |
| Edit | ✅ Yes | ❌ No Access |

#### Customer Detail
| Button | Admin | Others |
|--------|-------|--------|
| Edit Customer | ✅ Yes | ❌ No Access |
| Assign Aircraft | ✅ Yes | ❌ No Access |
| Unassign Aircraft | ✅ Yes | ❌ No Access |
| Assign Passenger | ✅ Yes | ❌ No Access |
| Unassign Passenger | ✅ Yes | ❌ No Access |

**Note:** Entire customer management section (`/customers`) is only accessible to admin users. Non-admin users are redirected to dashboard if they attempt to access.

### Navigation Menu

| Menu Item | Admin | Customer | Crew | Mechanic |
|-----------|-------|----------|------|----------|
| Dashboard | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Passengers | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Crew | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aircraft | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Flights | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Maintenance | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Customers** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| Logout | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |

## Implementation Details

### Template Updates

#### 1. Maintenance Templates

**templates/maintenance.html** (Lines 5-7, 26-33)
```html
{% if user.role in ['admin', 'crew', 'mechanic'] %}
<a href="{{ url_for('add_maintenance') }}" class="btn btn-primary">🔧 Schedule Maintenance</a>
{% endif %}

<!-- In table actions -->
{% if user.role in ['admin', 'crew', 'mechanic'] %}
<a href="{{ url_for('edit_maintenance', maintenance_id=maint.maintenance_id) }}" class="btn btn-success">Edit</a>
{% endif %}
{% if user.role in ['admin', 'mechanic'] %}
<form method="POST" action="{{ url_for('delete_maintenance', maintenance_id=maint.maintenance_id) }}">
    <button type="submit" class="btn btn-danger">Delete</button>
</form>
{% endif %}
```

**templates/maintenance_detail.html** (Lines 16-25, 28-47)
```html
{% if session.get('role') in ['admin', 'crew', 'mechanic'] %}
<div style="margin-top: 20px;">
    <a href="{{ url_for('edit_maintenance', maintenance_id=maintenance.maintenance_id) }}" class="btn btn-success">Edit Maintenance</a>
    {% if session.get('role') in ['admin', 'mechanic'] %}
    <form method="POST" action="{{ url_for('delete_maintenance', maintenance_id=maintenance.maintenance_id) }}">
        <button type="submit" class="btn btn-danger">Delete Maintenance</button>
    </form>
    {% endif %}
</div>
{% endif %}

{% if session.get('role') in ['admin', 'crew', 'mechanic'] %}
<div class="card" style="margin-top: 20px;">
    <h2>Update Status</h2>
    <!-- Status update form -->
</div>
{% endif %}
```

#### 2. Dashboard Template

**templates/dashboard.html** (Lines 262-271)
```html
{% if user.role in ['customer', 'admin'] %}
<a href="{{ url_for('add_passenger') }}" class="btn btn-primary">Add Passenger</a>
{% endif %}
<a href="{{ url_for('add_flight') }}" class="btn btn-success">Schedule Flight</a>
{% if user.role in ['admin', 'crew', 'mechanic'] %}
<a href="{{ url_for('add_maintenance') }}" class="btn btn-secondary">Schedule Maintenance</a>
{% endif %}
{% if user.role == 'admin' %}
<a href="{{ url_for('customers') }}" class="btn btn-primary">Manage Customers</a>
{% endif %}
```

#### 3. Passenger Templates

**templates/passengers.html** (Lines 5-7, 26-31)
```html
{% if session.get('role') in ['customer', 'admin'] %}
<a href="{{ url_for('add_passenger') }}" class="btn btn-primary">➕ Add New Passenger</a>
{% endif %}

<!-- In table actions -->
{% if session.get('role') in ['customer', 'admin'] %}
<a href="{{ url_for('edit_passenger', passenger_id=passenger.passenger_id) }}" class="btn btn-success">Edit</a>
<form method="POST" action="{{ url_for('delete_passenger', passenger_id=passenger.passenger_id) }}">
    <button type="submit" class="btn btn-danger">Delete</button>
</form>
{% endif %}
```

#### 4. Navigation Menu

**templates/base.html** (Lines 500-502)
```html
{% if session.get('role') == 'admin' %}
<li><a href="{{ url_for('customers') }}">Customers</a></li>
{% endif %}
```

### Backend Access Control

Button visibility is **complemented** by backend route protection using decorators:

```python
@app.route('/maintenance/add')
@role_required('admin', 'crew', 'mechanic')  # Backend enforcement
def add_maintenance():
    # Only allows admin, crew, mechanics
    pass

@app.route('/customers')
@role_required('admin')  # Backend enforcement
def customers():
    # Only allows admin
    pass
```

**Security Note:** Backend decorators are the **primary** security mechanism. Template visibility changes improve UX but don't replace server-side access control.

## User Experience by Role

### As Admin User
- Sees all buttons and actions
- Complete control over all features
- Can manage customers, maintenance, passengers, aircraft, flights

### As Customer User
- Can add/edit/delete own passengers
- Can schedule flights for own aircraft
- Can view maintenance for own aircraft (read-only)
- **Cannot** schedule or edit maintenance
- **Cannot** access customer management
- **Cannot** see "Schedule Maintenance" buttons

### As Crew User (Pilot)
- Can schedule and edit maintenance
- Can schedule flights
- Can view all passengers and aircraft
- **Cannot** add/edit/delete passengers
- **Cannot** delete maintenance (only edit)
- **Cannot** access customer management

### As Mechanic User
- Can schedule, edit, and delete maintenance
- Can schedule flights
- Can view all passengers and aircraft
- **Cannot** add/edit/delete passengers
- **Cannot** access customer management

## Testing Scenarios

### Test 1: Customer Login
1. Log in as `johnsmith / customer123`
2. Go to Dashboard
   - ✅ Should see: "Add Passenger", "Schedule Flight"
   - ❌ Should NOT see: "Schedule Maintenance", "Manage Customers"
3. Go to Maintenance
   - ✅ Should see maintenance for JET001, JET002 (their aircraft)
   - ❌ Should NOT see: "Schedule Maintenance" button
   - ❌ Should NOT see: "Edit" or "Delete" buttons

### Test 2: Crew (Pilot) Login
1. Log in as `pilot_mike / crew123`
2. Go to Dashboard
   - ❌ Should NOT see: "Add Passenger", "Manage Customers"
   - ✅ Should see: "Schedule Flight", "Schedule Maintenance"
3. Go to Maintenance
   - ✅ Should see: "Schedule Maintenance" button
   - ✅ Should see: "Edit" buttons on all records
   - ❌ Should NOT see: "Delete" buttons
4. Go to Passengers
   - ❌ Should NOT see: "Add New Passenger" button
   - ❌ Should NOT see: "Edit" or "Delete" buttons
   - ✅ Should see: "View" buttons

### Test 3: Mechanic Login
1. Log in as `mechanic_joe / mech123`
2. Go to Dashboard
   - ❌ Should NOT see: "Add Passenger", "Manage Customers"
   - ✅ Should see: "Schedule Flight", "Schedule Maintenance"
3. Go to Maintenance
   - ✅ Should see: "Schedule Maintenance" button
   - ✅ Should see: "Edit" and "Delete" buttons on all records
4. Go to Passengers
   - ❌ Should NOT see: "Add New Passenger" button
   - ❌ Should NOT see: "Edit" or "Delete" buttons

### Test 4: Admin Login
1. Log in as `admin / admin123`
2. Go to Dashboard
   - ✅ Should see ALL buttons: "Add Passenger", "Schedule Flight", "Schedule Maintenance", "Manage Customers"
3. Navigate to any page
   - ✅ Should see all available action buttons
4. Go to Customers (in nav menu)
   - ✅ Menu item visible
   - ✅ Can access customer management

## Files Modified

1. [templates/maintenance.html](templates/maintenance.html)
   - Lines 5-7: Hide "Schedule Maintenance" button for customers
   - Lines 26-33: Hide edit/delete buttons based on role

2. [templates/maintenance_detail.html](templates/maintenance_detail.html)
   - Lines 16-25: Hide edit/delete buttons for customers
   - Lines 28-47: Hide status update form for customers

3. [templates/dashboard.html](templates/dashboard.html)
   - Lines 262-271: Role-based quick actions visibility

4. [templates/passengers.html](templates/passengers.html)
   - Lines 5-7: Hide "Add New Passenger" for crew/mechanics
   - Lines 26-31: Hide edit/delete buttons for crew/mechanics

5. [templates/base.html](templates/base.html)
   - Lines 500-502: Show "Customers" menu item only for admin

## Benefits

### 1. Improved Security
- Users don't see buttons they can't use
- Reduces accidental unauthorized access attempts
- Clear visual indication of permissions

### 2. Better User Experience
- Cleaner interface (less clutter)
- No confusing "access denied" errors from clicking visible buttons
- Users understand their role capabilities immediately

### 3. Reduced Support Burden
- Users less likely to attempt unauthorized actions
- Fewer permission-related questions
- Self-documenting interface (what you see is what you can do)

### 4. Consistent with Backend
- Template visibility matches backend `@role_required` decorators
- Defense in depth (both frontend and backend protection)
- Easy to audit and maintain

## Future Enhancements (Optional)

1. **Tooltip Explanations**: Add tooltips explaining why certain buttons aren't visible
2. **Role Badge Display**: Show user's role prominently in header
3. **Permission Groups**: Create reusable permission groups (e.g., "maintenance_managers")
4. **Dynamic Permissions**: Load permissions from database instead of hardcoding
5. **Audit Log**: Track when users attempt to access unauthorized routes
6. **Context-Sensitive Help**: Show role-specific help based on available actions

---

**Completed**: 2025-10-15
**Status**: ✅ All templates updated with role-based button visibility

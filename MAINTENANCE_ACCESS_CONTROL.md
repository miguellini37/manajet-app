# Maintenance Access Control & Flight Scheduling Conflicts

## Overview
Implemented role-based access control for maintenance management and automatic conflict detection when scheduling flights on aircraft with active maintenance.

## Features Implemented

### 1. Maintenance Access Control

#### Who Can Create/Edit Maintenance
**Allowed Roles:**
- ✅ **Admin** - Full access to create, edit, delete maintenance
- ✅ **Crew (Pilots)** - Can create and edit maintenance records
- ✅ **Mechanics** - Can create and edit maintenance records

**Restricted Roles:**
- ❌ **Customers** - Can only VIEW maintenance for their aircraft (read-only)

#### Who Can View Maintenance
**All Users** can view maintenance records, but filtered by role:
- **Admin, Crew, Mechanics**: See all maintenance records
- **Customers**: See only maintenance for their own aircraft

### 2. Maintenance Route Permissions

| Route | Admin | Crew | Mechanic | Customer |
|-------|-------|------|----------|----------|
| `/maintenance` (List) | ✅ View All | ✅ View All | ✅ View All | 🔒 View Own Aircraft Only |
| `/maintenance/add` | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| `/maintenance/<id>` (View) | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes (own aircraft) |
| `/maintenance/<id>/edit` | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| `/maintenance/<id>/delete` | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| `/maintenance/<id>/update-status` | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |

### 3. Flight Scheduling Conflict Detection

#### Automatic Checks
When scheduling a new flight, the system automatically checks if the selected aircraft has:
- **Scheduled maintenance** (Status: "Scheduled")
- **Active maintenance** (Status: "In Progress")

#### Conflict Warning
If maintenance is detected, the system:
1. **Prevents flight creation** on first submission
2. **Shows warning message** with maintenance details
3. **Re-displays the form** with all entered data preserved
4. **Requires explicit override** to proceed

#### Warning Details Shown
- Maintenance Type (e.g., "Annual Inspection", "Engine Service")
- Scheduled Date
- Current Status
- Override confirmation required

### 4. Override Functionality

Users can override the maintenance conflict by:
1. Seeing the warning on first submission attempt
2. Reviewing the maintenance details
3. Re-submitting the form (which now includes hidden `override_maintenance` flag)
4. System creates the flight with override note in success message

**Override Message:**
```
Flight scheduled successfully with ID: FL001 (Maintenance override applied)
```

## Implementation Details

### Backend Changes (web_app.py)

#### 1. Maintenance List Route (Lines 631-646)
```python
@app.route('/maintenance')
@login_required
def maintenance():
    """List all maintenance records"""
    user = get_current_user()

    # Filter maintenance by user role
    if user.role == 'customer':
        # Customers see only maintenance for their aircraft
        customer_jets = [j.jet_id for j in manager.jets.values() if j.customer_id == user.related_id]
        maintenance_list = [m for m in manager.maintenance.values() if m.jet_id in customer_jets]
    else:
        # Admin, crew, mechanics see all maintenance
        maintenance_list = list(manager.maintenance.values())

    return render_template('maintenance.html', maintenance=maintenance_list, user=user)
```

#### 2. Add Maintenance Route (Lines 648-669)
```python
@app.route('/maintenance/add', methods=['GET', 'POST'])
@role_required('admin', 'crew', 'mechanic')  # ← Access control
def add_maintenance():
    """Schedule maintenance (admin, crew, mechanics only)"""
```

#### 3. Edit Maintenance Route (Lines 681-712)
```python
@app.route('/maintenance/<maintenance_id>/edit', methods=['GET', 'POST'])
@role_required('admin', 'crew', 'mechanic')  # ← Access control
def edit_maintenance(maintenance_id):
    """Edit an existing maintenance record (admin, crew, mechanics only)"""
```

#### 4. Delete Maintenance Route (Lines 714-723)
```python
@app.route('/maintenance/<maintenance_id>/delete', methods=['POST'])
@role_required('admin', 'mechanic')  # ← Only admin and mechanics can delete
def delete_maintenance(maintenance_id):
    """Delete a maintenance record (admin, mechanics only)"""
```

#### 5. Update Status Route (Lines 725-737)
```python
@app.route('/maintenance/<maintenance_id>/update-status', methods=['POST'])
@role_required('admin', 'crew', 'mechanic')  # ← Access control
def update_maintenance_status(maintenance_id):
    """Update maintenance status (admin, crew, mechanics only)"""
```

#### 6. Flight Add Route with Conflict Detection (Lines 513-587)
```python
@app.route('/flights/add', methods=['GET', 'POST'])
@login_required
def add_flight():
    """Schedule a new flight"""
    user = get_current_user()

    if request.method == 'POST':
        jet_id = request.form['jet_id']
        override_maintenance = request.form.get('override_maintenance') == 'true'

        # Check for maintenance conflicts
        active_maintenance = [m for m in manager.maintenance.values()
                            if m.jet_id == jet_id and m.status in ['Scheduled', 'In Progress']]

        if active_maintenance and not override_maintenance:
            # Show warning and ask for confirmation
            maintenance_details = active_maintenance[0]
            flash(f'WARNING: Aircraft has scheduled maintenance...', 'warning')

            # Re-render form with maintenance warning
            return render_template('flight_form.html',
                                 maintenance_warning=True,
                                 maintenance_details=maintenance_details,
                                 form_data=request.form)
```

### Frontend Changes (templates/flight_form.html)

#### 1. Maintenance Warning Banner (Lines 8-23)
```html
{% if maintenance_warning %}
<div class="card" style="background: #fff3cd; border-left: 4px solid #ff9800;">
    <h2 style="color: #856404;">⚠️ Maintenance Conflict Detected</h2>
    <p><strong>The selected aircraft has scheduled maintenance:</strong></p>
    <ul>
        <li><strong>Type:</strong> {{ maintenance_details.maintenance_type }}</li>
        <li><strong>Scheduled Date:</strong> {{ maintenance_details.scheduled_date }}</li>
        <li><strong>Status:</strong> {{ maintenance_details.status }}</li>
    </ul>
    <p style="color: #856404; font-weight: bold;">
        Scheduling this flight will override the maintenance schedule. Are you sure you want to proceed?
    </p>
</div>
{% endif %}
```

#### 2. Hidden Override Flag (Lines 27-29)
```html
{% if maintenance_warning %}
<input type="hidden" name="override_maintenance" value="true">
{% endif %}
```

#### 3. Form Data Preservation (Lines 34-68)
All form fields updated to preserve values when showing warning:
```html
<input type="text" name="departure"
       value="{{ form_data.get('departure') if form_data else (flight.departure if flight else '') }}">
```

## User Workflows

### Workflow 1: Customer Viewing Maintenance

1. Log in as customer (e.g., `johnsmith / customer123`)
2. Click "Maintenance" in navigation
3. See only maintenance for their aircraft (JET001, JET002)
4. Click on maintenance record to view details
5. ✅ Can view all details
6. ❌ No "Edit" or "Schedule Maintenance" buttons visible

### Workflow 2: Mechanic Creating Maintenance

1. Log in as mechanic (e.g., `mechanic_joe / mech123`)
2. Click "Maintenance" in navigation
3. Click "Schedule Maintenance" button
4. Fill in form:
   - Select aircraft
   - Choose maintenance type
   - Set scheduled date
   - Add description
5. Click "Schedule Maintenance"
6. ✅ Maintenance created successfully

### Workflow 3: Flight Scheduling with Maintenance Conflict

1. Log in as any authorized user
2. Click "Flights" → "Schedule Flight"
3. Select an aircraft that has scheduled maintenance
4. Fill in all flight details (departure, destination, dates, crew, passengers)
5. Click "Schedule Flight"
6. ⚠️ **Warning appears**:
   ```
   WARNING: Aircraft has scheduled maintenance (Annual Inspection)
   on 2025-10-20. Flight scheduling requires override.
   ```
7. Review the maintenance details shown in yellow warning box
8. **Decision Point:**
   - **Cancel**: Click "Cancel" button to return to flights list
   - **Override**: Click "Schedule Flight" again to confirm override
9. If override:
   - Flight scheduled successfully
   - Message: "Flight scheduled with ID: FL001 (Maintenance override applied)"

### Workflow 4: Pilot Creating Maintenance

1. Log in as pilot (e.g., `pilot_mike / crew123`)
2. Click "Maintenance" in navigation
3. Click "Schedule Maintenance"
4. ✅ Has access to create maintenance
5. Can also edit existing maintenance records

## Access Denied Scenarios

### Customer Tries to Create Maintenance
- Clicks "Maintenance" → sees only their aircraft maintenance
- **No "Schedule Maintenance" button** visible
- If trying to access `/maintenance/add` directly:
  - Redirected to dashboard
  - Flash message: "You do not have permission to access this page"

### Customer Tries to Edit Maintenance
- Views maintenance record
- **No "Edit" button** visible
- If trying to access `/maintenance/MAINT001/edit` directly:
  - Redirected to dashboard
  - Flash message: "You do not have permission to access this page"

### Crew Tries to Delete Maintenance
- Views maintenance record
- **No "Delete" button** visible (only admin and mechanics can delete)
- If trying to submit delete request:
  - Redirected to dashboard
  - Flash message: "You do not have permission to access this page"

## Testing Checklist

### Maintenance Access
- ✅ Admin can create/edit/delete maintenance
- ✅ Crew (pilots) can create/edit maintenance (but not delete)
- ✅ Mechanics can create/edit/delete maintenance
- ✅ Customers can view only their aircraft maintenance
- ✅ Customers cannot create/edit maintenance

### Flight Conflict Detection
- ✅ Scheduling flight on aircraft with scheduled maintenance shows warning
- ✅ Scheduling flight on aircraft with in-progress maintenance shows warning
- ✅ Warning displays maintenance type, date, and status
- ✅ Form data preserved when showing warning
- ✅ Override flag allows flight creation on second submission
- ✅ Success message indicates override was applied

### Form Preservation
- ✅ Aircraft selection preserved
- ✅ Departure/destination airports preserved
- ✅ Departure/arrival times preserved
- ✅ Selected passengers preserved
- ✅ Selected crew preserved

## Files Modified

1. [web_app.py](web_app.py)
   - Lines 631-646: Updated maintenance list route with filtering
   - Lines 648-669: Added role restriction to add_maintenance
   - Lines 681-712: Added role restriction to edit_maintenance
   - Lines 714-723: Added role restriction to delete_maintenance (admin/mechanic only)
   - Lines 725-737: Added role restriction to update_maintenance_status
   - Lines 513-587: Added conflict detection to add_flight route

2. [templates/flight_form.html](templates/flight_form.html)
   - Lines 8-23: Added maintenance warning banner
   - Lines 27-29: Added hidden override flag
   - Lines 34-68: Updated form fields to preserve data
   - Lines 96-103: Updated passengers multi-select with form_data
   - Lines 119-128: Updated crew multi-select with form_data

## Database/Data Structure

**No changes required** - Uses existing maintenance status values:
- "Scheduled"
- "In Progress"
- "Completed"
- "Cancelled"

## Security Notes

- Access control enforced at route level using `@role_required` decorator
- Customers cannot bypass restrictions via direct URL access
- Override requires form resubmission (prevents accidental overrides)
- All maintenance operations logged with user context
- No sensitive data exposed in warning messages

## Future Enhancements (Optional)

1. **Date Range Conflict Detection**: Check if flight dates overlap with maintenance dates
2. **Email Notifications**: Alert mechanics when flights override maintenance
3. **Maintenance History**: Track all overrides for audit purposes
4. **Bulk Operations**: Allow mechanics to reschedule multiple maintenance items
5. **Calendar View**: Visual calendar showing flights and maintenance conflicts
6. **Priority Levels**: Critical maintenance cannot be overridden

---

**Completed**: 2025-10-15
**Status**: ✅ All features implemented and tested

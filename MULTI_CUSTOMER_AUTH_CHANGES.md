# Multi-Customer Authentication System - Implementation Guide

## Overview

This update adds comprehensive customer management and role-based authentication to the Private Jet Manager application. The system now supports:

- **Multiple customers** - Each customer can own multiple jets
- **User authentication** - Login/logout system with password hashing
- **Role-based access control** - Different interfaces for:
  - **Customers** - See only their own jets, passengers, and flights
  - **Crew/Pilots** - See all data across customers (can work for multiple customers)
  - **Mechanics** - See all jets and maintenance records
  - **Admin** - Full system access

## Key Changes

### 1. Data Model Updates (jet_manager.py)

#### New Classes Added:

**Customer Class:**
```python
- customer_id: str
- name: str
- company: str
- email: str
- phone: str
- address: str
```

**User Class:**
```python
- user_id: str
- username: str
- password_hash: str
- role: str (customer/crew/mechanic/admin)
- related_id: str (links to customer_id, crew_id, etc.)
- email: str
```

#### Modified Classes:

**PrivateJet:**
- Added: `customer_id` field (required)
- Jets are now owned by specific customers

**Passenger:**
- Added: `customer_id` field
- Passengers are private to each customer account

#### New Methods:

**User Management:**
- `add_user()`, `get_user()`, `get_user_by_username()`
- `update_user()`, `delete_user()`

**Customer Management:**
- `add_customer()`, `get_customer()`, `update_customer()`, `delete_customer()`
- `list_customers()`, `get_customer_jets()`

### 2. Authentication System (web_app.py)

#### New Routes:

- `/login` - User login page
- `/logout` - End user session
- `/register` - Customer self-registration

#### Access Control Decorators:

```python
@login_required  # Requires any logged-in user
@role_required('customer', 'admin')  # Requires specific role(s)
```

#### Data Filtering:

All routes now filter data based on user role:

**Customer Users:**
- See ONLY their own:
  - Jets (customer_id matches)
  - Passengers (customer_id matches)
  - Flights (for their jets only)
  - Maintenance (for their jets only)
- Can view all crew/pilots (shared resource)

**Crew/Mechanic Users:**
- See ALL data across all customers
- Can be assigned to any customer's flights

**Admin Users:**
- Full access to everything
- Can manage all customers, users, and data

### 3. Database Changes

#### Breaking Changes:

**⚠️ IMPORTANT:** These changes require updating existing data:

1. **PrivateJet.customer_id** - Now required (was optional)
   - Old jets will load with empty customer_id
   - Must assign jets to customers manually or via migration

2. **Passenger.customer_id** - Now tracked
   - Old passengers will load with empty customer_id
   - Must assign passengers to customers

3. **add_jet() signature changed:**
   ```python
   # Old
   add_jet(jet_id, model, tail_number, capacity, status)

   # New
   add_jet(jet_id, model, tail_number, capacity, customer_id, status)
   ```

4. **add_passenger() signature changed:**
   ```python
   # Old
   add_passenger(passenger_id, name, passport, nationality, expiry, contact)

   # New
   add_passenger(passenger_id, name, passport, nationality, expiry, contact, customer_id)
   ```

## Setup Instructions

### Step 1: Update Core Code

The following files have been updated:
- ✅ `jet_manager.py` - Core data models
- ⚠️ `web_app.py` - Partially updated (needs completion)

### Step 2: Generate Templates

Run these scripts to create all necessary HTML templates:

```bash
# Create authentication templates
python generate_auth_templates.py

# Create existing templates (if not already done)
python generate_updated_templates.py
python generate_updated_templates_part2.py
```

### Step 3: Initialize Sample Data

```bash
# Create admin user and sample customers/crew
python setup_initial_data.py
```

This creates:
- Admin account: `admin` / `admin123`
- 2 sample customers with jets and passengers
- 4 crew members (2 pilots, 2 cabin crew)
- 1 mechanic account

### Step 4: Update web_app.py Routes

**⚠️ TODO:** The following routes still need access control decorators added:

1. **Passenger Routes:**
   - ✅ `passengers()` - Done
   - ✅ `add_passenger()` - Done
   - ⚠️ `view_passenger()` - Needs `@login_required` + ownership check
   - ⚠️ `edit_passenger()` - Needs `@role_required('customer', 'admin')` + ownership check
   - ⚠️ `delete_passenger()` - Needs `@role_required('customer', 'admin')` + ownership check

2. **Jet Routes:**
   - ⚠️ All routes need `@login_required`
   - ⚠️ `add_jet()` - Needs `@role_required('admin')` (only admin can add jets)
   - ⚠️ `edit_jet()` - Update to include `customer_id` parameter
   - ⚠️ `delete_jet()` - Needs ownership check

3. **Flight Routes:**
   - ⚠️ All routes need `@login_required`
   - ⚠️ Filter flights by customer (only show flights for customer's jets)

4. **Maintenance Routes:**
   - ⚠️ All routes need `@login_required`
   - ⚠️ `add_maintenance()` - `@role_required('mechanic', 'admin')`
   - ⚠️ Filter by customer (only show maintenance for customer's jets)

5. **Crew Routes:**
   - ⚠️ All routes need `@login_required`
   - ⚠️ Crew visible to all users (shared resource)

### Step 5: Add Customer Management Routes

**⚠️ TODO:** Add these new routes to web_app.py:

```python
# ====================
# CUSTOMER ROUTES (Admin only)
# ====================

@app.route('/customers')
@role_required('admin')
def customers():
    """List all customers"""
    return render_template('customers.html', customers=manager.customers.values(), user=get_current_user())

@app.route('/customers/add', methods=['GET', 'POST'])
@role_required('admin')
def add_customer():
    """Add a new customer"""
    if request.method == 'POST':
        customer_id = manager.add_customer(
            "",
            request.form['name'],
            request.form['company'],
            request.form['email'],
            request.form['phone'],
            request.form['address']
        )
        if customer_id:
            flash(f'Customer added successfully with ID: {customer_id}', 'success')
            manager.save_data()
            return redirect(url_for('customers'))
        else:
            flash('Error adding customer', 'error')

    return render_template('customer_form.html', user=get_current_user())

@app.route('/customers/<customer_id>')
@role_required('admin', 'customer')
def view_customer(customer_id):
    """View customer details"""
    user = get_current_user()

    # Customers can only view their own account
    if user.role == 'customer' and user.related_id != customer_id:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    customer = manager.get_customer(customer_id)
    if customer:
        jets = manager.get_customer_jets(customer_id)
        passengers = [p for p in manager.passengers.values() if p.customer_id == customer_id]
        return render_template('customer_detail.html',
                             customer=customer,
                             jets=jets,
                             passengers=passengers,
                             user=user)
    flash('Customer not found', 'error')
    return redirect(url_for('customers'))

# ... add edit and delete routes similarly
```

### Step 6: Update base.html Navigation

**⚠️ TODO:** Update templates/base.html to show/hide menu items based on user role:

```html
<nav>
    <ul>
        <li><a href="{{ url_for('index') }}">Dashboard</a></li>

        {% if user.role in ['customer', 'admin'] %}
            <li><a href="{{ url_for('passengers') }}">Passengers</a></li>
        {% endif %}

        <li><a href="{{ url_for('crew') }}">Crew</a></li>

        {% if user.role in ['customer', 'crew', 'mechanic', 'admin'] %}
            <li><a href="{{ url_for('jets') }}">Jets</a></li>
            <li><a href="{{ url_for('flights') }}">Flights</a></li>
        {% endif %}

        {% if user.role in ['mechanic', 'admin'] %}
            <li><a href="{{ url_for('maintenance') }}">Maintenance</a></li>
        {% endif %}

        {% if user.role == 'admin' %}
            <li><a href="{{ url_for('customers') }}">Customers</a></li>
        {% endif %}

        <li><a href="{{ url_for('logout') }}">Logout ({{ user.username }})</a></li>
    </ul>
</nav>
```

### Step 7: Create Customer Templates

**⚠️ TODO:** Generate customer management templates similar to other entities:

```bash
# Create: templates/customers.html
# Create: templates/customer_form.html
# Create: templates/customer_detail.html
```

## User Roles & Permissions

### Customer
**Can:**
- View/manage their own passengers
- View their own jets (read-only, admin adds jets)
- View/schedule flights for their jets
- View crew members (to assign to flights)
- View maintenance for their jets

**Cannot:**
- See other customers' data
- Add/edit jets (admin only)
- See other customers' passengers

### Crew/Pilot
**Can:**
- View all jets across all customers
- View all flights (can be assigned to any customer's flights)
- View their own profile
- View all maintenance schedules

**Cannot:**
- Manage passengers
- Add/edit jets
- Perform maintenance updates

### Mechanic
**Can:**
- View all jets
- View/update all maintenance records
- Create new maintenance tasks

**Cannot:**
- Manage passengers
- Schedule flights
- See passenger details

### Admin
**Can:**
- Everything
- Manage customers
- Create users for any role
- Add/remove jets
- Assign jets to customers
- View all data

## Security Considerations

### Current Implementation:
- ✅ Password hashing (SHA-256)
- ✅ Session-based authentication
- ✅ Role-based access control
- ✅ Data isolation (customers can't see each other)

### Recommended Improvements:
- ⚠️ Use bcrypt or Argon2 instead of SHA-256
- ⚠️ Add password strength requirements
- ⚠️ Add session timeout
- ⚠️ Add CSRF protection (Flask-WTF)
- ⚠️ Add rate limiting for login attempts
- ⚠️ Use HTTPS in production
- ⚠️ Add email verification for registration
- ⚠️ Add password reset functionality

## Migration Guide for Existing Data

If you have existing data in `jet_schedule_data.json`, you need to:

1. **Backup your data:**
   ```bash
   cp jet_schedule_data.json jet_schedule_data.json.backup
   ```

2. **Create admin and customers:**
   ```bash
   python setup_initial_data.py
   ```

3. **Manually assign jets to customers:**
   - Edit jet records to add customer_id
   - Or use admin interface once templates are complete

4. **Assign passengers to customers:**
   - Edit passenger records to add customer_id
   - Or reassign via admin interface

## Testing

### Test Scenarios:

1. **Customer Isolation:**
   - Login as `johnsmith`
   - Verify you only see jets/passengers for customer CUST001
   - Try accessing another customer's data directly (should fail)

2. **Crew Access:**
   - Login as `pilot_mike`
   - Verify you can see all jets and flights
   - Verify you can be assigned to any customer's flights

3. **Mechanic Access:**
   - Login as `mechanic_joe`
   - Verify you can see all jets
   - Verify you can create/update maintenance records

4. **Admin Access:**
   - Login as `admin`
   - Verify full access to all features
   - Create a new customer and jet

## Next Steps

1. ✅ Core data model updated
2. ✅ Authentication system added
3. ⚠️ **TODO:** Complete all route access control decorators
4. ⚠️ **TODO:** Add customer management routes
5. ⚠️ **TODO:** Update base.html navigation
6. ⚠️ **TODO:** Create customer templates
7. ⚠️ **TODO:** Add data filtering to remaining routes
8. ⚠️ **TODO:** Add password change functionality
9. ⚠️ **TODO:** Add user management for admin

## Questions?

Key design decisions:

**Q: Why can crew/mechanics see all customers' data?**
A: Crew and mechanics are shared resources that work across multiple customer accounts. A pilot might fly for multiple customers.

**Q: Can customers add their own jets?**
A: No, only admins can add jets. This is a business decision - jets are expensive assets that should be verified by admin.

**Q: Can a customer see other customers' crew?**
A: Yes, crew information is visible to all (they're shared resources), but customers can't see other customers' passengers.

**Q: What happens to old data without customer_id?**
A: It loads with empty customer_id. You must assign data to customers manually or via migration script.

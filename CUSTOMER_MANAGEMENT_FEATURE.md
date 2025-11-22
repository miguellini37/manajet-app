# Customer Management Feature - Admin Tools

## Overview
Added comprehensive customer management tools for admin users to manage customer accounts and associate aircraft and passengers to customer accounts.

## Features Implemented

### 1. Customer List View
**Route**: `/customers` (Admin only)
**Template**: `templates/customers.html`

Features:
- Display all customers in a table
- Show customer details (ID, name, company, email, phone)
- Display count of associated jets and passengers for each customer
- Quick actions: View Details, Edit
- "Add New Customer" button
- Mobile-responsive table layout

### 2. Customer Add/Edit Form
**Routes**:
- `/customers/add` (Admin only)
- `/customers/<customer_id>/edit` (Admin only)

**Template**: `templates/customer_form.html`

Features:
- Form fields: Full Name, Company Name, Email, Phone, Address
- Create new customer accounts
- Update existing customer information
- Delete customer (with confirmation dialog)
- Validation and error handling
- Mobile-responsive form layout

### 3. Customer Detail View with Asset Management
**Route**: `/customers/<customer_id>` (Admin only)
**Template**: `templates/customer_detail.html`

This is the main feature - a comprehensive dashboard for managing customer assets:

#### Customer Information Section
- Display all customer details
- Show associated user account (if exists)
- Edit and back navigation buttons

#### Summary Statistics Cards
- Total Jets assigned to customer
- Total Passengers assigned to customer
- Available unassigned jets and passengers

#### Associated Aircraft Management
**Features**:
- Table showing all jets assigned to this customer
  - Jet ID, Model, Tail Number, Capacity, Status
  - "Unassign" button to remove jet from customer
- Dropdown to assign new jets from unassigned pool
  - Shows only jets not currently assigned to any customer
  - One-click assignment with confirmation

#### Associated Passengers Management
**Features**:
- Table showing all passengers assigned to this customer
  - Passenger ID, Name, Passport Number, Nationality, Contact
  - "Unassign" button to remove passenger from customer
- Dropdown to assign new passengers from unassigned pool
  - Shows only passengers not currently assigned to any customer
  - One-click assignment with confirmation

### 4. Asset Assignment/Unassignment Routes
**Routes**:
- `/customers/<customer_id>/assign-jet` (POST, Admin only)
- `/customers/<customer_id>/unassign-jet/<jet_id>` (POST, Admin only)
- `/customers/<customer_id>/assign-passenger` (POST, Admin only)
- `/customers/<customer_id>/unassign-passenger/<passenger_id>` (POST, Admin only)

**Functionality**:
- Assign jets to customers by updating `jet.customer_id`
- Assign passengers to customers by updating `passenger.customer_id`
- Unassign by setting customer_id to empty string
- Automatic data persistence
- Flash messages for success/error feedback

### 5. Navigation Menu Update
**File**: `templates/base.html`

Added conditional "Customers" menu item:
- Only visible to admin users (`session.get('role') == 'admin'`)
- Positioned between "Maintenance" and "Logout"
- Mobile-responsive (included in hamburger menu)

## Implementation Details

### Backend Changes (web_app.py)
Lines 719-906: Added complete customer management section with:
- 9 new routes for customer CRUD and asset management
- Role-based access control using `@role_required('admin')` decorator
- Customer statistics calculation (jet/passenger counts)
- Filtering for unassigned jets and passengers
- User account lookup for customers

### Frontend Templates Created
1. **customers.html** - List view with stats
2. **customer_form.html** - Add/Edit form
3. **customer_detail.html** - Comprehensive detail view with asset management

### Design Features
- Consistent with existing Manajet design language
- Gradient stat cards matching dashboard design
- Mobile-responsive tables and forms
- Color-coded status badges
- Touch-friendly buttons (44px minimum on mobile)
- Confirmation dialogs for destructive actions
- Real-time feedback with flash messages

## Access Control
- All customer management routes require admin role
- Enforced at route level with `@role_required('admin')` decorator
- Menu item only visible to admin users
- Customer users can only see their own data (unchanged)
- Crew and mechanics see all data but cannot manage customers (unchanged)

## Data Model
Uses existing Customer class from jet_manager.py:
- `customer_id`: Unique identifier
- `name`: Full name
- `company`: Company name
- `email`: Email address
- `phone`: Phone number
- `address`: Physical address

Jets and Passengers have `customer_id` field for association.

## Testing Results
- ✅ All 9 customer routes successfully registered
- ✅ Templates created and properly structured
- ✅ Navigation menu updated with conditional rendering
- ✅ Existing data structure compatible (2 customers, 4 jets, 5 passengers)
- ✅ Asset associations working (3 jets and 3 passengers currently assigned)

## Usage Instructions

### As Admin User:
1. Log in as admin (username: admin, password: admin123)
2. Click "Customers" in the navigation menu
3. View list of all customers with jet/passenger counts
4. Click "View Details" to manage a customer's assets
5. Use dropdown menus to assign unassigned jets/passengers
6. Click "Unassign" buttons to remove associations
7. Click "Edit Customer" to update customer information
8. Use "Add New Customer" to create new customer accounts

### Asset Assignment Workflow:
1. Navigate to customer detail page
2. Scroll to "Associated Aircraft" or "Associated Passengers" section
3. Select asset from dropdown (shows only unassigned items)
4. Click "Assign Jet" or "Assign Passenger"
5. Asset immediately appears in customer's list
6. To unassign: click "Unassign" button next to asset

### Asset Unassignment Workflow:
1. Navigate to customer detail page
2. Find the jet or passenger in the respective table
3. Click "Unassign" button
4. Confirm the action in the dialog
5. Asset removed from customer and returns to unassigned pool

## Files Modified
- [web_app.py](web_app.py) - Lines 719-906: Customer management routes
- [templates/base.html](templates/base.html) - Lines 500-503: Navigation menu update

## Files Created
- [templates/customers.html](templates/customers.html) - Customer list view
- [templates/customer_form.html](templates/customer_form.html) - Add/Edit form
- [templates/customer_detail.html](templates/customer_detail.html) - Detail view with asset management
- [CUSTOMER_MANAGEMENT_FEATURE.md](CUSTOMER_MANAGEMENT_FEATURE.md) - This documentation

## Future Enhancements (Optional)
- Bulk asset assignment (select multiple jets/passengers at once)
- Customer activity log (show all flights for customer's jets)
- Customer billing/invoicing integration
- Export customer data to CSV/PDF
- Customer-specific reporting dashboard
- Email notifications for customer account changes
- API endpoints for customer management

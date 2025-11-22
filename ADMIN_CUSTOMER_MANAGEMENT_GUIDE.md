# Admin Customer Management Quick Guide

## Quick Start

### Accessing Customer Management
1. Log in as admin user
2. Look for "Customers" in the navigation menu (only visible to admins)
3. Click to view customer list

## Main Views

### 1. Customer List (`/customers`)
```
+--------------------------------------------------------------------+
| Customer Management                           [+ Add New Customer] |
+--------------------------------------------------------------------+
| Customer ID | Name        | Company      | Jets | Passengers | ... |
|-------------|-------------|--------------|------|------------|-----|
| CUST001     | John Smith  | Smith Ent.   |  2   |     2      | ... |
| CUST002     | Sarah J.    | Johnson LLC  |  1   |     1      | ... |
+--------------------------------------------------------------------+
```

**Actions Available**:
- View customer details (click "View Details")
- Edit customer info (click "Edit")
- Add new customer (click "+ Add New Customer")

### 2. Customer Detail (`/customers/<customer_id>`)

This is the main asset management screen:

```
+--------------------------------------------------------------------+
| Customer Details                        [Edit Customer] [Back]     |
+--------------------------------------------------------------------+
| Customer Information                                                |
| - Customer ID: CUST001                                             |
| - Name: John Smith                                                 |
| - Company: Smith Enterprises                                       |
| - Email: john@smithent.com                                         |
| - Phone: +1-555-0123                                               |
| - User Account: johnsmith (Active)                                 |
+--------------------------------------------------------------------+

+--------------------+--------------------+--------------------+
|   Total Jets: 2    | Total Passengers:2 | Available Unassign |
|                    |                    | 1 Jets, 2 Pass.    |
+--------------------+--------------------+--------------------+

+--------------------------------------------------------------------+
| Associated Aircraft                                                 |
+--------------------------------------------------------------------+
| Jet ID  | Model         | Tail #  | Capacity | Status    | Actions|
|---------|---------------|---------|----------|-----------|--------|
| JET001  | Gulfstream... | N123AB  | 12       | Available |[Unassgn]
| JET002  | Bombardier... | N456CD  | 16       | In Flight |[Unassgn]
+--------------------------------------------------------------------+
| Assign New Jet:                                                    |
| [Select Jet Dropdown v]                           [Assign Jet]    |
+--------------------------------------------------------------------+

+--------------------------------------------------------------------+
| Associated Passengers                                               |
+--------------------------------------------------------------------+
| Pass ID | Name      | Passport  | Nationality | Contact  | Actions|
|---------|-----------|-----------|-------------|----------|--------|
| P002    | Alice W.  | US123456  | USA         | +1-555.. |[Unassgn]
| P003    | Bob M.    | US789012  | USA         | +1-555.. |[Unassgn]
+--------------------------------------------------------------------+
| Assign New Passenger:                                              |
| [Select Passenger Dropdown v]                   [Assign Passenger] |
+--------------------------------------------------------------------+
```

## Common Workflows

### Assigning a Jet to a Customer

1. Navigate to customer detail page
2. Scroll to "Associated Aircraft" section
3. Look for "Assign New Jet" form at the bottom
4. Click the dropdown - you'll see unassigned jets like:
   ```
   -- Choose Jet --
   N808NX (Challenger 350) - Available
   ```
5. Select the jet you want to assign
6. Click "Assign Jet" button
7. ✅ Success message: "Jet N808NX assigned to John Smith"
8. Jet now appears in the customer's aircraft table

### Unassigning a Jet from a Customer

1. Navigate to customer detail page
2. Find the jet in the "Associated Aircraft" table
3. Click the "Unassign" button in the Actions column
4. Confirm: "Remove this jet from John Smith?"
5. ✅ Success message: "Jet JET001 unassigned from customer"
6. Jet removed from customer's list
7. Jet now available in "Assign New Jet" dropdown for other customers

### Assigning a Passenger to a Customer

1. Navigate to customer detail page
2. Scroll to "Associated Passengers" section
3. Look for "Assign New Passenger" form at the bottom
4. Click the dropdown - you'll see unassigned passengers like:
   ```
   -- Choose Passenger --
   Bob Jones (US987654)
   Robert Robertson (CA123456)
   ```
5. Select the passenger you want to assign
6. Click "Assign Passenger" button
7. ✅ Success message: "Passenger Bob Jones assigned to John Smith"
8. Passenger now appears in the customer's passenger table

### Unassigning a Passenger from a Customer

1. Navigate to customer detail page
2. Find the passenger in the "Associated Passengers" table
3. Click the "Unassign" button in the Actions column
4. Confirm: "Remove Alice Williams from John Smith?"
5. ✅ Success message: "Passenger Alice Williams unassigned from customer"
6. Passenger removed from customer's list
7. Passenger now available for assignment to other customers

### Creating a New Customer

1. From customer list, click "+ Add New Customer"
2. Fill in required fields:
   - Full Name: "Michael Brown"
   - Company Name: "Brown Aviation"
   - Email Address: "michael@brownaviation.com"
   - Phone Number: "+1-555-9999"
   - Address: "789 Airport Rd, Miami, FL"
3. Click "Create Customer"
4. ✅ Success message: "Customer added successfully with ID: CUST003"
5. Redirected to customer list
6. New customer appears in the table with 0 jets and 0 passengers
7. Click "View Details" to start assigning assets

### Editing Customer Information

1. From customer list or detail page, click "Edit Customer"
2. Modify any fields (name, company, email, phone, address)
3. Click "Update Customer"
4. ✅ Success message: "Customer CUST001 updated successfully"
5. Redirected to customer detail page
6. Changes immediately visible

### Deleting a Customer

1. Navigate to customer edit page
2. Click "Delete Customer" button (red button at bottom)
3. Confirm: "Are you sure you want to delete this customer?"
4. ⚠️ Note: Deletion will fail if customer has associated jets or passengers
5. To delete: first unassign all jets and passengers, then delete
6. ✅ Success message: "Customer CUST001 deleted successfully"

## Important Notes

### Asset Assignment Rules
- A jet can only be assigned to ONE customer at a time
- A passenger can only be assigned to ONE customer at a time
- Unassigned assets (customer_id = "") are available for assignment
- Crew members are NOT assigned to customers (shared resource)

### Access Control
- Only admin users can access customer management
- Customer users can only see their own jets and passengers
- Crew and mechanics can see all data but cannot manage customers
- Regular users will get "Permission denied" if they try to access `/customers`

### Data Persistence
- All assignments/unassignments are immediately saved to `jet_schedule_data.json`
- No manual save required
- Changes are reflected across all views instantly

### Current Data (Example)
```
Customers: 2
- CUST001: John Smith (Smith Enterprises)
  - Jets: JET001, JET002 (2 total)
  - Passengers: P002, P003 (2 total)

- CUST002: Sarah Johnson (Johnson Aviation LLC)
  - Jets: JET003 (1 total)
  - Passengers: P004 (1 total)

Unassigned Assets:
- Jets: N808NX (Challenger 350)
- Passengers: Bob Jones (ID: 1), Robert Robertson (P001)
```

## Troubleshooting

### "Cannot delete customer - has associated jets/passengers"
**Solution**: Navigate to customer detail page and unassign all jets and passengers first, then try deleting again.

### Dropdown shows "No jets/passengers available"
**Reason**: All jets/passengers are already assigned to customers.
**Solution**: Unassign assets from other customers first, or create new jets/passengers.

### "Permission denied" when accessing /customers
**Reason**: You are not logged in as admin.
**Solution**: Log out and log in with admin credentials (username: admin, password: admin123).

### Changes not saving
**Reason**: Permission issues with jet_schedule_data.json file.
**Solution**: Check file permissions and ensure the application has write access.

## Mobile Usage

On mobile devices:
- Tables scroll horizontally (swipe left/right)
- Forms stack vertically for easy input
- Navigation menu collapses to hamburger (☰)
- Touch targets are 44px minimum for easy tapping
- All functionality available on mobile

## Best Practices

1. **Before deleting a customer**: Always unassign all assets first
2. **Naming convention**: Use clear, descriptive company names
3. **Regular audits**: Review customer asset assignments periodically
4. **User accounts**: Create user accounts for customers after adding customer record
5. **Documentation**: Keep customer contact information up to date
6. **Asset tracking**: Monitor which jets/passengers are unassigned

## Quick Reference - Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/customers` | GET | List all customers |
| `/customers/add` | GET/POST | Create new customer |
| `/customers/<id>` | GET | View customer details |
| `/customers/<id>/edit` | GET/POST | Edit customer |
| `/customers/<id>/delete` | POST | Delete customer |
| `/customers/<id>/assign-jet` | POST | Assign jet |
| `/customers/<id>/unassign-jet/<jet_id>` | POST | Unassign jet |
| `/customers/<id>/assign-passenger` | POST | Assign passenger |
| `/customers/<id>/unassign-passenger/<p_id>` | POST | Unassign passenger |

---

For technical documentation, see [CUSTOMER_MANAGEMENT_FEATURE.md](CUSTOMER_MANAGEMENT_FEATURE.md)

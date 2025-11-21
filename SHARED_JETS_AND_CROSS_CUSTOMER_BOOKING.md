# 🤝 Shared Jets & Cross-Customer Booking

Your Manajet app now supports **shared jet ownership** and **cross-customer bookings**! This eliminates customer siloing and enables flexible aircraft sharing.

## What Changed

### ❌ Before (Siloed)
- Each jet could only have ONE owner
- Customers could only see THEIR OWN jets
- Customers could only book flights on jets they owned
- No way to share aircraft between customers

### ✅ After (Shared & Open)
- Jets can have MULTIPLE owners (shared ownership)
- Customers can see ALL available jets for booking
- Customers can book flights on any jet (including others' jets)
- Full support for shared aircraft and charter marketplace model

---

## Key Features

### 1. 🛩️ Shared Jet Ownership

**Multiple customers can co-own the same aircraft:**

- Admin can assign any jet to multiple customers
- Each customer sees the shared jet in their dashboard
- Jets display all co-owners with "SHARED" badge
- Unassigning removes only that customer, others remain

**Example Use Cases:**
- Fractional ownership programs
- Corporate jet sharing between subsidiaries
- Partnership aircraft
- Charter fleet management

### 2. ✈️ Cross-Customer Bookings

**Customers can book flights on any available jet:**

- Customer role users see ALL jets when scheduling flights
- Not limited to only their owned aircraft
- Can book flights on jets owned by other customers
- Passengers remain private (customers only see their own)

**Example Use Cases:**
- Charter marketplace
- On-demand booking from fleet
- Shared fleet operations
- Charter broker model

---

## Technical Implementation

### Data Model Changes

#### Jet Class (`jet_manager.py`)

**OLD:**
```python
class PrivateJet:
    def __init__(self, ..., customer_id: str, ...):
        self.customer_id = customer_id  # Single owner
```

**NEW:**
```python
class PrivateJet:
    def __init__(self, ..., customer_id: str = "", ...):
        # Supports both single string and list
        if isinstance(customer_id, list):
            self.customer_ids = customer_id
        elif customer_id:
            self.customer_ids = [customer_id]  # Convert to list
        else:
            self.customer_ids = []

    # Backward compatibility property
    @property
    def customer_id(self):
        return self.customer_ids[0] if self.customer_ids else ""
```

**Key Changes:**
- `customer_id` → `customer_ids` (list)
- Maintains backward compatibility with property
- `to_dict()` saves both formats for compatibility
- `from_dict()` handles both old and new data

### Filter Logic Updates

#### Filter by Customer (`web_app.py`)

**OLD:**
```python
def filter_by_customer(items, customer_field='customer_id'):
    if user.role == 'customer':
        return [item for item in items if getattr(item, customer_field, None) == user.related_id]
```

**NEW:**
```python
def filter_by_customer(items, customer_field='customer_id'):
    if user.role == 'customer':
        filtered = []
        for item in items:
            # Check if customer_id is in jet's owner list
            if hasattr(item, 'customer_ids'):
                if user.related_id in item.customer_ids:
                    filtered.append(item)
            # For other items with single customer_id
            elif getattr(item, customer_field, None) == user.related_id:
                filtered.append(item)
        return filtered
```

**Key Changes:**
- Checks if customer ID is IN the list (not equal to)
- Supports shared jets automatically
- Maintains single-owner logic for passengers

### Booking Access Changes

#### Flight Scheduling (`web_app.py:add_flight`)

**OLD:**
```python
if user.role == 'customer':
    available_jets = filter_by_customer(manager.jets.values())  # Only their jets
    available_passengers = filter_by_customer(manager.passengers.values())
```

**NEW:**
```python
if user.role == 'customer':
    available_jets = list(manager.jets.values())  # ALL jets visible
    available_passengers = filter_by_customer(manager.passengers.values())  # Still private
```

**Key Changes:**
- Customers now see ALL jets for booking
- Passengers remain private per customer
- Enables cross-customer bookings

### Admin Assignment Updates

#### Assign Jet to Customer (`web_app.py`)

**OLD:**
```python
def assign_jet_to_customer(customer_id):
    jet.customer_id = customer_id  # Replaces owner
    flash(f'Jet {jet_id} assigned to {customer.name}')
```

**NEW:**
```python
def assign_jet_to_customer(customer_id):
    if customer_id not in jet.customer_ids:
        jet.customer_ids.append(customer_id)  # Adds to owner list
        flash(f'Jet {jet_id} assigned to {customer.name}. Shared with {len(jet.customer_ids)} customer(s).')
    else:
        flash(f'Jet {jet_id} is already assigned to {customer.name}')
```

**Key Changes:**
- Adds to list instead of replacing
- Shows shared count
- Prevents duplicate assignments

#### Unassign Jet from Customer

**OLD:**
```python
def unassign_jet_from_customer(customer_id, jet_id):
    jet.customer_id = ''  # Removes owner completely
```

**NEW:**
```python
def unassign_jet_from_customer(customer_id, jet_id):
    if customer_id in jet.customer_ids:
        jet.customer_ids.remove(customer_id)  # Removes only this customer
        if len(jet.customer_ids) > 0:
            flash(f'Still shared with {len(jet.customer_ids)} other customer(s).')
        else:
            flash(f'Fully unassigned (no owners)')
```

**Key Changes:**
- Removes only that customer
- Other owners remain
- Shows remaining owners count

---

## UI Changes

### Jets List (`templates/jets.html`)

**NEW "Owners" Column:**
```html
<th>Owners</th>
...
<td>
    {% for customer_id in jet.customer_ids %}
        <span class="badge">{{ customer.name }}</span>
    {% endfor %}
    {% if jet.customer_ids|length > 1 %}
        <span class="badge">SHARED</span>
    {% endif %}
</td>
```

**Shows:**
- All customer names as badges
- "SHARED" indicator for multiple owners
- "Unassigned" for jets with no owners

### Customer Detail Page (`templates/customer_detail.html`)

**NEW "Co-Owners" Column:**
```html
<th>Co-Owners</th>
...
<td>
    {% if other_owners|length > 0 %}
        <span class="badge">🤝 SHARED</span>
        <div>with {{ other_owners|join(', ') }}</div>
    {% endif %}
</td>
```

**NEW Assignment Section:**
- Shows ALL jets (not just unassigned)
- Displays existing owners in dropdown
- Allows assigning jets that already have owners
- Clear "Supports Shared Ownership" messaging

---

## User Experience

### For Customers

**Viewing Jets:**
- Dashboard shows only jets they own/co-own
- Shared jets display "SHARED" badge
- See co-owner names on detail page

**Booking Flights:**
- Can see ALL available jets when scheduling
- Can book on any jet (including others')
- Clear indication of jet ownership in dropdown

**Example Workflow:**
1. Customer logs in
2. Goes to "Schedule Flight"
3. Sees entire fleet of available jets
4. Selects any jet (owned by them or others)
5. Adds their own passengers
6. Books the flight

### For Admins

**Managing Shared Ownership:**
1. Go to Customer detail page
2. Scroll to "Assign Aircraft"
3. Select any jet (even if already owned)
4. Click "Assign Aircraft"
5. Jet now shared between multiple customers

**Viewing Shared Jets:**
- Jets list shows all owners
- Customer detail shows co-owners
- Clear "SHARED" indicators throughout

---

## Data Migration

### Automatic Backward Compatibility

**Existing Data:**
- Old jets with `customer_id` (string) automatically convert to `customer_ids` (list)
- No manual migration needed
- `from_dict()` handles both formats

**Saving Data:**
- Both `customer_id` and `customer_ids` saved in JSON
- `customer_id` = first owner (for old code compatibility)
- `customer_ids` = full list (for new code)

### Example Data Format

**OLD JSON:**
```json
{
  "jet_id": "J001",
  "model": "Gulfstream G650",
  "customer_id": "C001"
}
```

**NEW JSON:**
```json
{
  "jet_id": "J001",
  "model": "Gulfstream G650",
  "customer_id": "C001",
  "customer_ids": ["C001", "C002", "C003"]
}
```

---

## Business Models Enabled

### 1. Fractional Ownership
- Multiple customers own percentages of aircraft
- Each owner can book flight time
- Shared maintenance costs

### 2. Charter Marketplace
- Jet owners list aircraft for charter
- Other customers book available jets
- Revenue sharing model

### 3. Corporate Fleet Sharing
- Multiple subsidiaries share corporate jets
- Centralized fleet management
- Cost optimization

### 4. Partnership Aircraft
- Business partners co-own aircraft
- Shared usage and costs
- Equal access to scheduling

---

## Configuration

### Enable/Disable Features

**To restrict customers to only their jets (revert to siloed):**

In `web_app.py`, change line 610:
```python
# Revert to siloed model
available_jets = filter_by_customer(manager.jets.values())
```

**To disable shared ownership (one owner per jet):**

In `web_app.py:assign_jet_to_customer`, change line 1029:
```python
# Replace owner instead of adding
jet.customer_ids = [customer_id]
```

---

## API Updates

### Getting Jet Owners

```python
jet = manager.get_jet('J001')
print(f"Owners: {len(jet.customer_ids)}")
for customer_id in jet.customer_ids:
    customer = manager.get_customer(customer_id)
    print(f"  - {customer.name}")
```

### Checking Shared Ownership

```python
if len(jet.customer_ids) > 1:
    print("This is a shared jet!")
```

### Finding Customer's Jets (Including Shared)

```python
customer_jets = [j for j in manager.jets.values()
                 if customer_id in j.customer_ids]
```

---

## Testing

### Test Shared Ownership

1. **Create 2 customers** (admin login)
2. **Create 1 jet**
3. **Assign jet to Customer A**
   - Go to Customer A detail
   - Assign the jet
4. **Assign same jet to Customer B**
   - Go to Customer B detail
   - Assign the same jet
5. **Verify both customers see it**
   - Login as Customer A → see jet
   - Login as Customer B → see jet
6. **View Jets list**
   - Should show both owners
   - Should show "SHARED" badge

### Test Cross-Customer Booking

1. **Login as Customer A**
2. **Go to Schedule Flight**
3. **Select jet owned by Customer B**
4. **Add Customer A's passengers**
5. **Schedule the flight**
6. **Verify:**
   - Flight created successfully
   - Customer A can see their passengers
   - Flight uses Customer B's jet

---

## Performance Impact

**Minimal performance impact:**
- `customer_ids` list lookups are O(n) where n = owners per jet
- Typically n = 1-5, very fast
- No database joins needed (JSON storage)
- Backward compatibility property has no overhead

---

## Security Considerations

### Data Privacy

**Passengers remain private:**
- Customers only see their own passengers
- Cannot view other customers' passenger lists
- `filter_by_customer()` still applies to passengers

**Jets are visible but not editable:**
- Customers see all jets for booking
- Cannot edit jets they don't own
- Admin controls all jet assignments

### Flight Access

**Customers can only:**
- View flights on jets they own
- Schedule flights with their own passengers
- Book any available jet

**Customers cannot:**
- See other customers' flight details
- Access other customers' passengers
- Modify jets they don't own

---

## Troubleshooting

### Issue: Shared jets not showing

**Check:**
```python
jet = manager.get_jet('J001')
print(f"customer_ids: {jet.customer_ids}")  # Should be list
print(f"customer_id: {jet.customer_id}")     # Should be first item
```

### Issue: Customer can't see shared jet

**Verify customer ID is in list:**
```python
customer_id = 'C001'
jet = manager.get_jet('J001')
print(f"Is {customer_id} an owner? {customer_id in jet.customer_ids}")
```

### Issue: Old data not converting

**Check from_dict:**
```python
# Old format should auto-convert
old_data = {'jet_id': 'J001', 'model': 'G650', 'customer_id': 'C001'}
jet = PrivateJet.from_dict(old_data)
print(f"customer_ids: {jet.customer_ids}")  # Should be ['C001']
```

---

## Summary

✅ **Shared Ownership** - Multiple customers per jet
✅ **Cross-Customer Booking** - Book any available jet
✅ **Backward Compatible** - Works with existing data
✅ **Admin Controls** - Full shared ownership management
✅ **Privacy Maintained** - Passengers still private
✅ **Clear UI** - "SHARED" indicators throughout

**Your Manajet system now supports modern, flexible aircraft sharing! 🚀**

---

## Files Modified

1. **jet_manager.py** - Updated PrivateJet class for multiple owners
2. **web_app.py** - Updated filter logic and flight booking access
3. **templates/jets.html** - Added "Owners" column with shared indicators
4. **templates/customer_detail.html** - Added co-owner display and shared assignment

**Zero breaking changes - fully backward compatible!**

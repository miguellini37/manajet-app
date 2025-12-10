# Quick Start Guide

## You're All Set! 🎉

Your private jet management app now has **customer separation** with **role-based authentication**.

## Start the App Right Now

```bash
python web_app.py
```

Then open: **http://localhost:5000**

## Login Credentials

### Admin (Full Access)
- **Username:** `admin`
- **Password:** `admin123`

### Customer 1 (John Smith)
- **Username:** `johnsmith`
- **Password:** `customer123`
- **Owns:** 2 jets, 2 passengers

### Customer 2 (Sarah Johnson)
- **Username:** `sarahjohnson`
- **Password:** `customer123`
- **Owns:** 1 jet, 1 passenger

### Pilot
- **Username:** `pilot_mike`
- **Password:** `crew123`

### Mechanic
- **Username:** `mechanic_joe`
- **Password:** `mech123`

## What Each User Can Do

| Role | Can See | Can Do |
|------|---------|--------|
| **Customer** | Only their own jets, passengers, flights | Add passengers, schedule flights on their jets |
| **Crew** | All jets and flights | View assignments across all customers |
| **Mechanic** | All jets and maintenance | Create/update maintenance records |
| **Admin** | Everything | Manage customers, add jets, full control |

## Test Customer Isolation

1. Login as `johnsmith`
2. Go to "Jets" - see only 2 jets (JET001, JET002)
3. Logout
4. Login as `sarahjohnson`
5. Go to "Jets" - see only 1 jet (JET003)

**Each customer is completely isolated!**

## Key Features

✅ Multiple customers with separate data
✅ Secure authentication with password hashing
✅ Role-based access control
✅ Customer self-registration
✅ Auto-assignment of data to customers
✅ Shared crew resources across customers

## Files You Have

- `jet_manager.py` - Core business logic (Customer & User classes added)
- `web_app.py` - Web interface with authentication
- `jet_schedule_data.json` - Your database
- `templates/` - HTML templates including login/register pages
- `SETUP_COMPLETE.md` - Full documentation
- `MULTI_CUSTOMER_AUTH_CHANGES.md` - Technical details

## What Changed

**Before:** Single user, all data visible to everyone

**Now:**
- Each customer owns specific jets
- Customers can only see their own data
- Crew/mechanics see all data (they work for multiple customers)
- Admin manages everything

## Need More Help?

Read these in order:
1. **SETUP_COMPLETE.md** - Complete overview
2. **MULTI_CUSTOMER_AUTH_CHANGES.md** - Technical details

---

**Ready to fly! Start with:** `python web_app.py`

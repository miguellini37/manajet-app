# 🔄 Automatic Status Updates

Your Manajet app now automatically updates flight and maintenance statuses based on time!

## How It Works

### Automatic Updates Every 5 Minutes
The system checks flight and maintenance statuses before each page load. If more than 5 minutes have passed since the last check, statuses are automatically updated:

**Flight Status Progression:**
- **Scheduled** → Before departure time
- **In Progress** → Between departure and arrival time
- **Completed** → After arrival time

**Maintenance Status Progression:**
- **Scheduled** → Before scheduled date
- **In Progress** → After scheduled date (if not completed)
- **Completed** → After completion date is set

### Smart Status Detection
The system parses various datetime formats:
- `YYYY-MM-DD HH:MM:SS`
- `YYYY-MM-DD HH:MM`
- `YYYY-MM-DD`
- `MM/DD/YYYY HH:MM`
- `DD/MM/YYYY HH:MM`

## Admin Controls

### Manual Status Update
Admins can trigger an immediate status update from the dashboard:
1. Go to Dashboard
2. Scroll to "Automatic Status Updates" section
3. Click "🔄 Update All Statuses Now"
4. See summary of updated records

### View Upcoming Events
Check what's happening in the next 24 hours:
1. Go to Dashboard
2. Click "📅 View Upcoming Events"
3. See flights and maintenance scheduled soon
4. Color-coded urgency:
   - 🔴 Red: Within 2 hours
   - 🟡 Yellow: Within 6 hours
   - 🟢 Green: Within 24 hours

## Technical Details

### Files Modified
- `web_app.py` - Added status updater integration
- `status_updater.py` - Core status update logic
- `dashboard.html` - Admin controls for status updates
- `upcoming_events.html` - View upcoming flights/maintenance

### Background Execution
```python
# Status updater runs every 5 minutes
status_updater = create_scheduled_task(manager, interval_minutes=5)

@app.before_request
def auto_update_statuses():
    """Check if update needed before each request"""
    status_updater.run_if_needed()
```

### Status Update Logic

**Flights:**
```python
if now < departure_time:
    status = 'Scheduled'
elif departure_time <= now < arrival_time:
    status = 'In Progress'
elif now >= arrival_time:
    status = 'Completed'
```

**Maintenance:**
```python
if completion_date and now >= completion_date:
    status = 'Completed'
elif now >= scheduled_date and not completion_date:
    status = 'In Progress'
else:
    status = 'Scheduled'
```

## Example Output

When manual update is triggered:
```
🔄 Running automatic status updates...
⏰ Current time: 2025-01-15 14:30:00

✅ Flight F001: Scheduled → In Progress
✅ Flight F002: In Progress → Completed
✅ Maintenance M003: Scheduled → In Progress

✨ Updated 2 flights and 1 maintenance records
```

## Benefits

✅ **No Manual Updates** - Statuses update automatically
✅ **Always Accurate** - Real-time status based on current time
✅ **Zero Maintenance** - Runs in background automatically
✅ **Audit Trail** - Console logs show all updates
✅ **Efficient** - Only runs every 5 minutes, not on every request

## API Access

Get upcoming events programmatically:
```python
from status_updater import StatusUpdater

updater = StatusUpdater(manager)
upcoming = updater.get_upcoming_events(hours=24)

print(f"Flights in next 24h: {len(upcoming['flights'])}")
print(f"Maintenance in next 24h: {len(upcoming['maintenance'])}")
```

## Configuration

Change update interval in `web_app.py`:
```python
# Update every 10 minutes instead of 5
status_updater = create_scheduled_task(manager, interval_minutes=10)
```

## Troubleshooting

**Issue:** Statuses not updating
**Solution:** Check that datetime fields are properly formatted

**Issue:** Update interval too frequent
**Solution:** Increase `interval_minutes` parameter

**Issue:** Need immediate update
**Solution:** Use "Update All Statuses Now" button (admin only)

## Integration with Other Features

Works seamlessly with:
- ✅ Activity Log - Updates are logged
- ✅ Email Notifications - Can trigger notifications on status change
- ✅ Dashboard - Shows real-time accurate statuses
- ✅ Search & Filter - Search by current status
- ✅ CSV Export - Export with current statuses

---

**Status updates keep your Manajet system always accurate! 🚀**

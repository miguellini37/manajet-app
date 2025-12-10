# Manajet iOS App

Native iOS application for Manajet Private Jet Management System built with SwiftUI.

## Features

- ✈️ **Flight Scheduling** with location-based airport search
- 🕐 **Flexible Time Selection** (Depart at / Arrive by)
- ✅ **Approval Workflow** for pilots to review customer flight requests
- 📱 **Native iOS Design** with modern UI/UX
- 🔐 **Secure Authentication** with session management
- 📊 **Dashboard** with real-time stats and quick actions

## Requirements

- Xcode 15.0 or later
- iOS 17.0 or later
- Swift 5.9 or later
- Active Apple Developer account (for TestFlight)

## Project Structure

```
Manajet-iOS/
├── Manajet/
│   ├── Models/
│   │   └── Models.swift           # Data models matching backend
│   ├── Services/
│   │   └── APIClient.swift        # Backend API communication
│   ├── Views/
│   │   ├── LoginView.swift        # Authentication
│   │   ├── DashboardView.swift    # Main dashboard
│   │   ├── FlightScheduleView.swift  # Flight scheduling with search
│   │   └── ApprovalsView.swift    # Pilot approval workflow
│   ├── ManajetApp.swift           # App entry point
│   └── Info.plist                 # App configuration
└── README.md
```

## Setup Instructions

### 1. Create Xcode Project

1. Open Xcode
2. File → New → Project
3. Choose "App" template
4. Configure:
   - Product Name: **Manajet**
   - Team: Your Apple Developer Team
   - Organization Identifier: `com.yourcompany` (use your domain)
   - Interface: **SwiftUI**
   - Language: **Swift**
   - Storage: **None**
5. Choose save location
6. Create project

### 2. Add Source Files

1. In Xcode, right-click on "Manajet" folder
2. Add Files to "Manajet"
3. Select all files from this directory:
   - Models/Models.swift
   - Services/APIClient.swift
   - Views/*.swift
   - ManajetApp.swift
4. Make sure "Copy items if needed" is checked
5. Click Add

### 3. Configure Backend URL

Open `Services/APIClient.swift` and update the `baseURL`:

```swift
// For local testing (Mac on same network)
private let baseURL = "http://YOUR_IP:5000"

// For production deployment
private let baseURL = "https://your-backend-url.com"
```

To find your local IP:
- macOS: System Settings → Network → your connection → Details → TCP/IP
- Windows: `ipconfig` in Command Prompt

### 4. Configure App Transport Security

Add this to `Info.plist` (for local development only):

1. Right-click Info.plist → Open As → Source Code
2. Add before `</dict>`:

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

**⚠️ IMPORTANT:** Remove this before production! Use HTTPS in production.

### 5. Build and Run

1. Select a simulator or device
2. Click Run (⌘R)
3. App should launch and show login screen

## Backend Setup

### Required API Endpoints

The iOS app needs these additional endpoints in your Flask backend:

#### 1. Current User Endpoint
Add to `web_app.py`:

```python
@app.route('/api/current-user')
@login_required
def api_current_user():
    """Get current logged in user"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401

    return jsonify({
        'user_id': user.user_id,
        'username': user.username,
        'role': user.role,
        'related_id': user.related_id,
        'email': user.email if hasattr(user, 'email') else ''
    })
```

#### 2. Flights API Endpoint
Add to `web_app.py`:

```python
@app.route('/api/flights')
@login_required
def api_flights():
    """Get all flights for current user"""
    user = get_current_user()

    if user.role == 'customer':
        customer_jets = [j.jet_id for j in manager.jets.values() if user.related_id in j.customer_ids]
        flights = [f for f in manager.flights.values() if f.jet_id in customer_jets]
    else:
        flights = list(manager.flights.values())

    return jsonify([f.to_dict() for f in flights])
```

#### 3. Schedule Flight API
Add to `web_app.py`:

```python
@app.route('/api/flights/schedule', methods=['POST'])
@login_required
def api_schedule_flight():
    """Schedule a new flight via API"""
    user = get_current_user()
    data = request.json

    # Determine approval status
    if user.role == 'customer':
        approval_status = "Pending"
    else:
        approval_status = "Approved"

    flight_id = manager.schedule_flight(
        "",
        data['jet_id'],
        data['departure'],
        data['destination'],
        data['departure_time'],
        data['arrival_time'],
        data['passenger_ids'],
        data['crew_ids'],
        approval_status,
        user.user_id
    )

    if flight_id:
        manager.save_data()
        return jsonify({'success': True, 'flight_id': flight_id})
    else:
        return jsonify({'success': False, 'error': 'Failed to schedule flight'}), 400
```

#### 4. Pending Approvals API
Add to `web_app.py`:

```python
@app.route('/api/approvals/pending')
@role_required('crew')
def api_pending_approvals():
    """Get pending approvals for current pilot"""
    user = get_current_user()
    crew_member = manager.get_crew(user.related_id) if user.related_id else None

    if not crew_member or crew_member.crew_type != 'Pilot':
        return jsonify({'error': 'Only pilots can access approvals'}), 403

    pending = manager.get_pending_approvals(crew_member.crew_id)
    return jsonify([f.to_dict() for f in pending])
```

#### 5. Jets API
```python
@app.route('/api/jets')
@login_required
def api_jets():
    """Get all jets"""
    user = get_current_user()

    if user.role == 'customer':
        jets = [j for j in manager.jets.values() if user.related_id in j.customer_ids]
    else:
        jets = list(manager.jets.values())

    return jsonify([j.to_dict() for j in jets])
```

#### 6. Passengers API
```python
@app.route('/api/passengers')
@login_required
def api_passengers():
    """Get all passengers"""
    user = get_current_user()

    if user.role == 'customer':
        passengers = [p for p in manager.passengers.values() if p.customer_id == user.related_id]
    else:
        passengers = list(manager.passengers.values())

    return jsonify([p.to_dict() for p in passengers])
```

#### 7. Crew API
```python
@app.route('/api/crew')
@login_required
def api_crew():
    """Get all crew members"""
    crew_list = list(manager.crew.values())
    return jsonify([c.to_dict() for c in crew_list])
```

## Testing

### Local Testing

1. Start Flask backend: `python web_app.py`
2. Update backend URL in APIClient.swift with your local IP
3. Run iOS app in simulator
4. Login with test credentials:
   - Customer: `johnsmith` / `customer123`
   - Pilot: `pilot_mike` / `crew123`

### Test Flows

**Customer Flow:**
1. Login as customer
2. Schedule new flight with location search
3. Choose "Depart at" or "Arrive by"
4. Flight shows as "Pending Approval"

**Pilot Flow:**
1. Login as pilot
2. See notification badge on Approvals
3. Review pending flight requests
4. Approve or reject flights

## TestFlight Deployment

See `TESTFLIGHT_DEPLOYMENT_GUIDE.md` for complete instructions.

## Troubleshooting

### Can't connect to backend
- Check backend URL in APIClient.swift
- Ensure Flask app is running
- Check firewall allows connections on port 5000
- Verify you're on the same network (for local testing)

### Login fails
- Check backend has required API endpoints
- Verify credentials are correct
- Check Flask logs for errors

### App crashes on launch
- Check all source files are added to target
- Verify no syntax errors in Swift files
- Check Xcode console for error messages

## Architecture

### MVVM Pattern
- **Models**: Data structures (`Models.swift`)
- **Views**: SwiftUI views (`Views/*.swift`)
- **ViewModels**: Business logic (`@StateObject` classes in views)
- **Services**: API client and utilities (`Services/*.swift`)

### API Communication
- Uses URLSession for HTTP requests
- Cookie-based authentication (matches Flask sessions)
- JSON encoding/decoding with Codable
- Async/await for modern Swift concurrency

## License

Private use only. Part of Manajet project.

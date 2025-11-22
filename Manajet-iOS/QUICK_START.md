# Manajet iOS - Quick Start Guide

Get your iOS app running in 15 minutes!

## Step 1: Create Xcode Project (5 minutes)

1. **Open Xcode** → File → New → Project
2. **Choose:** App template
3. **Configure:**
   - Product Name: **Manajet**
   - Team: Your Apple Developer Team
   - Organization ID: `com.yourcompany`
   - Interface: **SwiftUI**
   - Language: **Swift**
4. **Save** in a location you prefer

## Step 2: Add Source Files (3 minutes)

1. **Right-click** "Manajet" folder in Xcode
2. **Add Files to "Manajet"**
3. **Navigate** to `Manajet-iOS/Manajet` folder
4. **Select all** `.swift` files in:
   - Models/
   - Services/
   - Views/
   - ManajetApp.swift
5. **Check** "Copy items if needed"
6. **Click** Add

## Step 3: Configure Backend URL (2 minutes)

Open `Services/APIClient.swift` and update line 21:

```swift
// Find your Mac's IP address:
// Mac: System Settings → Network → Details → TCP/IP
// Windows PC: Open Command Prompt → ipconfig

private let baseURL = "http://YOUR_IP_ADDRESS:5000"
// Example: "http://192.168.1.100:5000"
```

## Step 4: Enable HTTP (Development Only) (2 minutes)

1. **Open** Info.plist
2. **Right-click** → Open As → Source Code
3. **Add before** `</dict>`:

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

⚠️ **Remove this before TestFlight/App Store!**

## Step 5: Start Backend (1 minute)

In your terminal:

```bash
cd manajet-app
python web_app.py
```

Flask should start on `http://0.0.0.0:5000`

## Step 6: Run App! (2 minutes)

1. **Select** iPhone simulator (iPhone 15 Pro recommended)
2. **Click** Run button (or press ⌘R)
3. **Wait** for build to complete
4. **App launches!**

## Step 7: Test Login

Use these credentials:

**Customer Account:**
- Username: `johnsmith`
- Password: `customer123`

**Pilot Account:**
- Username: `pilot_mike`
- Password: `crew123`

**Admin Account:**
- Username: `admin`
- Password: `admin123`

## What to Try

### As Customer:
1. ✈️ Schedule a flight
2. 🔍 Search airports by city name (try "Los Angeles")
3. ⏰ Choose "Arrive by" instead of "Depart at"
4. 👥 Add a new passenger
5. 📋 See your flight listed as "Pending Approval"

### As Pilot:
1. 🔔 See notification badge on Approvals
2. 📝 Review pending flight requests
3. ✅ Approve or reject flights
4. 📊 View dashboard stats

## Troubleshooting

### Can't connect to backend?

1. **Check** Flask is running (should see logs in terminal)
2. **Verify** backend URL in APIClient.swift
3. **Ensure** Mac and iPhone are on same WiFi network
4. **Try** pinging your IP from another device

### Login doesn't work?

1. **Check** Flask logs for error messages
2. **Verify** credentials are correct
3. **Ensure** backend API endpoints were added to `web_app.py`

### Build errors?

1. **Clean** build folder (⌘ + Shift + K)
2. **Check** all files were added to target
3. **Verify** you're using Xcode 15+
4. **Restart** Xcode

### App crashes on launch?

1. **Check** Xcode console for error messages
2. **Verify** all Swift files were added correctly
3. **Ensure** ManajetApp.swift is set as entry point

## Next Steps

Once everything works:

1. 📱 **Test on real iPhone** (connect via USB, select device)
2. 🚀 **Deploy backend** to cloud (Railway, DigitalOcean)
3. 🔐 **Update to HTTPS** backend URL
4. 🧪 **Submit to TestFlight** (see TESTFLIGHT_DEPLOYMENT_GUIDE.md)

## File Structure

```
Manajet-iOS/
├── Manajet/
│   ├── Models/
│   │   └── Models.swift              # All data models
│   ├── Services/
│   │   └── APIClient.swift           # Backend communication
│   ├── Views/
│   │   ├── LoginView.swift           # Login screen
│   │   ├── DashboardView.swift       # Main dashboard
│   │   ├── FlightScheduleView.swift  # Flight booking
│   │   └── ApprovalsView.swift       # Pilot approvals
│   └── ManajetApp.swift              # App entry point
├── README.md                         # Detailed documentation
├── TESTFLIGHT_DEPLOYMENT_GUIDE.md    # Full TestFlight guide
└── QUICK_START.md                    # This file
```

## Features Implemented

✅ Modern SwiftUI design with gradient backgrounds
✅ Cookie-based authentication (matches Flask sessions)
✅ Location-based airport search with autocomplete
✅ Flexible time selection (Depart at / Arrive by)
✅ Automatic flight duration calculation
✅ Flight approval workflow for pilots
✅ Real-time notification badges
✅ Add passengers on-the-fly
✅ Multi-select for passengers and crew
✅ Role-based access control
✅ Async/await networking
✅ Pull-to-refresh
✅ Error handling with alerts

## Need Help?

- **Backend API:** Check `web_app.py` has all mobile endpoints
- **Xcode Issues:** Clean build, restart Xcode
- **Network Issues:** Verify firewall, WiFi, IP address
- **TestFlight:** See TESTFLIGHT_DEPLOYMENT_GUIDE.md

---

**You're all set!** Enjoy your native iOS Manajet app! 🎉

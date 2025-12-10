# Update iOS App for Production Backend

Your backend is deployed! Now let's point the iOS app to it.

## Your Production URL

After deploying to DigitalOcean, you received a URL like:
```
https://manajet-xxxxx.ondigitalocean.app
```

**Copy this URL** - you'll need it below.

## Option 1: Quick Update (Development) - 2 minutes

For quick testing with a single environment:

### Step 1: Update APIClient.swift

1. Open your Xcode project
2. Navigate to: `Manajet/Services/APIClient.swift`
3. Find line ~21:
   ```swift
   private let baseURL = "http://localhost:5000"
   ```
4. Replace with your production URL:
   ```swift
   private let baseURL = "https://manajet-xxxxx.ondigitalocean.app"
   ```
5. **Save file** (⌘S)

### Step 2: Remove HTTP Exception

Since we're now using HTTPS, remove the insecure transport setting:

1. Open `Info.plist`
2. Find and **DELETE** this entire section:
   ```xml
   <key>NSAppTransportSecurity</key>
   <dict>
       <key>NSAllowsArbitraryLoads</key>
       <true/>
   </dict>
   ```
3. **Save file**

### Step 3: Test

1. Clean build: **⌘ + Shift + K**
2. Run app: **⌘ + R**
3. Try logging in:
   - Username: `admin`
   - Password: `admin123`
4. Schedule a flight
5. Test approvals

**Done!** Your app now uses production backend. ✅

## Option 2: Professional Setup (Recommended) - 10 minutes

Use build configurations to easily switch between local dev and production.

### Step 1: Create Configuration File

1. In Xcode, right-click `Manajet` folder
2. New File → **Swift File**
3. Name: `Configuration.swift`
4. Add this code:

```swift
//
//  Configuration.swift
//  Manajet
//
//  Environment configuration
//

import Foundation

enum Environment {
    case development
    case production

    var baseURL: String {
        switch self {
        case .development:
            return "http://192.168.1.100:5000"  // ← Your local IP
        case .production:
            return "https://manajet-xxxxx.ondigitalocean.app"  // ← Your production URL
        }
    }

    var name: String {
        switch self {
        case .development:
            return "Development"
        case .production:
            return "Production"
        }
    }
}

class Configuration {
    // CHANGE THIS TO SWITCH ENVIRONMENTS
    static let current: Environment = .production  // ← Change to .development for local testing

    static var baseURL: String {
        return current.baseURL
    }

    static var environment: String {
        return current.name
    }
}
```

5. Update these URLs:
   - `development`: Your Mac's local IP (from Quick Start guide)
   - `production`: Your DigitalOcean URL

### Step 2: Update APIClient.swift

1. Open `Services/APIClient.swift`
2. Find line ~21:
   ```swift
   private let baseURL = "http://localhost:5000"
   ```
3. Replace with:
   ```swift
   private let baseURL = Configuration.baseURL
   ```
4. **Save file**

### Step 3: Switch Environments Easily

To use **local development** backend:
```swift
// In Configuration.swift
static let current: Environment = .development
```

To use **production** backend:
```swift
// In Configuration.swift
static let current: Environment = .production
```

Just change one line, rebuild, and you're switched! 🎉

### Step 4: Show Environment in App (Optional)

Add environment indicator to dashboard:

In `DashboardView.swift`, add to the welcome header:

```swift
VStack(alignment: .leading, spacing: 8) {
    Text("Welcome back,")
        .font(.title3)
        .foregroundColor(.secondary)

    if let user = apiClient.currentUser {
        Text(user.username)
            .font(.system(size: 32, weight: .bold))
    }

    // Add this:
    Text("Environment: \(Configuration.environment)")
        .font(.caption)
        .foregroundColor(.secondary)
        .padding(.horizontal, 8)
        .padding(.vertical, 4)
        .background(Color.blue.opacity(0.1))
        .cornerRadius(4)
}
```

Now you always know which backend you're using!

## Option 3: Advanced - Build Schemes (For Pros) - 20 minutes

Use Xcode schemes to automatically switch environments.

### Step 1: Duplicate Scheme

1. Xcode → Product → Scheme → **Manage Schemes**
2. Select **Manajet**, click **⚙️ (gear)** → **Duplicate**
3. Rename to **Manajet-Production**
4. Click **Close**

### Step 2: Add Build Configuration

1. Project Navigator → Click project (blue icon)
2. Select **Manajet** project (not target)
3. **Info** tab
4. Under **Configurations**, click **+** → **Duplicate "Release" Configuration**
5. Name it **Production**

### Step 3: Add User-Defined Settings

1. Click **Manajet** target
2. **Build Settings** tab
3. Click **+** → **Add User-Defined Setting**
4. Name: `API_BASE_URL`
5. Set values:
   - Debug: `http://192.168.1.100:5000`
   - Release: `http://localhost:5000`
   - Production: `https://manajet-xxxxx.ondigitalocean.app`

### Step 4: Update Configuration.swift

```swift
class Configuration {
    static var baseURL: String {
        #if PRODUCTION
        return "https://manajet-xxxxx.ondigitalocean.app"
        #elseif DEBUG
        return "http://192.168.1.100:5000"
        #else
        return "http://localhost:5000"
        #endif
    }
}
```

### Step 5: Set Compiler Flags

1. **Build Settings** → Search "flags"
2. **Swift Compiler - Custom Flags**
3. Under **Production**, add to "Other Swift Flags":
   ```
   -D PRODUCTION
   ```

### Step 6: Use Schemes

- **Develop locally:** Select **Manajet** scheme, run
- **Production testing:** Select **Manajet-Production** scheme, run
- **TestFlight:** Archive with **Manajet-Production** scheme

## Verify Production Connection

### Test Checklist

1. ✅ **Login works**
   - Try all user roles (admin, customer, pilot)

2. ✅ **Data loads**
   - Dashboard shows correct stats
   - Flights list appears
   - Passengers load

3. ✅ **Create operations**
   - Schedule new flight
   - Add passenger
   - Upload works

4. ✅ **Approvals work**
   - Customer schedules flight
   - Pilot sees notification
   - Can approve/reject

5. ✅ **Search works**
   - Airport search returns results
   - Flight duration calculated

### Common Issues

**"Could not connect to server"**
- Check backend URL is correct (no typos)
- Verify backend is actually running on DigitalOcean
- Check backend URL in browser - should show login page

**"Authentication failed"**
- Backend might not have data initialized
- Run `setup_initial_data.py` on production
- Check user credentials

**"Invalid response"**
- Check backend logs in DigitalOcean
- API endpoints might have errors
- Check Flask logs for Python errors

**SSL/Certificate errors**
- Make sure URL uses `https://` (not `http://`)
- DigitalOcean provides automatic SSL certificates
- Wait 5 minutes after deployment for SSL to activate

## Initialize Production Data

Your production backend needs sample data!

### Option 1: DigitalOcean Console

1. Go to DigitalOcean → Apps → Your App
2. Click **"Console"** tab
3. Click **"Run Console"**
4. Run:
   ```bash
   python setup_initial_data.py
   ```
5. Exit console

### Option 2: API Initialization

Create an admin account via the iOS app:
1. Open app
2. Should see "No users" or similar
3. (Your web app has a register route - use that first)

Or use the web interface:
1. Open `https://your-app-url.ondigitalocean.app`
2. Log in as admin
3. Use web interface to create initial data

## Environment Variables Reference

Make sure these are set in DigitalOcean:

```bash
SECRET_KEY=<64-character-hex-string>  # REQUIRED
DEBUG=False                            # REQUIRED
SESSION_COOKIE_SECURE=True            # REQUIRED for HTTPS
SESSION_COOKIE_HTTPONLY=True          # Security
SESSION_COOKIE_SAMESITE=Lax          # Security
PERMANENT_SESSION_LIFETIME=3600       # 1 hour sessions
PORT=5000                             # Required
```

## TestFlight with Production

When building for TestFlight:

1. **Set to production:**
   ```swift
   static let current: Environment = .production
   ```

2. **Remove NSAppTransportSecurity** from Info.plist

3. **Archive:**
   - Product → Archive
   - Follow TestFlight guide

4. **Testers will use production backend!**

## Monitoring iOS ↔ Backend

### Backend Logs

1. DigitalOcean → Apps → Your App
2. **Runtime Logs** tab
3. Watch for:
   - `/api/current-user` calls
   - `/api/flights` requests
   - Login attempts
   - Errors

### Xcode Debugging

1. Run app in debug mode
2. Check console for:
   - API request URLs
   - Response data
   - Error messages

### Network Debugging

Add logging to APIClient.swift:

```swift
func getFlights() async throws -> [Flight] {
    let url = URL(string: "\(baseURL)/api/flights")!
    print("📡 Fetching flights from: \(url)")

    let (data, response) = try await session.data(from: url)
    print("✅ Response: \((response as? HTTPURLResponse)?.statusCode ?? 0)")

    return try JSONDecoder().decode([Flight].self, from: data)
}
```

## Rollback if Needed

If production has issues:

### Quick Rollback
```swift
// Configuration.swift
static let current: Environment = .development  // Back to local
```

Rebuild and run.

### DigitalOcean Rollback

1. Apps → Your App → **Settings**
2. **App Spec** → **View Spec**
3. Previous commit should auto-deploy
4. Or manually trigger rebuild from specific commit

## Next Steps

1. ✅ App connected to production
2. ✅ All features tested
3. ✅ Sample data initialized
4. 🚀 **Ready for TestFlight!**

See `TESTFLIGHT_DEPLOYMENT_GUIDE.md` for next steps.

---

**Congratulations!** Your iOS app is now running on production DigitalOcean backend! 🎉

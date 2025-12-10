# TestFlight Deployment Guide for Manajet iOS

Complete step-by-step guide to deploy your iOS app to TestFlight for beta testing.

## Prerequisites

- ✅ **Apple Developer Account** ($99/year)
  - Enroll at: https://developer.apple.com/programs/
  - Approval takes 24-48 hours

- ✅ **Mac with Xcode 15+**
- ✅ **App ID configured** (done during project setup)
- ✅ **Backend API deployed** with HTTPS (required for production)

## Part 1: Initial Xcode Setup

### Step 1: Configure Signing & Capabilities

1. Open your Manajet project in Xcode
2. Select **Manajet** target in left sidebar
3. Go to **Signing & Capabilities** tab
4. Under "Signing":
   - ✅ Check "Automatically manage signing"
   - Team: Select your Apple Developer team
   - Bundle Identifier: Should be unique (e.g., `com.yourcompany.manajet`)

### Step 2: Set Deployment Target

1. In **General** tab:
   - Deployment Info → iOS: **17.0** (or lower if you want to support older devices)
   - Supported Destinations: iPhone (recommended)
   - Device Orientation: Portrait (recommended for consistency)

### Step 3: Update App Icons

1. In **Assets.xcassets**:
   - Click AppIcon
   - Drag in icon images for all required sizes
   - Xcode will show which sizes are needed
   - Use https://appicon.co to generate all sizes from one image

### Step 4: Configure Production Backend

Update `Services/APIClient.swift`:

```swift
// PRODUCTION - Use your deployed backend URL
private let baseURL = "https://your-backend-url.com"

// Make sure this is HTTPS! TestFlight requires secure connections
```

Remove development-only settings from `Info.plist`:
- Delete the `NSAppTransportSecurity` key (was for local HTTP testing)

### Step 5: Build for Release

1. Select target device: **Any iOS Device (arm64)**
2. Product → Scheme → Edit Scheme
3. Set Run configuration to **Release**
4. Product → Clean Build Folder (⌘ + Shift + K)
5. Product → Archive (wait for build to complete)

## Part 2: App Store Connect Configuration

### Step 1: Create App Record

1. Go to https://appstoreconnect.apple.com
2. Click **Apps** → **+** → **New App**
3. Configure:
   - **Platforms:** iOS
   - **Name:** Manajet
   - **Primary Language:** English (U.S.)
   - **Bundle ID:** Select your bundle identifier
   - **SKU:** manajet-ios (unique identifier)
   - **User Access:** Full Access
4. Click **Create**

### Step 2: Complete App Information

1. In your app, go to **App Information** tab:
   - **Category:** Business (primary)
   - **Content Rights:** Check if you own all rights
   - **Age Rating:** Configure appropriately

2. Go to **Pricing and Availability**:
   - **Price:** Free (or set price)
   - **Availability:** Your desired regions

### Step 3: Prepare Test Information

In **TestFlight** tab → **Test Information**:

1. **Beta App Description:**
   ```
   Manajet is a private jet management system for scheduling flights,
   managing passengers, and coordinating crew operations.

   Features:
   - Schedule flights with smart airport search
   - Flexible departure/arrival time selection
   - Flight approval workflow for pilots
   - Real-time dashboard and statistics
   ```

2. **Beta App Review Information:**
   - **Email:** your-email@example.com
   - **Phone Number:** Your phone
   - **Sign-In Required:** YES
   - **Username:** johnsmith (or your test account)
   - **Password:** customer123 (or your test password)
   - **Notes:**
     ```
     Test credentials:
     - Customer: johnsmith / customer123
     - Pilot: pilot_mike / crew123
     - Admin: admin / admin123

     The app connects to our backend API for all data.
     ```

3. **Feedback Email:** Your email for tester feedback

## Part 3: Upload Build to TestFlight

### Step 1: Archive Your App

1. In Xcode: Window → Organizer (or ⌘ + Shift + Option + O)
2. Select your latest archive
3. Click **Distribute App**

### Step 2: Distribution Process

1. **Select distribution method:** App Store Connect
2. **Select destination:** Upload
3. **App Store Connect distribution options:**
   - ✅ Upload your app's symbols
   - ✅ Manage version and build number (Xcode can auto-increment)
4. **Distribution certificate:** Automatically manage signing
5. Review summary
6. Click **Upload**
7. Wait for upload to complete (can take 5-30 minutes)

### Step 3: Processing in App Store Connect

1. Go to App Store Connect → Your App → TestFlight
2. Wait for "Processing" to complete (10-60 minutes)
3. You'll receive email when build is ready
4. Build will appear under "Builds" section

### Step 4: Submit for Review (First Time Only)

1. When build appears, it may say "Missing Compliance"
2. Click **Manage** next to the warning
3. **Export Compliance:**
   - "Does your app use encryption?" → **NO** (unless you added custom encryption)
   - If YES, you'll need export documentation
4. Build status changes to "Ready to Submit"

## Part 4: Add Beta Testers

### Internal Testing (Up to 100 testers, no review required)

1. In TestFlight → **Internal Testing**
2. Click **+** → **Add Group** or use "App Store Connect Users"
3. Add testers:
   - Users must have App Store Connect accounts
   - Add via email in **Users and Access** section
4. Select your build
5. Testers receive invitation immediately

### External Testing (Unlimited testers, requires review)

1. In TestFlight → **External Testing**
2. Click **+** → Create new group (e.g., "Beta Testers")
3. **Add Testers:**
   - Click **+** next to testers
   - Enter email addresses
   - Testers DON'T need App Store Connect access
4. **Enable Automatic Distribution** (optional):
   - New builds auto-deploy to testers
5. **Select Build** and click **Submit for Review**
6. **Beta App Review:**
   - First submission takes 24-48 hours
   - Future builds: 12-24 hours
   - Apple reviews for TestFlight compliance

## Part 5: Testers Install App

### Tester Instructions

Send these steps to your testers:

1. **Install TestFlight:**
   - Download from App Store: https://apps.apple.com/app/testflight/id899247664

2. **Accept Invitation:**
   - Check email for "You're invited to test Manajet"
   - Click "View in TestFlight" or "Start Testing"
   - Opens TestFlight app

3. **Install Manajet:**
   - Tap "Install" in TestFlight
   - Wait for download
   - App appears on home screen

4. **Provide Feedback:**
   - Open TestFlight
   - Select Manajet
   - Tap "Send Beta Feedback"
   - Describe issues or suggestions
   - Can attach screenshots

## Part 6: Update & Iterate

### Releasing Updates

1. Make code changes in Xcode
2. Increment build number:
   - Project Settings → Build → **Versioning**
   - Current Project Version: increment (e.g., 2, 3, 4...)
   - Marketing Version: 1.0 (only change for major releases)
3. Archive and upload (same process as before)
4. In App Store Connect:
   - Select new build for tester group
   - If "Automatic Distribution" enabled, testers get it automatically

### Version Numbering

- **Marketing Version:** What users see (1.0, 1.1, 2.0)
  - Change for feature releases
- **Build Number:** Internal tracking (1, 2, 3, 4...)
  - Increment for every upload
  - Must always increase

## Part 7: Monitoring & Analytics

### View TestFlight Metrics

1. App Store Connect → Your App → TestFlight
2. **Testers & Groups:**
   - See who installed
   - Installation rate
   - Active testers

3. **Crashes:**
   - View crash reports
   - Stack traces for debugging
   - OS versions affected

4. **Feedback:**
   - Read tester comments
   - View screenshots
   - Respond to testers

### Xcode Crash Reports

1. Window → Organizer
2. **Crashes** tab
3. Select your app
4. View detailed crash logs with symbolication

## Troubleshooting

### Build Fails to Upload

**Error: "Couldn't communicate with a helper application"**
- Restart Xcode
- Restart Mac
- Clear Derived Data: Xcode → Preferences → Locations → Derived Data → Delete

**Error: "Invalid Bundle"**
- Check Bundle Identifier matches App Store Connect
- Verify signing certificates are valid
- Clean build folder and rebuild

### Build Stuck in "Processing"

- Normal processing: 10-60 minutes
- If > 2 hours: Contact Apple Support
- Check https://developer.apple.com/system-status/

### Testers Can't Install

- Verify email invitation was sent
- Check tester's device iOS version meets minimum
- Ensure tester has TestFlight app installed
- Resend invitation from App Store Connect

### "Export Compliance" Issues

- For apps without custom encryption: Select "NO"
- If using HTTPS only (normal web communication): Select "NO"
- Custom encryption requires filing exemption with US government

### Certificate/Provisioning Issues

1. Xcode → Preferences → Accounts
2. Select your team
3. Click "Download Manual Profiles"
4. Try archiving again

## Best Practices

### 1. Testing Before Upload

- Test on real device, not just simulator
- Test all user roles (customer, pilot, admin)
- Verify backend connectivity
- Check all features work with production backend

### 2. Release Notes

Include in TestFlight update notes:
```
Version 1.0 Build 2

What's New:
- Fixed login issue
- Improved airport search
- Better error messages

Known Issues:
- Calendar view may be slow with many flights
```

### 3. Staged Rollout

1. Start with small internal group
2. Fix critical bugs
3. Expand to larger external group
4. Monitor feedback and crashes
5. Only then submit to App Store

### 4. Communication

- Set up TestFlight feedback email
- Create Slack/Discord for testers
- Respond to feedback quickly
- Document known issues

## Moving to Production App Store

When ready for public release:

1. Complete all App Store metadata:
   - Screenshots (required for all device sizes)
   - App Preview videos (optional)
   - Description, keywords
   - Privacy policy URL
   - Support URL

2. Select build for release

3. Submit for App Review:
   - Stricter than TestFlight review
   - Takes 1-7 days
   - Provide detailed test instructions

4. Upon approval:
   - Choose manual or automatic release
   - App goes live on App Store

## Resources

- **Apple Developer:** https://developer.apple.com
- **App Store Connect:** https://appstoreconnect.apple.com
- **TestFlight Documentation:** https://developer.apple.com/testflight/
- **App Store Review Guidelines:** https://developer.apple.com/app-store/review/guidelines/
- **Human Interface Guidelines:** https://developer.apple.com/design/human-interface-guidelines/

## Support

For questions:
- Apple Developer Forums: https://developer.apple.com/forums/
- Stack Overflow: Tag `ios` and `testflight`
- Apple Developer Support: https://developer.apple.com/support/

---

**Congratulations!** You're now ready to deploy Manajet to TestFlight and start beta testing. Good luck with your app launch!

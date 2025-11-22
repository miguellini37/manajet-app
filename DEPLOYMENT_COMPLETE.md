# 🚀 Manajet Deployment Guide - Complete Workflow

## What You Have Now

✅ **Backend Code** - Ready for DigitalOcean
✅ **iOS App** - Ready for TestFlight
✅ **All Features** - Approvals, Location Search, Flexible Time
✅ **GitHub** - Code pushed and ready
✅ **Configuration** - Easy environment switching

## Deployment Workflow (30 minutes total)

### Phase 1: Deploy Backend to DigitalOcean (10 minutes)

**Follow:** `DIGITALOCEAN_DEPLOY_NOW.md`

**Quick Steps:**
1. Go to https://cloud.digitalocean.com/apps
2. Create App → Connect GitHub repo: `miguellini37/manajet-app`
3. Add SECRET_KEY environment variable
4. Deploy and wait 5-10 minutes
5. Get your URL: `https://manajet-xxxxx.ondigitalocean.app`

**Result:** Backend running on production with HTTPS ✅

### Phase 2: Update iOS App for Production (5 minutes)

**Follow:** `UPDATE_IOS_FOR_PRODUCTION.md`

**Quick Steps:**
1. Open `Manajet-iOS/Manajet/Utils/Configuration.swift`
2. Update production URL (line ~22):
   ```swift
   return "https://manajet-xxxxx.ondigitalocean.app"
   ```
3. Save and rebuild in Xcode
4. Test login and features

**Result:** iOS app connected to production ✅

### Phase 3: Initialize Production Data (2 minutes)

**In DigitalOcean Console:**
```bash
python setup_initial_data.py
```

**Or via web interface:**
1. Open your app URL in browser
2. Login as admin/admin123
3. Use web UI to create test data

**Result:** Production has sample data ✅

### Phase 4: Deploy to TestFlight (15 minutes)

**Follow:** `Manajet-iOS/TESTFLIGHT_DEPLOYMENT_GUIDE.md`

**Quick Steps:**
1. In Xcode: Product → Archive
2. Distribute → App Store Connect
3. Upload build
4. Wait for processing (~30 minutes)
5. Add beta testers
6. Testers download via TestFlight app

**Result:** App available for beta testing ✅

## File Structure

```
manajet-app/
├── Backend (Flask)
│   ├── web_app.py                          # Main Flask app with mobile APIs
│   ├── jet_manager.py                      # Business logic + approvals
│   ├── airport_utils.py                    # Airport search & duration
│   ├── airports_data.json                  # 51 US airports
│   ├── Dockerfile                          # Production container
│   ├── requirements.txt                    # Python dependencies
│   └── .do/app.yaml                        # DigitalOcean config
│
├── iOS App (SwiftUI)
│   └── Manajet-iOS/
│       ├── Manajet/
│       │   ├── Models/Models.swift         # Data models
│       │   ├── Services/APIClient.swift    # API communication
│       │   ├── Utils/Configuration.swift   # Environment config ⭐
│       │   ├── Views/
│       │   │   ├── LoginView.swift         # Auth
│       │   │   ├── DashboardView.swift     # Main dashboard
│       │   │   ├── FlightScheduleView.swift # Booking with search
│       │   │   └── ApprovalsView.swift     # Pilot workflow
│       │   └── ManajetApp.swift            # Entry point
│       ├── README.md                       # iOS setup guide
│       ├── QUICK_START.md                  # 15-min quick start
│       └── TESTFLIGHT_DEPLOYMENT_GUIDE.md  # TestFlight steps
│
└── Deployment Guides
    ├── DIGITALOCEAN_DEPLOY_NOW.md          # Deploy backend
    ├── UPDATE_IOS_FOR_PRODUCTION.md        # Configure iOS
    └── DEPLOYMENT_COMPLETE.md              # This file
```

## Environment Configuration (iOS)

The iOS app now has a smart configuration system!

### Location: `Manajet-iOS/Manajet/Utils/Configuration.swift`

```swift
// Switch environments by changing this ONE line:
static let current: Environment = .production  // or .development
```

### Development (Local Testing)
```swift
static let current: Environment = .development

// Uses: http://192.168.1.100:5000
// Update line 19 with your Mac's IP
```

### Production (DigitalOcean)
```swift
static let current: Environment = .production

// Uses: https://manajet-xxxxx.ondigitalocean.app
// Update line 24 with your DigitalOcean URL
```

### Benefits
- ✅ One line to switch environments
- ✅ No code changes in APIClient.swift
- ✅ Environment badge shown in app
- ✅ Debug logging in development
- ✅ Ready for TestFlight builds

## Feature Summary

### Backend Features
- ✈️ **Flight Scheduling** with airport search
- 👥 **Passenger Management** with inline add
- 👨‍✈️ **Crew Management** with pilot validation
- ✅ **Approval Workflow** for customer flights
- 📊 **Dashboard** with real-time stats
- 🔐 **Role-Based Access** (admin, customer, crew, mechanic)
- 📧 **Session Management** with cookies
- 🌐 **Mobile API** with 7 new endpoints
- 🔍 **Airport Database** with 51 major US airports
- ⏱️ **Flight Duration** calculation
- 📅 **Calendar View** for flight scheduling

### iOS App Features
- 📱 **Native iOS Design** with SwiftUI
- 🎨 **Modern UI** with gradients & animations
- 🔐 **Secure Auth** with session cookies
- 🔍 **Location Search** - type city names
- ⏰ **Flexible Time** - "Depart at" OR "Arrive by"
- ✈️ **Auto Duration** calculation
- ✅ **Pilot Approvals** with notifications
- 🔔 **Badge Alerts** for pending approvals
- 👥 **Inline Add** passengers
- 📊 **Real-time Stats** dashboard
- 🔄 **Pull-to-Refresh** on all lists
- ⚙️ **Environment Switching** dev ↔ prod

## Testing Checklist

### Backend (Web Browser)
```
URL: https://manajet-xxxxx.ondigitalocean.app

Test:
□ Login page loads
□ Admin login works (admin/admin123)
□ Dashboard shows stats
□ Create flight
□ View passengers
□ Approve flights (as pilot)
```

### iOS App (Simulator/Device)
```
Test as Customer:
□ Login (johnsmith/customer123)
□ Dashboard loads with stats
□ Search airports (try "Los Angeles")
□ Schedule flight with "Arrive by"
□ Add new passenger inline
□ See "Pending Approval" status
□ Logout

Test as Pilot:
□ Login (pilot_mike/crew123)
□ See notification badge
□ Open Approvals tab
□ Review flight details
□ Approve flight
□ Verify badge updates
```

## Production URLs

**Backend (after deployment):**
```
Production: https://manajet-xxxxx.ondigitalocean.app
Web Login: https://manajet-xxxxx.ondigitalocean.app/login
API Docs: https://manajet-xxxxx.ondigitalocean.app/api
```

**iOS App:**
- Development: Xcode simulator
- TestFlight: Beta testers via TestFlight app
- App Store: Coming soon

## Costs Breakdown

### DigitalOcean App Platform
- **$5/month** - Basic (good for testing)
  - 512 MB RAM
  - 1 vCPU
  - 40 GB bandwidth

- **$12/month** - Professional (recommended)
  - 1 GB RAM
  - 1 vCPU
  - 100 GB bandwidth
  - Better performance

### Apple Developer
- **$99/year** - Required for TestFlight + App Store
  - TestFlight beta testing
  - App Store publishing
  - Push notifications
  - CloudKit storage

### Total Monthly Cost
- **Minimum:** $5/mo + $8.25/mo (Apple) = ~$13/month
- **Recommended:** $12/mo + $8.25/mo = ~$20/month

## Monitoring & Maintenance

### DigitalOcean Dashboard
```
Apps → Your App → Insights
- CPU usage
- Memory usage
- Request count
- Error rates
- Response times
```

### Logs
```
Apps → Your App → Runtime Logs
- Real-time application logs
- Error stack traces
- API request logs
- Python print statements
```

### Alerts
```
Apps → Your App → Settings → Alerts
- App down notifications
- High CPU/memory alerts
- Error rate spikes
```

### Auto-Deploy
With GitHub integration:
```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin master

# DigitalOcean automatically:
# 1. Detects push
# 2. Builds new image
# 3. Deploys update
# 4. Zero downtime
```

## Troubleshooting Quick Reference

### Backend Issues

**Build fails:**
```
Check: Runtime Logs for Python errors
Fix: Verify requirements.txt, check Dockerfile
```

**500 errors:**
```
Check: Runtime Logs for stack trace
Fix: SECRET_KEY set? All dependencies installed?
```

**Can't access app:**
```
Check: Deployment complete? SSL active?
Fix: Wait 5 min for SSL, check URL is correct
```

### iOS Issues

**Can't connect:**
```
Check: Configuration.swift has correct URL
Fix: Update production URL, rebuild
```

**SSL errors:**
```
Check: Using https:// not http://
Fix: Remove NSAppTransportSecurity from Info.plist
```

**Login fails:**
```
Check: Backend has data initialized
Fix: Run setup_initial_data.py on production
```

## Support Resources

### DigitalOcean
- Dashboard: https://cloud.digitalocean.com/apps
- Docs: https://docs.digitalocean.com/products/app-platform/
- Support: https://cloud.digitalocean.com/support/tickets
- Community: https://www.digitalocean.com/community/

### Apple Developer
- TestFlight: https://developer.apple.com/testflight/
- App Store Connect: https://appstoreconnect.apple.com
- Documentation: https://developer.apple.com/documentation/
- Support: https://developer.apple.com/support/

### Project Documentation
- Backend API: See `web_app.py` docstrings
- iOS Setup: `Manajet-iOS/README.md`
- Quick Start: `Manajet-iOS/QUICK_START.md`
- TestFlight: `Manajet-iOS/TESTFLIGHT_DEPLOYMENT_GUIDE.md`

## Next Steps After Deployment

### Immediate (Today)
1. ✅ Deploy backend to DigitalOcean
2. ✅ Update iOS app configuration
3. ✅ Test all features
4. ✅ Initialize production data

### This Week
1. 📱 Submit to TestFlight
2. 👥 Invite 5-10 beta testers
3. 🐛 Fix bugs from feedback
4. 📊 Monitor usage and performance

### This Month
1. 🎨 Add app screenshots
2. 📝 Write App Store description
3. 🚀 Submit to App Store
4. 🌐 Set up custom domain (optional)

### Future Enhancements
- 📧 Email notifications for approvals
- 📱 Push notifications
- 📍 Real-time flight tracking
- 💳 Payment integration
- 📊 Advanced analytics
- 🌍 International airports
- 📅 Advanced calendar features
- 🖼️ Photo uploads

## Congratulations! 🎉

You now have:
- ✅ Production backend on DigitalOcean
- ✅ Native iOS app ready for TestFlight
- ✅ Complete approval workflow
- ✅ Location-based flight scheduling
- ✅ Professional deployment setup
- ✅ Easy environment switching
- ✅ Comprehensive documentation

**Your Manajet app is production-ready!**

---

**Need help?** Check the specific guides:
- Backend deployment → `DIGITALOCEAN_DEPLOY_NOW.md`
- iOS configuration → `UPDATE_IOS_FOR_PRODUCTION.md`
- TestFlight submission → `Manajet-iOS/TESTFLIGHT_DEPLOYMENT_GUIDE.md`

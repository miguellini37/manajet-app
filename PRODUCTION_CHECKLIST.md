# Production Deployment Checklist for pr.manajet.io

Use this checklist to ensure your production deployment is complete and secure.

## Pre-Deployment

### 1. Code Preparation
- [ ] All features tested locally
- [ ] Code committed to git repository
- [ ] No console.log or debug print statements in production code
- [ ] Error handling implemented for critical functions
- [ ] Database schema finalized

### 2. Environment Configuration
- [ ] Create production `.env` file (do not commit to git!)
- [ ] Generate new SECRET_KEY for production:
  ```python
  python -c 'import secrets; print(secrets.token_hex(32))'
  ```
- [ ] Set DEBUG=False
- [ ] Set SESSION_COOKIE_SECURE=True
- [ ] Configure Apple OAuth credentials

**Production `.env` template:**
```env
SECRET_KEY=your-new-production-secret-key-here
DEBUG=False
SESSION_COOKIE_SECURE=True
PERMANENT_SESSION_LIFETIME=3600
APPLE_CLIENT_ID=io.manajet.connect10
APPLE_CLIENT_SECRET=your_generated_jwt_token_here
```

## DNS Setup

### 3. Configure DNS
- [ ] Choose DNS provider (Cloudflare recommended)
- [ ] Add CNAME record: `pr.manajet.io` → Railway domain
- [ ] Verify DNS propagation with `nslookup pr.manajet.io`
- [ ] Wait 15-30 minutes for global propagation

### 4. SSL Certificate
- [ ] Verify HTTPS is working on pr.manajet.io
- [ ] Check SSL certificate validity (lock icon in browser)
- [ ] Ensure automatic HTTPS redirect is enabled

## Railway Deployment

### 5. Deploy to Railway
```bash
# Login
railway login

# Link project or create new
railway link
# OR
railway init

# Set environment variables
railway variables set SECRET_KEY="your-production-secret"
railway variables set DEBUG="False"
railway variables set SESSION_COOKIE_SECURE="True"
railway variables set APPLE_CLIENT_ID="io.manajet.connect10"
railway variables set APPLE_CLIENT_SECRET="your-jwt-token"

# Deploy
railway up

# Add custom domain
railway domain pr.manajet.io

# Check deployment
railway logs
```

### 6. Verify Deployment
- [ ] App loads at https://pr.manajet.io
- [ ] Login page displays correctly
- [ ] Database is accessible (create test user)
- [ ] Static files load correctly
- [ ] No console errors in browser DevTools

## Apple Sign In Configuration

### 7. Apple Developer Portal
- [ ] Navigate to Service ID: `io.manajet.connect10`
- [ ] Configure domains:
  - Add domain: `pr.manajet.io`
  - Add return URL: `https://pr.manajet.io/auth/apple/callback`
- [ ] Save configuration
- [ ] Wait 5-10 minutes for changes to propagate

### 8. Test Apple OAuth
- [ ] Visit https://pr.manajet.io/login
- [ ] Click "Sign in with Apple"
- [ ] Complete Apple authentication
- [ ] Verify redirect back to app
- [ ] Check user is logged in
- [ ] Verify user account created correctly

## Security Hardening

### 9. Security Checks
- [ ] SECRET_KEY is unique and not in git repository
- [ ] DEBUG=False in production
- [ ] SESSION_COOKIE_SECURE=True (requires HTTPS)
- [ ] SESSION_COOKIE_HTTPONLY=True
- [ ] No hardcoded passwords in code
- [ ] API keys and secrets in environment variables only
- [ ] `.env` file is in `.gitignore`
- [ ] CORS configured correctly (if needed)

### 10. Data Protection
- [ ] Database backups configured
- [ ] User passwords properly hashed
- [ ] Sensitive data encrypted
- [ ] Input validation on all forms
- [ ] SQL injection prevention (using ORM)
- [ ] XSS protection enabled

## Performance Optimization

### 11. Performance
- [ ] Gunicorn configured with appropriate workers
- [ ] Static files served efficiently
- [ ] Database queries optimized
- [ ] Caching implemented where appropriate
- [ ] CDN configured (if using Cloudflare)

### 12. Monitoring
- [ ] Set up error logging
- [ ] Configure uptime monitoring
- [ ] Set up performance monitoring
- [ ] Configure alerting for critical errors

## Post-Deployment

### 13. Testing
- [ ] Test all critical user flows
- [ ] Test regular login
- [ ] Test Apple Sign In
- [ ] Test flight creation
- [ ] Test passenger management
- [ ] Test PDF generation
- [ ] Test on mobile devices
- [ ] Test on different browsers

### 14. Documentation
- [ ] Update README with production URL
- [ ] Document deployment process
- [ ] Create runbook for common issues
- [ ] Document environment variables
- [ ] Update API documentation (if applicable)

### 15. Maintenance Plan
- [ ] Schedule for dependency updates
- [ ] Plan for database migrations
- [ ] Backup and recovery procedures
- [ ] SSL certificate renewal (automatic with Railway)
- [ ] Apple Client Secret renewal (every 180 days)

## Rollback Plan

### 16. Emergency Procedures
- [ ] Document rollback procedure
- [ ] Keep previous deployment accessible
- [ ] Have database backup restoration procedure
- [ ] Know how to revert to previous git commit

**Quick Rollback:**
```bash
# Revert to previous commit
git log  # Find previous commit hash
git checkout <previous-commit-hash>
railway up
```

## Launch Checklist

### Final Steps Before Going Live
1. [ ] All items above completed
2. [ ] Stakeholders notified of launch
3. [ ] Support team briefed
4. [ ] Monitoring dashboards active
5. [ ] Backup procedures verified
6. [ ] Emergency contacts documented

### Post-Launch Monitoring (First 24 Hours)
- [ ] Monitor error logs continuously
- [ ] Check performance metrics
- [ ] Monitor user sign-ups
- [ ] Verify Apple OAuth success rate
- [ ] Check database performance
- [ ] Monitor server resources

## Quick Commands Reference

### Railway
```bash
railway logs                    # View logs
railway logs --follow          # Stream logs
railway variables              # List variables
railway status                 # Check deployment status
railway open                   # Open in browser
```

### DNS Verification
```bash
nslookup pr.manajet.io         # Check DNS
dig pr.manajet.io              # Detailed DNS info
curl -I https://pr.manajet.io  # Check HTTP headers
```

### Git
```bash
git status                     # Check current status
git add .                      # Stage all changes
git commit -m "message"        # Commit
git push origin main           # Push to remote
```

## Support Contacts

- **Railway Support**: https://railway.app/help
- **Apple Developer**: https://developer.apple.com/contact/
- **DNS Provider**: [Your provider support]

## Success Criteria

Production deployment is successful when:
- ✅ pr.manajet.io loads with valid HTTPS
- ✅ Users can log in with username/password
- ✅ Users can sign in with Apple
- ✅ All features work as in development
- ✅ No errors in production logs
- ✅ Performance is acceptable
- ✅ Mobile responsiveness verified

## Completion

Date Completed: _______________
Deployed By: __________________
Verified By: __________________

Notes:
_________________________________
_________________________________
_________________________________

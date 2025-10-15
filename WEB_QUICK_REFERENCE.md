# 🚀 Web App Quick Reference

## One-Command Start (Windows)
```bash
setup_web.bat
```

## Manual Start
```bash
python generate_templates.py    # Once only
pip install flask               # Once only
python web_app.py              # Every time
```

Open: **http://localhost:5000**

---

## 🌐 Deploy to Internet (FREE)

### Render.com (Easiest - 10 min)
1. Push code to GitHub
2. Go to render.com, sign up
3. New Web Service → Connect GitHub
4. Build: `pip install -r requirements.txt`
5. Start: `gunicorn web_app:app`
6. Deploy!

**URL:** `https://yourapp.onrender.com`

---

## 📁 Files You Need

✅ Already created:
- `web_app.py` - Main Flask app
- `jet_manager.py` - Business logic
- `templates/base.html` - Layout
- `templates/dashboard.html` - Homepage
- `generate_templates.py` - Create other pages
- `requirements.txt` - Dependencies
- `setup_web.bat` - One-command start

🔧 To create remaining templates:
```bash
python generate_templates.py
```

---

## 🎯 What Works

✅ Dashboard with stats
✅ Add/view passengers
✅ Add/view jets
✅ Schedule flights
✅ Schedule maintenance
✅ Update statuses
✅ Auto status sync
✅ Mobile responsive
✅ Professional design

---

## 🔧 Troubleshooting

**Templates not found?**
```bash
python generate_templates.py
```

**Flask not installed?**
```bash
pip install flask
```

**Port already in use?**
Edit `web_app.py`, change:
```python
app.run(debug=True, port=5001)  # Changed from 5000
```

---

## 📊 URLs

- Dashboard: `/`
- Passengers: `/passengers`
- Jets: `/jets`
- Flights: `/flights`
- Maintenance: `/maintenance`
- API Stats: `/api/stats`

---

## 🎨 Customize

**Colors:** Edit `templates/base.html` styles
**Logo:** Change ✈️ in header
**Routes:** Add to `web_app.py`

---

## 🔒 Security (Before Going Live)

1. Change secret key in `web_app.py`
2. Add authentication
3. Use HTTPS
4. Upgrade database to PostgreSQL
5. Add rate limiting

---

## 💰 Cost Comparison

| Host | Free Tier | Paid |
|------|-----------|------|
| Render | ✅ (sleeps) | $7/mo |
| Heroku | ❌ | $7/mo |
| PythonAnywhere | ✅ (limited) | $5/mo |
| Fly.io | ✅ (credit) | Usage |

---

## ⚡ Performance Tips

Production setup:
```bash
gunicorn --workers 4 web_app:app
```

---

## 📞 Help Resources

- Full Guide: `DEPLOYMENT_GUIDE.md`
- Quick Start: `QUICKSTART_WEB.md`
- Summary: `WEB_DEPLOYMENT_SUMMARY.md`
- Flask Docs: https://flask.palletsprojects.com/

---

## ✅ Deployment Checklist

- [ ] Templates generated
- [ ] Flask installed
- [ ] Tested locally
- [ ] Code on GitHub
- [ ] Deployed to host
- [ ] Custom domain (optional)
- [ ] Authentication added
- [ ] Database upgraded
- [ ] Backups configured

---

**Ready to deploy? Run `setup_web.bat` now!**

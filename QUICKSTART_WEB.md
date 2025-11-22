# Quick Start: Deploy Your Jet Manager as a Web App

## 🚀 Get Running in 5 Minutes

### Step 1: Install Dependencies

```bash
pip install flask
```

### Step 2: Complete the Templates

I've created the basic structure. You need to create these template files in the `templates/` folder:

**Minimal templates to get started:**

#### templates/passengers.html
```html
{% extends "base.html" %}
{% block content %}
<h1>Passengers</h1>
<a href="{{ url_for('add_passenger') }}" class="btn btn-primary">Add New Passenger</a>
<table>
    <thead>
        <tr>
            <th>ID</th><th>Name</th><th>Passport</th><th>Nationality</th><th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for passenger in passengers %}
        <tr>
            <td>{{ passenger.passenger_id }}</td>
            <td>{{ passenger.name }}</td>
            <td>{{ passenger.passport_number }}</td>
            <td>{{ passenger.nationality }}</td>
            <td><a href="{{ url_for('view_passenger', passenger_id=passenger.passenger_id) }}">View</a></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

#### templates/passenger_form.html
```html
{% extends "base.html" %}
{% block content %}
<h1>Add Passenger</h1>
<form method="POST" class="card">
    <div class="form-group">
        <label>Full Name</label>
        <input type="text" name="name" required>
    </div>
    <div class="form-group">
        <label>Passport Number</label>
        <input type="text" name="passport_number" required>
    </div>
    <div class="form-group">
        <label>Nationality</label>
        <input type="text" name="nationality" required>
    </div>
    <div class="form-group">
        <label>Passport Expiry (YYYY-MM-DD)</label>
        <input type="date" name="passport_expiry" required>
    </div>
    <div class="form-group">
        <label>Contact</label>
        <input type="text" name="contact" required>
    </div>
    <button type="submit" class="btn btn-success">Add Passenger</button>
    <a href="{{ url_for('passengers') }}" class="btn btn-secondary">Cancel</a>
</form>
{% endblock %}
```

**Do the same for jets, flights, and maintenance!**

### Step 3: Run Locally

```bash
python web_app.py
```

Open browser to: **http://localhost:5000**

---

## 🌐 Deploy to Internet (FREE)

### Option A: Render.com (Easiest - Recommended)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_URL
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Sign up (free)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Configure:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn web_app:app`
   - Click "Create Web Service"
   - Your app will be live at: `https://your-app.onrender.com`

**Time:** 10 minutes
**Cost:** FREE (with sleep after inactivity)

---

### Option B: Heroku

```bash
# Install Heroku CLI
# Then:
heroku login
heroku create your-jet-manager
git push heroku main
heroku open
```

**Time:** 15 minutes
**Cost:** $7/month (no free tier anymore)

---

### Option C: PythonAnywhere

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Go to "Web" tab
3. "Add a new web app"
4. Choose Flask
5. Upload your files via "Files" tab
6. Edit WSGI configuration to point to your app
7. Reload web app

**Time:** 20 minutes
**Cost:** FREE tier available

---

## 📱 Make it Mobile-Friendly

The CSS I provided is already responsive! Test on mobile:
- Chrome: Press F12 → Toggle device toolbar
- Safari: Develop → Enter Responsive Design Mode

---

## 🔐 Add Security (IMPORTANT for production)

### Quick Security Setup:

```python
# In web_app.py, add at the top:
import os
from flask_login import LoginManager, login_required, UserMixin

# Change secret key
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-in-production')

# Add login requirement to all routes
@app.route('/passengers')
@login_required  # Add this decorator
def passengers():
    # ... existing code
```

### Environment Variables:

Create `.env` file:
```
SECRET_KEY=your-random-secret-key-here
DATABASE_URL=sqlite:///jet_schedule.db
```

---

## 🗄️ Upgrade Database (When You Need It)

### SQLite (Easy upgrade):

```python
# Replace in jet_manager.py:
import sqlite3
import json

class JetScheduleManager:
    def __init__(self, db_path="jet_schedule.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS passengers (
                passenger_id TEXT PRIMARY KEY,
                name TEXT,
                passport_number TEXT,
                nationality TEXT,
                passport_expiry TEXT,
                contact TEXT
            )
        ''')
        self.conn.commit()
```

---

## 📊 Monitor Your App

### Free Monitoring Tools:

1. **UptimeRobot** - Monitor uptime (free)
2. **Google Analytics** - Track usage (free)
3. **Sentry** - Error tracking (free tier)
4. **LogDNA** - Log management (free tier)

---

## 🎨 Customize Design

The app uses inline CSS for simplicity. To customize:

1. **Create static/css/custom.css**
2. **Link in base.html:**
   ```html
   <link rel="stylesheet" href="{{ url_for('static', filename='css/custom.css') }}">
   ```

3. **Add your styles**

---

## ⚡ Performance Tips

### For Production:

1. **Use a production WSGI server:**
   ```bash
   gunicorn --workers 4 --bind 0.0.0.0:8000 web_app:app
   ```

2. **Enable caching:**
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'simple'})
   ```

3. **Compress responses:**
   ```python
   from flask_compress import Compress
   Compress(app)
   ```

4. **Use CDN for static files**

---

## 🐛 Troubleshooting

### App won't start?
```bash
# Check Python version
python --version  # Should be 3.7+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### "Template not found" error?
- Make sure templates/ folder exists
- Check template names match exactly (case-sensitive)

### Data not saving?
- Check file permissions in deployment directory
- Consider upgrading to SQLite database

---

## 📞 Next Steps

1. ✅ Complete all HTML templates (copy pattern from passenger examples)
2. ✅ Test locally
3. ✅ Deploy to Render.com (free)
4. ✅ Add authentication (Flask-Login)
5. ✅ Upgrade to PostgreSQL when needed
6. ✅ Add custom domain (optional)

---

## 💡 Pro Tips

- **Start simple** - Get basic deployment working first
- **Test thoroughly** - Use all features before deploying
- **Backup data** - Download jet_schedule_data.json regularly
- **Monitor usage** - Watch logs for errors
- **Scale gradually** - Upgrade only when needed

---

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Render Deployment Guide](https://render.com/docs/deploy-flask)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/getting-started-with-python)

---

**Need help?** The deployment guide (DEPLOYMENT_GUIDE.md) has more detailed options!

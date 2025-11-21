# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

### Two-Layer Architecture
- **web_app.py**: Flask web application (presentation layer)
  - Routes and HTTP request handling
  - Authentication decorators (`@login_required`, `@role_required`)
  - Session management and user context
  - Template rendering with Jinja2
- **jet_manager.py**: Business logic and data models (domain layer)
  - All data classes: Customer, User, Passenger, Crew, Jet, Flight, Maintenance
  - JetScheduleManager singleton handles all CRUD operations
  - JSON-based persistence to `jet_schedule_data.json`

### Role-Based Access Control (RBAC)
The system has four user roles with different permissions:
- **admin**: Full access to all features including customer management
- **customer**: Can view/edit own aircraft and passengers only (filtered by `customer_id`)
- **crew**: Can view all data, schedule flights, manage maintenance
- **mechanic**: Can view all data, schedule flights, full maintenance access

Access control is enforced at two levels:
1. Backend routes use `@role_required('admin', 'customer')` decorators
2. Frontend templates conditionally show/hide UI elements based on `session.role`

Data filtering happens in `filter_by_customer()` helper function.

### Data Model Relationships
- **Customer** owns multiple **Jets** and **Passengers** (via `customer_id` foreign key)
- **User** links to Customer/Crew via `related_id` field
- **Flight** references Jet, Passengers (list), and Crew (list)
- **Maintenance** references Jet and includes conflict detection with flights

All models use string IDs with auto-generation (e.g., `P001`, `F001`, `M001`).

### Template System
- **Base template** (`templates/base.html`):
  - Contains modern CSS design system with CSS variables
  - Responsive navigation with mobile hamburger menu
  - Flash message handling
  - Role-based navigation items (e.g., Customers link only for admin)
- Templates use symlink to `C:\Users\MichaelSilver\AppData\Roaming\Microsoft\Windows\Templates`
- Custom styles in `static/css/custom.css` provide additional utilities and animations

## Development Commands

### Run Application
```bash
python web_app.py
```
App runs on `http://localhost:5000` with debug mode enabled by default.

### Initialize Sample Data
```bash
python setup_initial_data.py
```
Creates sample users (admin, customers, crew, mechanic) and test data. Default credentials:
- Admin: `admin` / `admin123`
- Customer: `johnsmith` / `customer123`
- Pilot: `pilot_mike` / `crew123`
- Mechanic: `mechanic_joe` / `mech123`

### Reset Database
```bash
# Delete existing data
rm jet_schedule_data.json
# Recreate with sample data
python setup_initial_data.py
```

### Generate Templates
```bash
python generate_templates.py
```
Regenerates HTML templates (if templates directory is missing or corrupted).

## Deployment

### Docker Deployment (Recommended)
Quick deploy using automated script:
```bash
# Windows
docker-deploy.bat

# Mac/Linux
./docker-deploy.sh
```

Or manually:
```bash
# Generate secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Create .env file from template and add your SECRET_KEY
cp .env.docker .env

# Build and run
docker-compose up -d

# Initialize sample data
docker-compose exec manajet python setup_initial_data.py
```

Access at `http://localhost:5000`

See `DOCKER_DEPLOYMENT.md` for comprehensive Docker guide.

### Railway Deployment
Quick deploy using automated script:
```bash
# Windows
deploy-to-railway.bat

# Mac/Linux
./deploy-to-railway.sh
```

Or manually:
```bash
railway login
railway init
railway variables set SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
railway variables set DEBUG="False"
railway variables set SESSION_COOKIE_SECURE="True"
railway up
railway domain
```

See `RAILWAY_DEPLOYMENT.md` for comprehensive Railway guide.

### Environment Variables
Required for production:
- `SECRET_KEY`: Flask session secret (use `secrets.token_hex(32)`)
- `DEBUG`: Set to `"False"` in production
- `SESSION_COOKIE_SECURE`: Set to `"True"` for HTTPS
- `PERMANENT_SESSION_LIFETIME`: Session timeout in seconds (default: 3600)

## Working with the Codebase

### Adding New Routes
1. Add route function in `web_app.py`
2. Apply appropriate decorators (`@login_required`, `@role_required`)
3. Use `get_current_user()` to get logged-in user context
4. Filter data with `filter_by_customer()` if needed
5. Create/update Jinja2 template in `templates/`

### Adding New Data Models
1. Define class in `jet_manager.py` with `to_dict()` and `from_dict()` methods
2. Add storage dictionary in `JetScheduleManager.__init__`
3. Implement CRUD methods in `JetScheduleManager`
4. Update `load_data()` and `save_data()` methods
5. Add corresponding routes in `web_app.py`

### Modifying UI/Styles
- **Global styles**: Edit CSS in `templates/base.html` within `<style>` tags
- **Additional styles**: Add to `static/css/custom.css`
- **Design system**: Uses CSS variables (`:root` in base.html)
  - Colors: `--primary`, `--secondary`, `--accent`, `--success`, `--warning`, `--danger`
  - Spacing: `--border-radius`, `--border-radius-lg`
  - Shadows: `--shadow-sm`, `--shadow`, `--shadow-lg`, `--shadow-xl`
- **Responsive breakpoints**: 1024px, 768px, 480px

### Authentication Flow
1. User submits login form to `/login` POST
2. `hash_password()` creates SHA-256 hash
3. `manager.get_user_by_username()` retrieves user
4. Password hash compared
5. On success: `session['user_id']`, `session['username']`, `session['role']` set
6. Protected routes check session with decorators

### Data Persistence
- All data stored in single JSON file: `jet_schedule_data.json`
- `JetScheduleManager.save_data()` must be called after any modifications
- File contains dictionaries of serialized objects for each entity type
- Auto-creates file on first run if missing

## Key Files

- `web_app.py` - Flask application entry point (1143 lines)
- `jet_manager.py` - Core business logic and data models
- `setup_initial_data.py` - Sample data generator
- `Procfile` - Railway/Gunicorn configuration
- `railway.toml` - Railway deployment settings
- `requirements.txt` - Python dependencies
- `templates/base.html` - Base template with modern CSS design system
- `static/css/custom.css` - Additional styles and utilities

## Documentation

- `README.md` - Main project documentation
- `RAILWAY_DEPLOYMENT.md` - Detailed Railway deployment guide
- `QUICK_DEPLOY.md` - Quick deployment instructions
- `MAINTENANCE_ACCESS_CONTROL.md` - Maintenance permissions reference
- `BUTTON_VISIBILITY_BY_ROLE.md` - UI element visibility by role
- `CUSTOMER_MANAGEMENT_FEATURE.md` - Customer management guide

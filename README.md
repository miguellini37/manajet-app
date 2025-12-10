# Manajet - Private Jet Management System

A comprehensive web-based application for managing private jet operations, including flight scheduling, maintenance tracking, passenger management, and multi-customer support.

## Features

### Core Functionality
- **Flight Management** - Schedule and track flights with crew and passenger assignments
- **Maintenance Tracking** - Schedule and monitor aircraft maintenance with conflict detection
- **Passenger Management** - Maintain passenger records with passport information
- **Crew Management** - Track pilots and cabin crew with license information
- **Aircraft Fleet** - Manage multiple aircraft with capacity and status tracking

### Multi-Customer Support
- **Customer Accounts** - Separate accounts for multiple customers
- **Role-Based Access Control** - Admin, Customer, Crew, and Mechanic roles
- **Data Isolation** - Customers see only their own aircraft and passengers
- **Asset Management** - Assign/unassign aircraft and passengers to customers

### Advanced Features
- **Maintenance Conflict Detection** - Warns when scheduling flights during maintenance
- **Dashboard with Activity Feed** - Real-time view of flights, maintenance, and operations
- **Mobile-Responsive Design** - Works on desktop, tablet, and mobile devices
- **Inline Passenger Creation** - Add passengers directly from flight scheduling form
- **Real-Time Validation** - Capacity and pilot requirement checks

## User Roles & Permissions

| Feature | Admin | Customer | Crew (Pilot) | Mechanic |
|---------|-------|----------|--------------|----------|
| View Dashboard | ✅ | ✅ | ✅ | ✅ |
| Manage Customers | ✅ | ❌ | ❌ | ❌ |
| Add/Edit Passengers | ✅ | ✅ (own) | ❌ | ❌ |
| Schedule Flights | ✅ | ✅ | ✅ | ✅ |
| Schedule/Edit Maintenance | ✅ | ❌ | ✅ | ✅ |
| Delete Maintenance | ✅ | ❌ | ❌ | ✅ |
| View Maintenance | ✅ All | ✅ (own aircraft) | ✅ All | ✅ All |

## Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/manajet-app.git
   cd manajet-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up initial data** (creates sample users and data)
   ```bash
   python setup_initial_data.py
   ```

4. **Run the application**
   ```bash
   python web_app.py
   ```

5. **Access the application**
   - Open your browser to: `http://localhost:5000`
   - Log in with sample credentials (see below)

## Sample User Accounts

### Admin (Full Access)
- **Username:** `admin`
- **Password:** `admin123`
- Full system access including customer management

### Customer Accounts
**Customer 1 - John Smith (Smith Enterprises)**
- **Username:** `johnsmith`
- **Password:** `customer123`
- Owns 2 aircraft, 2 passengers

**Customer 2 - Sarah Johnson (Johnson Aviation LLC)**
- **Username:** `sarahjohnson`
- **Password:** `customer123`
- Owns 1 aircraft, 1 passenger

### Crew Account
**Pilot - Captain Mike Anderson**
- **Username:** `pilot_mike`
- **Password:** `crew123`
- Can schedule and manage maintenance

### Mechanic Account
**Mechanic - Joe**
- **Username:** `mechanic_joe`
- **Password:** `mech123`
- Full maintenance management access

⚠️ **Security Note:** Change these default passwords in production!

## Project Structure

```
manajet-app/
├── web_app.py                 # Flask web application (main entry point)
├── jet_manager.py             # Core business logic and data models
├── jet_manager_cli.py         # Command-line interface (legacy)
├── setup_initial_data.py      # Initial data setup script
├── jet_schedule_data.json     # Data storage (JSON file)
├── requirements.txt           # Python dependencies
├── templates/                 # HTML templates (Jinja2)
│   ├── base.html             # Base template with navigation
│   ├── dashboard.html        # Main dashboard with activity feed
│   ├── login.html            # Login page
│   ├── customers.html        # Customer management
│   ├── flights*.html         # Flight management templates
│   ├── maintenance*.html     # Maintenance templates
│   └── ...
├── static/                    # Static assets (CSS, JS, images)
└── docs/                      # Documentation files
    ├── QUICK_START.md
    ├── MAINTENANCE_ACCESS_CONTROL.md
    └── ...
```

## Key Technologies

- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3, JavaScript (vanilla)
- **Templating:** Jinja2
- **Data Storage:** JSON file (easily upgradeable to SQLite/PostgreSQL)
- **Authentication:** Session-based with SHA-256 hashing

## Documentation

Comprehensive documentation is available in the project:

- **[QUICK_START.md](QUICK_START.md)** - Getting started guide
- **[MAINTENANCE_ACCESS_CONTROL.md](MAINTENANCE_ACCESS_CONTROL.md)** - Maintenance and access control details
- **[BUTTON_VISIBILITY_BY_ROLE.md](BUTTON_VISIBILITY_BY_ROLE.md)** - Role-based UI reference
- **[CUSTOMER_MANAGEMENT_FEATURE.md](CUSTOMER_MANAGEMENT_FEATURE.md)** - Customer management guide
- **[MOBILE_RESPONSIVE_GUIDE.md](MOBILE_RESPONSIVE_GUIDE.md)** - Mobile optimization details

## Features in Detail

### Flight Scheduling
- Select aircraft from available fleet
- Multi-select passengers and crew
- Real-time capacity validation
- Pilot requirement enforcement
- Maintenance conflict detection with override option
- Inline passenger creation via modal

### Maintenance Management
- Schedule routine and emergency maintenance
- Track maintenance status (Scheduled, In Progress, Completed)
- Role-based creation/editing (admin, crew, mechanics)
- Customers can view maintenance for their aircraft
- Automatic conflict warnings when scheduling flights

### Customer Management (Admin Only)
- Create and manage customer accounts
- Assign/unassign aircraft to customers
- Assign/unassign passengers to customers
- View customer statistics (aircraft count, passenger count)
- Create user accounts linked to customers

### Dashboard
- Real-time activity feed
- Statistics cards (aircraft, flights, passengers, maintenance)
- Active flights table
- Flights this week
- Upcoming flights (next 7 days)
- Active and scheduled maintenance
- Recently completed flights
- Role-specific quick actions

## Development

### Running in Development Mode
```bash
python web_app.py
```
The app runs on `http://localhost:5000` with debug mode enabled.

### Data Storage
Data is stored in `jet_schedule_data.json`. To reset the database:
1. Delete `jet_schedule_data.json`
2. Run `python setup_initial_data.py`

### Adding New Features
1. Update data models in `jet_manager.py`
2. Add routes in `web_app.py`
3. Create/update templates in `templates/`
4. Test with different user roles

## Production Deployment

For production deployment:

1. **Change Secret Key**
   ```python
   app.secret_key = 'your-secure-random-key-here'
   ```

2. **Upgrade Password Hashing**
   - Replace SHA-256 with bcrypt or Argon2

3. **Use Production Database**
   - Migrate from JSON to SQLite or PostgreSQL

4. **Set Debug to False**
   ```python
   app.run(debug=False)
   ```

5. **Use Production Server**
   - Deploy with Gunicorn or uWSGI behind Nginx

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

## Security Features

- Session-based authentication
- Role-based access control (RBAC)
- Backend route protection with decorators
- Frontend button visibility based on permissions
- Customer data isolation
- Input validation
- SQL injection prevention (via parameterized queries if using SQL)

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation in the `docs/` folder

## Acknowledgments

- Built with Flask web framework
- Inspired by real-world aviation management needs
- Designed for small to medium-sized private jet operators

## Version History

- **v1.0.0** (2025-10-15)
  - Initial release
  - Multi-customer support
  - Role-based access control
  - Maintenance conflict detection
  - Mobile-responsive design
  - Comprehensive dashboard

---

**Manajet** - Professional Aviation Management
© 2025 Manajet IO LLC

# Private Jet Schedule Management System

A comprehensive Python application for managing private jet operations, including passenger tracking with passport information, flight scheduling, and maintenance management.

## Features

### Passenger Management
- Store passenger details including passport numbers
- Track passport expiration dates
- Manage contact information
- Link passengers to flights

### Flight Scheduling
- Schedule flights with departure and arrival times
- Assign jets and passengers to flights
- Track flight status (Scheduled, In Progress, Completed, Cancelled)
- Validate passenger capacity against jet specifications

### Maintenance Tracking
- Schedule routine and emergency maintenance
- Track maintenance status and completion
- View maintenance history by jet
- Maintain detailed service records

### Data Persistence
- Automatic save/load functionality using JSON
- All data persists between sessions

## Files

- **jet_manager.py** - Core application with all business logic and data models
- **jet_manager_cli.py** - Interactive command-line interface
- **jet_manager_gui.py** - Graphical user interface (tkinter)
- **web_app.py** - Flask web application for browser access
- **generate_templates.py** - Generates HTML templates for web app
- **jet_schedule_data.json** - Data storage file (created automatically)

## Installation

No external dependencies required. Uses Python standard library only.

Requirements:
- Python 3.7 or higher

## Usage

### Starting the Application

You can run the application in three ways:

**Web Interface (Recommended for Multiple Users/Remote Access):**
```bash
# One-command setup (Windows)
setup_web.bat

# Or manually:
python generate_templates.py
pip install flask
python web_app.py
# Open browser to http://localhost:5000
```

**GUI Interface (Desktop Application):**
```bash
python jet_manager_gui.py
```

**CLI Interface (Terminal/Command Line):**
```bash
python jet_manager_cli.py
```

### Web Interface Features

The browser-based interface includes:
- **Modern Design** - Professional gradient UI with responsive layout
- **Multi-User Support** - Multiple people can access simultaneously
- **Remote Access** - Access from any device on the network
- **Dashboard** - Real-time statistics and quick actions
- **All Management Features** - Full CRUD for passengers, jets, flights, maintenance
- **Status Synchronization** - Automatic updates when statuses change
- **Mobile Friendly** - Works on phones and tablets

**Deployment Options:**
- See [WEB_DEPLOYMENT_SUMMARY.md](WEB_DEPLOYMENT_SUMMARY.md) for quick start
- See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for all hosting options
- Deploy FREE to Render.com, Heroku, PythonAnywhere, etc.

### GUI Features

The graphical interface includes:
- **Tabbed Interface** - Easy navigation between Passengers, Jets, Flights, Maintenance, and Dashboard
- **Forms** - User-friendly forms for adding and editing data
- **Data Tables** - View all records in sortable tables
- **Double-click to Edit** - Double-click any record to load it into the form
- **Dashboard** - View system statistics and jet schedules
- **Real-time Status** - Status bar shows current operations
- **Auto-save** - Prompts to save data on exit

### CLI Menu Options (Command-Line Interface)

1. **Add Passenger** - Register a new passenger with passport details
2. **List All Passengers** - View all registered passengers
3. **View Passenger Details** - Look up specific passenger information
4. **Add Jet** - Register a new jet with specifications
5. **List All Jets** - View all registered jets
6. **View Jet Schedule** - See complete schedule for a specific jet
7. **Schedule Flight** - Create a new flight booking
8. **List All Flights** - View all scheduled flights (with optional status filter)
9. **Update Flight Status** - Change flight status
10. **Schedule Maintenance** - Schedule maintenance for a jet
11. **Complete Maintenance** - Mark maintenance as completed
12. **List Maintenance Records** - View maintenance history (with filters)
13. **Save Data** - Manually save all data to file
14. **Exit** - Exit the application

## Example Workflow

### 1. Register a Jet
```
Jet ID: JET001
Jet Model: Gulfstream G650
Tail Number: N123AB
Passenger Capacity: 14
Status: Available
```

### 2. Register Passengers
```
Passenger ID: P001
Full Name: John Smith
Passport Number: AB1234567
Nationality: USA
Passport Expiry Date: 2026-12-31
Contact: john.smith@email.com
```

### 3. Schedule a Flight
```
Flight ID: FL001
Jet ID: JET001
Departure Airport: KTEB (Teterboro)
Destination Airport: KLAX (Los Angeles)
Departure Time: 2025-11-15 09:00
Arrival Time: 2025-11-15 14:30
Number of passengers: 1
  Passenger 1 ID: P001
```

### 4. Schedule Maintenance
```
Maintenance ID: MAINT001
Jet ID: JET001
Scheduled Date: 2025-12-01
Maintenance Type: Routine
Description: 100-hour inspection and service
```

## Data Model

### Passenger
- Passenger ID (unique identifier)
- Name
- Passport Number
- Nationality
- Passport Expiry Date
- Contact Information

### Private Jet
- Jet ID (unique identifier)
- Model
- Tail Number
- Passenger Capacity
- Status (Available, In Flight, Maintenance)

### Flight
- Flight ID (unique identifier)
- Jet ID (reference)
- Departure Airport
- Destination Airport
- Departure Time
- Arrival Time
- Passenger IDs (list of references)
- Status (Scheduled, In Progress, Completed, Cancelled)

### Maintenance Record
- Maintenance ID (unique identifier)
- Jet ID (reference)
- Scheduled Date
- Maintenance Type (Routine, Emergency, Inspection)
- Description
- Status (Scheduled, In Progress, Completed)
- Completed Date (when finished)

## Data Storage

All data is stored in `jet_schedule_data.json` in JSON format. The file is automatically:
- Created on first save
- Loaded when the application starts
- Can be manually saved using menu option 13
- Automatically prompts to save on exit

## Using as a Library

You can also import and use the core functionality in your own Python scripts:

```python
from jet_manager import JetScheduleManager

# Initialize manager
manager = JetScheduleManager()

# Add a passenger
manager.add_passenger(
    "P001",
    "John Smith",
    "AB1234567",
    "USA",
    "2026-12-31",
    "john@email.com"
)

# Add a jet
manager.add_jet("JET001", "Gulfstream G650", "N123AB", 14)

# Schedule a flight
manager.schedule_flight(
    "FL001",
    "JET001",
    "KTEB",
    "KLAX",
    "2025-11-15 09:00",
    "2025-11-15 14:30",
    ["P001"]
)

# Save data
manager.save_data()
```

## Security Note

This application stores sensitive information including passport numbers. In a production environment, you should:
- Encrypt the data file
- Implement access controls
- Use a proper database with encryption
- Follow data protection regulations (GDPR, etc.)
- Implement audit logging
- Use secure authentication

## License

This is a demonstration application. Modify as needed for your use case.

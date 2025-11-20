"""
Flask Web Application for Private Jet Schedule Management System
Simple, lightweight web interface that works with existing code
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from jet_manager import JetScheduleManager
from functools import wraps
from datetime import datetime, timedelta
import hashlib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Production-ready configuration
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = int(os.environ.get('PERMANENT_SESSION_LIFETIME', '3600'))

# Initialize manager
manager = JetScheduleManager()

# ====================
# AUTH HELPERS
# ====================

def hash_password(password: str) -> str:
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page', 'error')
                return redirect(url_for('login'))

            user = manager.get_user(session['user_id'])
            if not user or user.role not in roles:
                flash('You do not have permission to access this page', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_current_user():
    """Get currently logged in user"""
    if 'user_id' in session:
        return manager.get_user(session['user_id'])
    return None

def filter_by_customer(items, customer_field='customer_id'):
    """Filter items by customer for customer role users"""
    user = get_current_user()
    if not user:
        return []

    if user.role == 'customer':
        # Customer users only see their own data
        return [item for item in items if getattr(item, customer_field, None) == user.related_id]
    elif user.role in ['crew', 'mechanic']:
        # Crew and mechanics see all data
        return list(items)
    elif user.role == 'admin':
        # Admin sees everything
        return list(items)
    return []

# ====================
# AUTH ROUTES
# ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hash_password(password)

        user = manager.get_user_by_username(username)
        if user and user.password_hash == password_hash:
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['role'] = user.role
            flash(f'Welcome, {user.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration (creates customer account)"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        company = request.form['company']
        phone = request.form['phone']
        address = request.form['address']

        # Create customer first
        customer_id = manager.add_customer("", name, company, email, phone, address)
        if not customer_id:
            flash('Error creating customer account', 'error')
            return render_template('register.html')

        # Create user account
        password_hash = hash_password(password)
        user_id = manager.add_user("", username, password_hash, "customer", customer_id, email)

        if user_id:
            flash('Account created successfully! Please log in.', 'success')
            manager.save_data()
            return redirect(url_for('login'))
        else:
            # Rollback customer creation
            manager.delete_customer(customer_id)
            flash('Error creating user account (username may already exist)', 'error')

    return render_template('register.html')

# ====================
# DASHBOARD & HOME
# ====================

@app.route('/')
@login_required
def index():
    """Main dashboard with activity feed"""
    user = get_current_user()

    # Filter data based on user role
    if user.role == 'customer':
        passengers = filter_by_customer(manager.passengers.values())
        jets = filter_by_customer(manager.jets.values())
        flights = [f for f in manager.flights.values() if f.jet_id in [j.jet_id for j in jets]]
        maintenance = [m for m in manager.maintenance.values() if m.jet_id in [j.jet_id for j in jets]]
        crew = manager.crew.values()  # Crew visible to all
    else:
        passengers = list(manager.passengers.values())
        jets = list(manager.jets.values())
        flights = list(manager.flights.values())
        maintenance = list(manager.maintenance.values())
        crew = list(manager.crew.values())

    # Calculate date ranges (use date components for comparison to avoid time issues)
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    # Helper function to parse date strings
    def parse_date(date_str):
        try:
            # Handle both 'YYYY-MM-DD HH:MM' and 'YYYY-MM-DDThh:mm' formats
            date_part = date_str.replace('T', ' ').split()[0]
            return datetime.strptime(date_part, '%Y-%m-%d')
        except:
            return None

    # Active flights (In Progress)
    active_flights = [f for f in flights if f.status == 'In Progress']

    # Flights this week
    flights_this_week = []
    for f in flights:
        dep_date = parse_date(f.departure_time)
        if dep_date and week_start <= dep_date <= week_end:
            flights_this_week.append(f)

    # Upcoming flights (scheduled, next 7 days)
    upcoming_flights = []
    next_week = today + timedelta(days=7)
    for f in flights:
        if f.status == 'Scheduled':
            dep_date = parse_date(f.departure_time)
            if dep_date and today <= dep_date <= next_week:
                upcoming_flights.append(f)

    # Sort by departure time
    upcoming_flights.sort(key=lambda f: f.departure_time)
    flights_this_week.sort(key=lambda f: f.departure_time)

    # Active maintenance
    active_maintenance = [m for m in maintenance if m.status == 'In Progress']

    # Scheduled maintenance this week
    maintenance_this_week = []
    for m in maintenance:
        if m.status in ['Scheduled', 'In Progress']:
            maint_date = parse_date(m.scheduled_date)
            if maint_date and week_start <= maint_date <= week_end:
                maintenance_this_week.append(m)

    # Sort by scheduled date
    maintenance_this_week.sort(key=lambda m: m.scheduled_date)

    # Jets by status
    available_jets = [j for j in jets if j.status == 'Available']
    in_flight_jets = [j for j in jets if j.status == 'In Flight']
    maintenance_jets = [j for j in jets if j.status == 'Maintenance']

    # Recent activity (completed flights and maintenance in last 7 days)
    last_week = today - timedelta(days=7)
    recent_completed_flights = []
    for f in flights:
        if f.status == 'Completed':
            arr_date = parse_date(f.arrival_time)
            if arr_date and last_week <= arr_date <= today:
                recent_completed_flights.append(f)

    recent_completed_flights.sort(key=lambda f: f.arrival_time, reverse=True)
    recent_completed_flights = recent_completed_flights[:5]  # Last 5

    # Stats summary
    stats = {
        'total_passengers': len(passengers),
        'total_crew': len(crew),
        'total_jets': len(jets),
        'total_flights': len(flights),
        'total_maintenance': len(maintenance),
        'active_flights': len(active_flights),
        'available_jets': len(available_jets),
        'in_flight_jets': len(in_flight_jets),
        'maintenance_jets': len(maintenance_jets),
        'user': user
    }

    # Activity data
    activity = {
        'active_flights': active_flights[:10],  # Limit to 10
        'flights_this_week': flights_this_week[:10],
        'upcoming_flights': upcoming_flights[:10],
        'active_maintenance': active_maintenance[:10],
        'maintenance_this_week': maintenance_this_week[:10],
        'recent_completed': recent_completed_flights,
        'week_start': week_start.strftime('%Y-%m-%d'),
        'week_end': week_end.strftime('%Y-%m-%d'),
    }

    return render_template('dashboard.html', stats=stats, activity=activity, user=user, manager=manager)

# ====================
# PASSENGER ROUTES
# ====================

@app.route('/passengers')
@login_required
def passengers():
    """List all passengers"""
    user = get_current_user()
    passenger_list = filter_by_customer(manager.passengers.values())
    return render_template('passengers.html', passengers=passenger_list, user=user)

@app.route('/passengers/add', methods=['GET', 'POST'])
@role_required('customer', 'admin')
def add_passenger():
    """Add a new passenger"""
    user = get_current_user()

    if request.method == 'POST':
        # For customer users, automatically set customer_id
        customer_id = user.related_id if user.role == 'customer' else request.form.get('customer_id', '')

        passenger_id = manager.add_passenger(
            "",  # Auto-generate
            request.form['name'],
            request.form['passport_number'],
            request.form['nationality'],
            request.form['passport_expiry'],
            request.form['contact'],
            customer_id
        )
        if passenger_id:
            flash(f'Passenger added successfully with ID: {passenger_id}', 'success')
            manager.save_data()
            return redirect(url_for('passengers'))
        else:
            flash('Error adding passenger', 'error')

    # Admin can choose customer, customer users get their own automatically
    customers = manager.customers.values() if user.role == 'admin' else [manager.get_customer(user.related_id)]
    return render_template('passenger_form.html', user=user, customers=customers)

@app.route('/passengers/<passenger_id>')
def view_passenger(passenger_id):
    """View passenger details"""
    passenger = manager.get_passenger(passenger_id)
    if passenger:
        return render_template('passenger_detail.html', passenger=passenger)
    flash('Passenger not found', 'error')
    return redirect(url_for('passengers'))

@app.route('/passengers/<passenger_id>/edit', methods=['GET', 'POST'])
def edit_passenger(passenger_id):
    """Edit an existing passenger"""
    passenger = manager.get_passenger(passenger_id)
    if not passenger:
        flash('Passenger not found', 'error')
        return redirect(url_for('passengers'))

    if request.method == 'POST':
        success = manager.update_passenger(
            passenger_id,
            request.form['name'],
            request.form['passport_number'],
            request.form['nationality'],
            request.form['passport_expiry'],
            request.form['contact']
        )
        if success:
            flash(f'Passenger {passenger_id} updated successfully', 'success')
            manager.save_data()
            return redirect(url_for('view_passenger', passenger_id=passenger_id))
        else:
            flash('Error updating passenger', 'error')

    return render_template('passenger_form.html', passenger=passenger, edit_mode=True)

@app.route('/passengers/<passenger_id>/delete', methods=['POST'])
def delete_passenger(passenger_id):
    """Delete a passenger"""
    if manager.delete_passenger(passenger_id):
        flash(f'Passenger {passenger_id} deleted successfully', 'success')
        manager.save_data()
    else:
        flash('Cannot delete passenger - assigned to flights or not found', 'error')
    return redirect(url_for('passengers'))

# ====================
# CREW ROUTES
# ====================

@app.route('/crew')
def crew():
    """List all crew members"""
    return render_template('crew.html', crew=manager.crew.values())

@app.route('/crew/add', methods=['GET', 'POST'])
def add_crew():
    """Add a new crew member"""
    if request.method == 'POST':
        crew_id = manager.add_crew(
            "",  # Auto-generate
            request.form['name'],
            request.form['crew_type'],
            request.form['passport_number'],
            request.form['nationality'],
            request.form['passport_expiry'],
            request.form['contact'],
            request.form.get('license_number') or None
        )
        if crew_id:
            flash(f'Crew member added successfully with ID: {crew_id}', 'success')
            manager.save_data()
            return redirect(url_for('crew'))
        else:
            flash('Error adding crew member (pilots need license number)', 'error')

    return render_template('crew_form.html')

@app.route('/crew/<crew_id>')
def view_crew(crew_id):
    """View crew member details"""
    crew_member = manager.get_crew(crew_id)
    if crew_member:
        # Find flights this crew member is assigned to
        assigned_flights = [f for f in manager.flights.values() if crew_id in f.crew_ids]
        return render_template('crew_detail.html', crew=crew_member, flights=assigned_flights)
    flash('Crew member not found', 'error')
    return redirect(url_for('crew'))

@app.route('/crew/<crew_id>/edit', methods=['GET', 'POST'])
def edit_crew(crew_id):
    """Edit an existing crew member"""
    crew_member = manager.get_crew(crew_id)
    if not crew_member:
        flash('Crew member not found', 'error')
        return redirect(url_for('crew'))

    if request.method == 'POST':
        success = manager.update_crew(
            crew_id,
            request.form['name'],
            request.form['crew_type'],
            request.form['passport_number'],
            request.form['nationality'],
            request.form['passport_expiry'],
            request.form['contact'],
            request.form.get('license_number') or None
        )
        if success:
            flash(f'Crew member {crew_id} updated successfully', 'success')
            manager.save_data()
            return redirect(url_for('view_crew', crew_id=crew_id))
        else:
            flash('Error updating crew member (pilots need license number)', 'error')

    return render_template('crew_form.html', crew=crew_member, edit_mode=True)

@app.route('/crew/<crew_id>/delete', methods=['POST'])
def delete_crew(crew_id):
    """Delete a crew member"""
    if manager.delete_crew(crew_id):
        flash(f'Crew member {crew_id} deleted successfully', 'success')
        manager.save_data()
    else:
        flash('Cannot delete crew member - assigned to flights or not found', 'error')
    return redirect(url_for('crew'))

# ====================
# JET ROUTES
# ====================

@app.route('/jets')
def jets():
    """List all jets"""
    return render_template('jets.html', jets=manager.jets.values())

@app.route('/jets/add', methods=['GET', 'POST'])
def add_jet():
    """Add a new jet"""
    if request.method == 'POST':
        jet_id = manager.add_jet(
            "",  # Auto-generate
            request.form['model'],
            request.form['tail_number'],
            int(request.form['capacity']),
            request.form.get('status', 'Available')
        )
        if jet_id:
            flash(f'Jet added successfully with ID: {jet_id}', 'success')
            manager.save_data()
            return redirect(url_for('jets'))
        else:
            flash('Error adding jet', 'error')

    return render_template('jet_form.html')

@app.route('/jets/<jet_id>')
def view_jet(jet_id):
    """View jet schedule and details"""
    jet = manager.get_jet(jet_id)
    if jet:
        flights = [f for f in manager.flights.values() if f.jet_id == jet_id]
        maintenance = [m for m in manager.maintenance.values() if m.jet_id == jet_id]
        return render_template('jet_detail.html', jet=jet, flights=flights, maintenance=maintenance)
    flash('Jet not found', 'error')
    return redirect(url_for('jets'))

@app.route('/jets/<jet_id>/edit', methods=['GET', 'POST'])
def edit_jet(jet_id):
    """Edit an existing jet"""
    jet = manager.get_jet(jet_id)
    if not jet:
        flash('Jet not found', 'error')
        return redirect(url_for('jets'))

    if request.method == 'POST':
        success = manager.update_jet(
            jet_id,
            request.form['model'],
            request.form['tail_number'],
            int(request.form['capacity']),
            request.form.get('status', 'Available')
        )
        if success:
            flash(f'Jet {jet_id} updated successfully', 'success')
            manager.save_data()
            return redirect(url_for('view_jet', jet_id=jet_id))
        else:
            flash('Error updating jet', 'error')

    return render_template('jet_form.html', jet=jet, edit_mode=True)

@app.route('/jets/<jet_id>/delete', methods=['POST'])
def delete_jet(jet_id):
    """Delete a jet"""
    if manager.delete_jet(jet_id):
        flash(f'Jet {jet_id} deleted successfully', 'success')
        manager.save_data()
    else:
        flash('Cannot delete jet - has flights or maintenance records', 'error')
    return redirect(url_for('jets'))

# ====================
# FLIGHT ROUTES
# ====================

@app.route('/flights')
def flights():
    """List all flights"""
    return render_template('flights.html', flights=manager.flights.values())

@app.route('/flights/add', methods=['GET', 'POST'])
@login_required
def add_flight():
    """Schedule a new flight"""
    user = get_current_user()

    if request.method == 'POST':
        # Get selected passengers and crew from multi-select
        passenger_ids = request.form.getlist('passengers')
        crew_ids = request.form.getlist('crew')
        jet_id = request.form['jet_id']
        override_maintenance = request.form.get('override_maintenance') == 'true'

        # Check for maintenance conflicts
        active_maintenance = [m for m in manager.maintenance.values()
                            if m.jet_id == jet_id and m.status in ['Scheduled', 'In Progress']]

        if active_maintenance and not override_maintenance:
            # Show warning and ask for confirmation
            maintenance_details = active_maintenance[0]
            flash(f'WARNING: Aircraft has scheduled maintenance ({maintenance_details.maintenance_type}) on {maintenance_details.scheduled_date}. Flight scheduling requires override.', 'warning')

            # Re-render form with maintenance warning
            if user.role == 'customer':
                available_jets = filter_by_customer(manager.jets.values())
                available_passengers = filter_by_customer(manager.passengers.values())
            else:
                available_jets = list(manager.jets.values())
                available_passengers = list(manager.passengers.values())

            return render_template('flight_form.html',
                                 jets=available_jets,
                                 passengers=available_passengers,
                                 crew=manager.crew.values(),
                                 user=user,
                                 maintenance_warning=True,
                                 maintenance_details=maintenance_details,
                                 form_data=request.form)

        flight_id = manager.schedule_flight(
            "",  # Auto-generate
            jet_id,
            request.form['departure'],
            request.form['destination'],
            request.form['departure_time'],
            request.form['arrival_time'],
            passenger_ids,
            crew_ids  # REQUIRED!
        )
        if flight_id:
            if override_maintenance:
                flash(f'Flight scheduled successfully with ID: {flight_id} (Maintenance override applied)', 'success')
            else:
                flash(f'Flight scheduled successfully with ID: {flight_id}', 'success')
            manager.save_data()
            return redirect(url_for('flights'))
        else:
            flash('Error scheduling flight - check crew requirements (need at least 1 pilot)', 'error')

    # Filter data based on user role
    if user.role == 'customer':
        available_jets = filter_by_customer(manager.jets.values())
        available_passengers = filter_by_customer(manager.passengers.values())
    else:
        available_jets = list(manager.jets.values())
        available_passengers = list(manager.passengers.values())

    # Filter for available jets only
    available_jets = [j for j in available_jets if j.status == 'Available']

    return render_template('flight_form.html',
                         jets=available_jets,
                         passengers=available_passengers,
                         crew=manager.crew.values(),
                         user=user)

@app.route('/flights/<flight_id>')
def view_flight(flight_id):
    """View flight details"""
    flight = manager.get_flight(flight_id)
    if flight:
        jet = manager.get_jet(flight.jet_id)
        passengers = [manager.get_passenger(pid) for pid in flight.passenger_ids]
        crew = [manager.get_crew(cid) for cid in flight.crew_ids]
        return render_template('flight_detail.html', flight=flight, jet=jet, passengers=passengers, crew=crew)
    flash('Flight not found', 'error')
    return redirect(url_for('flights'))

@app.route('/flights/<flight_id>/trip-sheet')
@login_required
def flight_trip_sheet(flight_id):
    """Generate trip sheet for a flight"""
    flight = manager.get_flight(flight_id)
    if not flight:
        flash('Flight not found', 'error')
        return redirect(url_for('flights'))

    jet = manager.get_jet(flight.jet_id)
    passengers = [manager.get_passenger(pid) for pid in flight.passenger_ids if manager.get_passenger(pid)]
    crew = [manager.get_crew(cid) for cid in flight.crew_ids if manager.get_crew(cid)]

    # Get current timestamp for footer
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return render_template('trip_sheet.html',
                         flight=flight,
                         jet=jet,
                         passengers=passengers,
                         crew=crew,
                         current_time=current_time)

@app.route('/jets/<jet_id>/aircraft-sheet')
@login_required
def aircraft_sheet(jet_id):
    """Generate aircraft information sheet with monthly flights and maintenance"""
    jet = manager.get_jet(jet_id)
    if not jet:
        flash('Aircraft not found', 'error')
        return redirect(url_for('jets'))

    # Get current date info
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    month_name = now.strftime('%B')

    # Get customer info
    customer = manager.get_customer(jet.customer_id) if jet.customer_id else None

    # Filter flights for this month
    flights_this_month = []
    for flight in manager.flights.values():
        if flight.jet_id == jet_id:
            try:
                # Parse departure date
                dep_date_str = flight.departure_time.replace('T', ' ').split()[0]
                dep_date = datetime.strptime(dep_date_str, '%Y-%m-%d')
                if dep_date.year == current_year and dep_date.month == current_month:
                    flights_this_month.append(flight)
            except:
                pass

    # Sort flights by departure time
    flights_this_month.sort(key=lambda f: f.departure_time)

    # Filter maintenance for this month
    maintenance_this_month = []
    for maint in manager.maintenance.values():
        if maint.jet_id == jet_id:
            try:
                # Parse scheduled date
                maint_date = datetime.strptime(maint.scheduled_date, '%Y-%m-%d')
                if maint_date.year == current_year and maint_date.month == current_month:
                    maintenance_this_month.append(maint)
            except:
                pass

    # Sort maintenance by scheduled date
    maintenance_this_month.sort(key=lambda m: m.scheduled_date)

    # Estimate flight hours (rough calculation: 1 hour per 500 miles, assume average 1000 miles per flight)
    flight_hours = len(flights_this_month) * 2  # Simplified estimate

    # Get current timestamp
    current_time = now.strftime('%Y-%m-%d %H:%M:%S')

    return render_template('aircraft_sheet.html',
                         jet=jet,
                         customer=customer,
                         flights=flights_this_month,
                         maintenance_records=maintenance_this_month,
                         current_year=current_year,
                         month_name=month_name,
                         flight_hours=flight_hours,
                         current_time=current_time)

@app.route('/flights/<flight_id>/edit', methods=['GET', 'POST'])
def edit_flight(flight_id):
    """Edit an existing flight"""
    flight = manager.get_flight(flight_id)
    if not flight:
        flash('Flight not found', 'error')
        return redirect(url_for('flights'))

    if request.method == 'POST':
        passenger_ids = [p.strip() for p in request.form['passenger_ids'].split(',') if p.strip()]
        crew_ids = [c.strip() for c in request.form['crew_ids'].split(',') if c.strip()]
        success = manager.update_flight(
            flight_id,
            request.form['jet_id'],
            request.form['departure'],
            request.form['destination'],
            request.form['departure_time'],
            request.form['arrival_time'],
            passenger_ids,
            crew_ids,
            request.form.get('status', 'Scheduled')
        )
        if success:
            flash(f'Flight {flight_id} updated successfully', 'success')
            manager.save_data()
            return redirect(url_for('view_flight', flight_id=flight_id))
        else:
            flash('Error updating flight - check crew requirements', 'error')

    return render_template('flight_form.html',
                         flight=flight,
                         jets=manager.jets.values(),
                         passengers=manager.passengers.values(),
                         crew=manager.crew.values(),
                         edit_mode=True)

@app.route('/flights/<flight_id>/delete', methods=['POST'])
def delete_flight(flight_id):
    """Delete a flight"""
    if manager.delete_flight(flight_id):
        flash(f'Flight {flight_id} deleted successfully', 'success')
        manager.save_data()
    else:
        flash('Cannot delete flight - not found', 'error')
    return redirect(url_for('flights'))

@app.route('/flights/<flight_id>/update-status', methods=['POST'])
def update_flight_status(flight_id):
    """Update flight status"""
    new_status = request.form['status']
    if manager.update_flight_status(flight_id, new_status):
        flash(f'Flight status updated to {new_status}', 'success')
        manager.save_data()
    else:
        flash('Error updating flight status', 'error')
    return redirect(url_for('view_flight', flight_id=flight_id))

# ====================
# MAINTENANCE ROUTES
# ====================

@app.route('/maintenance')
@login_required
def maintenance():
    """List all maintenance records"""
    user = get_current_user()

    # Filter maintenance by user role
    if user.role == 'customer':
        # Customers see only maintenance for their aircraft
        customer_jets = [j.jet_id for j in manager.jets.values() if j.customer_id == user.related_id]
        maintenance_list = [m for m in manager.maintenance.values() if m.jet_id in customer_jets]
    else:
        # Admin, crew, mechanics see all maintenance
        maintenance_list = list(manager.maintenance.values())

    return render_template('maintenance.html', maintenance=maintenance_list, user=user)

@app.route('/maintenance/add', methods=['GET', 'POST'])
@role_required('admin', 'crew', 'mechanic')
def add_maintenance():
    """Schedule maintenance (admin, crew, mechanics only)"""
    user = get_current_user()

    if request.method == 'POST':
        maint_id = manager.schedule_maintenance(
            "",  # Auto-generate
            request.form['jet_id'],
            request.form['scheduled_date'],
            request.form['maintenance_type'],
            request.form['description']
        )
        if maint_id:
            flash(f'Maintenance scheduled successfully with ID: {maint_id}', 'success')
            manager.save_data()
            return redirect(url_for('maintenance'))
        else:
            flash('Error scheduling maintenance', 'error')

    return render_template('maintenance_form.html', jets=manager.jets.values(), user=user)

@app.route('/maintenance/<maintenance_id>')
def view_maintenance(maintenance_id):
    """View maintenance details"""
    maint = manager.maintenance.get(maintenance_id)
    if maint:
        jet = manager.get_jet(maint.jet_id)
        return render_template('maintenance_detail.html', maintenance=maint, jet=jet)
    flash('Maintenance record not found', 'error')
    return redirect(url_for('maintenance'))

@app.route('/maintenance/<maintenance_id>/edit', methods=['GET', 'POST'])
@role_required('admin', 'crew', 'mechanic')
def edit_maintenance(maintenance_id):
    """Edit an existing maintenance record (admin, crew, mechanics only)"""
    user = get_current_user()
    maint = manager.maintenance.get(maintenance_id)
    if not maint:
        flash('Maintenance record not found', 'error')
        return redirect(url_for('maintenance'))

    if request.method == 'POST':
        success = manager.update_maintenance(
            maintenance_id,
            request.form['jet_id'],
            request.form['scheduled_date'],
            request.form['maintenance_type'],
            request.form['description'],
            request.form.get('status', 'Scheduled'),
            request.form.get('completed_date') or None
        )
        if success:
            flash(f'Maintenance {maintenance_id} updated successfully', 'success')
            manager.save_data()
            return redirect(url_for('view_maintenance', maintenance_id=maintenance_id))
        else:
            flash('Error updating maintenance', 'error')

    return render_template('maintenance_form.html',
                         maintenance=maint,
                         jets=manager.jets.values(),
                         user=user,
                         edit_mode=True)

@app.route('/maintenance/<maintenance_id>/delete', methods=['POST'])
@role_required('admin', 'mechanic')
def delete_maintenance(maintenance_id):
    """Delete a maintenance record (admin, mechanics only)"""
    if manager.delete_maintenance(maintenance_id):
        flash(f'Maintenance {maintenance_id} deleted successfully', 'success')
        manager.save_data()
    else:
        flash('Cannot delete maintenance - not found', 'error')
    return redirect(url_for('maintenance'))

@app.route('/maintenance/<maintenance_id>/update-status', methods=['POST'])
@role_required('admin', 'crew', 'mechanic')
def update_maintenance_status(maintenance_id):
    """Update maintenance status (admin, crew, mechanics only)"""
    new_status = request.form['status']
    completed_date = request.form.get('completed_date') if new_status == 'Completed' else None

    if manager.update_maintenance_status(maintenance_id, new_status, completed_date):
        flash(f'Maintenance status updated to {new_status}', 'success')
        manager.save_data()
    else:
        flash('Error updating maintenance status', 'error')
    return redirect(url_for('view_maintenance', maintenance_id=maintenance_id))

# ====================
# CUSTOMER ROUTES (Admin Only)
# ====================

@app.route('/customers')
@role_required('admin')
def customers():
    """List all customers (admin only)"""
    user = get_current_user()
    customer_list = list(manager.customers.values())

    # Get counts for each customer
    customer_stats = {}
    for customer in customer_list:
        jets_count = len([j for j in manager.jets.values() if j.customer_id == customer.customer_id])
        passengers_count = len([p for p in manager.passengers.values() if p.customer_id == customer.customer_id])
        customer_stats[customer.customer_id] = {
            'jets': jets_count,
            'passengers': passengers_count
        }

    return render_template('customers.html', customers=customer_list, stats=customer_stats, user=user)

@app.route('/customers/add', methods=['GET', 'POST'])
@role_required('admin')
def add_customer():
    """Add a new customer (admin only)"""
    user = get_current_user()

    if request.method == 'POST':
        customer_id = manager.add_customer(
            "",  # Auto-generate
            request.form['name'],
            request.form['company'],
            request.form['email'],
            request.form['phone'],
            request.form['address']
        )
        if customer_id:
            flash(f'Customer added successfully with ID: {customer_id}', 'success')
            manager.save_data()
            return redirect(url_for('customers'))
        else:
            flash('Error adding customer', 'error')

    return render_template('customer_form.html', user=user)

@app.route('/customers/<customer_id>')
@role_required('admin')
def view_customer(customer_id):
    """View customer details with associated jets and passengers"""
    user = get_current_user()
    customer = manager.get_customer(customer_id)
    if not customer:
        flash('Customer not found', 'error')
        return redirect(url_for('customers'))

    # Get all jets and passengers for this customer
    customer_jets = [j for j in manager.jets.values() if j.customer_id == customer_id]
    customer_passengers = [p for p in manager.passengers.values() if p.customer_id == customer_id]

    # Get all available jets and passengers (not assigned to any customer)
    unassigned_jets = [j for j in manager.jets.values() if not j.customer_id or j.customer_id == '']
    unassigned_passengers = [p for p in manager.passengers.values() if not p.customer_id or p.customer_id == '']

    # Get user account for this customer
    customer_user = None
    for u in manager.users.values():
        if u.role == 'customer' and u.related_id == customer_id:
            customer_user = u
            break

    return render_template('customer_detail.html',
                         customer=customer,
                         customer_jets=customer_jets,
                         customer_passengers=customer_passengers,
                         unassigned_jets=unassigned_jets,
                         unassigned_passengers=unassigned_passengers,
                         customer_user=customer_user,
                         user=user)

@app.route('/customers/<customer_id>/edit', methods=['GET', 'POST'])
@role_required('admin')
def edit_customer(customer_id):
    """Edit an existing customer"""
    user = get_current_user()
    customer = manager.get_customer(customer_id)
    if not customer:
        flash('Customer not found', 'error')
        return redirect(url_for('customers'))

    if request.method == 'POST':
        success = manager.update_customer(
            customer_id,
            request.form['name'],
            request.form['company'],
            request.form['email'],
            request.form['phone'],
            request.form['address']
        )
        if success:
            flash(f'Customer {customer_id} updated successfully', 'success')
            manager.save_data()
            return redirect(url_for('view_customer', customer_id=customer_id))
        else:
            flash('Error updating customer', 'error')

    return render_template('customer_form.html', customer=customer, edit_mode=True, user=user)

@app.route('/customers/<customer_id>/delete', methods=['POST'])
@role_required('admin')
def delete_customer(customer_id):
    """Delete a customer"""
    if manager.delete_customer(customer_id):
        flash(f'Customer {customer_id} deleted successfully', 'success')
        manager.save_data()
    else:
        flash('Cannot delete customer - has associated jets/passengers or not found', 'error')
    return redirect(url_for('customers'))

@app.route('/customers/<customer_id>/assign-jet', methods=['POST'])
@role_required('admin')
def assign_jet_to_customer(customer_id):
    """Assign a jet to a customer"""
    jet_id = request.form.get('jet_id')
    jet = manager.get_jet(jet_id)
    customer = manager.get_customer(customer_id)

    if not jet or not customer:
        flash('Jet or customer not found', 'error')
        return redirect(url_for('view_customer', customer_id=customer_id))

    # Update jet's customer_id
    jet.customer_id = customer_id
    manager.save_data()
    flash(f'Jet {jet_id} assigned to {customer.name}', 'success')
    return redirect(url_for('view_customer', customer_id=customer_id))

@app.route('/customers/<customer_id>/unassign-jet/<jet_id>', methods=['POST'])
@role_required('admin')
def unassign_jet_from_customer(customer_id, jet_id):
    """Unassign a jet from a customer"""
    jet = manager.get_jet(jet_id)

    if not jet:
        flash('Jet not found', 'error')
        return redirect(url_for('view_customer', customer_id=customer_id))

    # Remove customer association
    jet.customer_id = ''
    manager.save_data()
    flash(f'Jet {jet_id} unassigned from customer', 'success')
    return redirect(url_for('view_customer', customer_id=customer_id))

@app.route('/customers/<customer_id>/assign-passenger', methods=['POST'])
@role_required('admin')
def assign_passenger_to_customer(customer_id):
    """Assign a passenger to a customer"""
    passenger_id = request.form.get('passenger_id')
    passenger = manager.get_passenger(passenger_id)
    customer = manager.get_customer(customer_id)

    if not passenger or not customer:
        flash('Passenger or customer not found', 'error')
        return redirect(url_for('view_customer', customer_id=customer_id))

    # Update passenger's customer_id
    passenger.customer_id = customer_id
    manager.save_data()
    flash(f'Passenger {passenger.name} assigned to {customer.name}', 'success')
    return redirect(url_for('view_customer', customer_id=customer_id))

@app.route('/customers/<customer_id>/unassign-passenger/<passenger_id>', methods=['POST'])
@role_required('admin')
def unassign_passenger_from_customer(customer_id, passenger_id):
    """Unassign a passenger from a customer"""
    passenger = manager.get_passenger(passenger_id)

    if not passenger:
        flash('Passenger not found', 'error')
        return redirect(url_for('view_customer', customer_id=customer_id))

    # Remove customer association
    passenger.customer_id = ''
    manager.save_data()
    flash(f'Passenger {passenger.name} unassigned from customer', 'success')
    return redirect(url_for('view_customer', customer_id=customer_id))

# ====================
# API ENDPOINTS (for AJAX/future mobile app)
# ====================

@app.route('/api/passengers/add', methods=['POST'])
@login_required
def api_add_passenger():
    """Quick add passenger via AJAX"""
    user = get_current_user()

    try:
        # For customer users, automatically set customer_id
        customer_id = user.related_id if user.role == 'customer' else request.json.get('customer_id', '')

        passenger_id = manager.add_passenger(
            "",  # Auto-generate
            request.json['name'],
            request.json['passport_number'],
            request.json['nationality'],
            request.json['passport_expiry'],
            request.json['contact'],
            customer_id
        )

        if passenger_id:
            manager.save_data()
            passenger = manager.get_passenger(passenger_id)
            return jsonify({
                'success': True,
                'passenger_id': passenger_id,
                'name': passenger.name,
                'passport_number': passenger.passport_number
            })
        else:
            return jsonify({'success': False, 'error': 'Error adding passenger'}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/jets/<jet_id>/status')
def api_jet_status(jet_id):
    """Get jet status (for real-time updates)"""
    jet = manager.get_jet(jet_id)
    if jet:
        return jsonify({'jet_id': jet_id, 'status': jet.status})
    return jsonify({'error': 'Jet not found'}), 404

@app.route('/api/stats')
def api_stats():
    """Get dashboard statistics"""
    return jsonify({
        'total_passengers': len(manager.passengers),
        'total_crew': len(manager.crew),
        'total_jets': len(manager.jets),
        'total_flights': len(manager.flights),
        'total_maintenance': len(manager.maintenance),
        'active_flights': len([f for f in manager.flights.values() if f.status == 'In Progress']),
        'available_jets': len([j for j in manager.jets.values() if j.status == 'Available']),
    })

# ====================
# ERROR HANDLERS
# ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# ====================
# MAIN
# ====================

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)

    # Get configuration from environment
    debug = os.environ.get('DEBUG', 'True') == 'True'
    port = int(os.environ.get('PORT', 5000))

    # Run application
    app.run(debug=debug, host='0.0.0.0', port=port)

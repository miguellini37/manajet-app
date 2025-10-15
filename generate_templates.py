"""
Quick Template Generator
Run this to create all missing HTML templates
"""

import os

def create_templates():
    """Generate all necessary HTML templates"""

    templates = {
        'passengers.html': '''{% extends "base.html" %}
{% block content %}
<h1>Passengers</h1>
<a href="{{ url_for('add_passenger') }}" class="btn btn-primary" style="margin-bottom: 20px;">➕ Add New Passenger</a>
<table>
    <thead>
        <tr>
            <th>ID</th><th>Name</th><th>Passport</th><th>Nationality</th><th>Expiry</th><th>Contact</th><th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for passenger in passengers %}
        <tr>
            <td>{{ passenger.passenger_id }}</td>
            <td>{{ passenger.name }}</td>
            <td>{{ passenger.passport_number }}</td>
            <td>{{ passenger.nationality }}</td>
            <td>{{ passenger.passport_expiry }}</td>
            <td>{{ passenger.contact }}</td>
            <td><a href="{{ url_for('view_passenger', passenger_id=passenger.passenger_id) }}" class="btn btn-primary">View</a></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}''',

        'passenger_form.html': '''{% extends "base.html" %}
{% block content %}
<h1>Add Passenger</h1>
<form method="POST" class="card">
    <div class="form-group">
        <label>Full Name *</label>
        <input type="text" name="name" required>
    </div>
    <div class="form-group">
        <label>Passport Number *</label>
        <input type="text" name="passport_number" required>
    </div>
    <div class="form-group">
        <label>Nationality *</label>
        <input type="text" name="nationality" required>
    </div>
    <div class="form-group">
        <label>Passport Expiry Date *</label>
        <input type="date" name="passport_expiry" required>
    </div>
    <div class="form-group">
        <label>Contact (Email/Phone) *</label>
        <input type="text" name="contact" required>
    </div>
    <button type="submit" class="btn btn-success">Add Passenger</button>
    <a href="{{ url_for('passengers') }}" class="btn btn-secondary">Cancel</a>
</form>
{% endblock %}''',

        'passenger_detail.html': '''{% extends "base.html" %}
{% block content %}
<a href="{{ url_for('passengers') }}" class="btn btn-secondary" style="margin-bottom: 20px;">← Back to Passengers</a>
<div class="card">
    <h1>{{ passenger.name }}</h1>
    <div style="margin-top: 20px;">
        <p><strong>Passenger ID:</strong> {{ passenger.passenger_id }}</p>
        <p><strong>Passport Number:</strong> {{ passenger.passport_number }}</p>
        <p><strong>Nationality:</strong> {{ passenger.nationality }}</p>
        <p><strong>Passport Expiry:</strong> {{ passenger.passport_expiry }}</p>
        <p><strong>Contact:</strong> {{ passenger.contact }}</p>
    </div>
</div>
{% endblock %}''',

        'jets.html': '''{% extends "base.html" %}
{% block content %}
<h1>Jets</h1>
<a href="{{ url_for('add_jet') }}" class="btn btn-primary" style="margin-bottom: 20px;">➕ Add New Jet</a>
<table>
    <thead>
        <tr>
            <th>ID</th><th>Model</th><th>Tail Number</th><th>Capacity</th><th>Status</th><th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for jet in jets %}
        <tr>
            <td>{{ jet.jet_id }}</td>
            <td>{{ jet.model }}</td>
            <td>{{ jet.tail_number }}</td>
            <td>{{ jet.capacity }}</td>
            <td><span class="status-badge status-{{ jet.status.lower().replace(' ', '-') }}">{{ jet.status }}</span></td>
            <td><a href="{{ url_for('view_jet', jet_id=jet.jet_id) }}" class="btn btn-primary">View Schedule</a></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}''',

        'jet_form.html': '''{% extends "base.html" %}
{% block content %}
<h1>Add Jet</h1>
<form method="POST" class="card">
    <div class="form-group">
        <label>Jet Model *</label>
        <input type="text" name="model" placeholder="e.g., Gulfstream G650" required>
    </div>
    <div class="form-group">
        <label>Tail Number *</label>
        <input type="text" name="tail_number" placeholder="e.g., N123AB" required>
    </div>
    <div class="form-group">
        <label>Passenger Capacity *</label>
        <input type="number" name="capacity" min="1" max="50" required>
    </div>
    <div class="form-group">
        <label>Status</label>
        <select name="status">
            <option value="Available">Available</option>
            <option value="Maintenance">Maintenance</option>
            <option value="In Flight">In Flight</option>
        </select>
    </div>
    <button type="submit" class="btn btn-success">Add Jet</button>
    <a href="{{ url_for('jets') }}" class="btn btn-secondary">Cancel</a>
</form>
{% endblock %}''',

        'jet_detail.html': '''{% extends "base.html" %}
{% block content %}
<a href="{{ url_for('jets') }}" class="btn btn-secondary" style="margin-bottom: 20px;">← Back to Jets</a>
<div class="card">
    <h1>{{ jet.model }}</h1>
    <div style="margin-top: 20px;">
        <p><strong>Jet ID:</strong> {{ jet.jet_id }}</p>
        <p><strong>Tail Number:</strong> {{ jet.tail_number }}</p>
        <p><strong>Capacity:</strong> {{ jet.capacity }} passengers</p>
        <p><strong>Status:</strong> <span class="status-badge status-{{ jet.status.lower().replace(' ', '-') }}">{{ jet.status }}</span></p>
    </div>
</div>

<div class="card" style="margin-top: 20px;">
    <h2>Scheduled Flights</h2>
    {% if flights %}
    <table>
        <thead>
            <tr><th>Flight ID</th><th>Route</th><th>Departure</th><th>Status</th></tr>
        </thead>
        <tbody>
            {% for flight in flights %}
            <tr>
                <td>{{ flight.flight_id }}</td>
                <td>{{ flight.departure }} → {{ flight.destination }}</td>
                <td>{{ flight.departure_time }}</td>
                <td><span class="status-badge status-{{ flight.status.lower().replace(' ', '-') }}">{{ flight.status }}</span></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p>No flights scheduled</p>
    {% endif %}
</div>

<div class="card" style="margin-top: 20px;">
    <h2>Maintenance Records</h2>
    {% if maintenance %}
    <table>
        <thead>
            <tr><th>Maintenance ID</th><th>Type</th><th>Scheduled Date</th><th>Status</th></tr>
        </thead>
        <tbody>
            {% for maint in maintenance %}
            <tr>
                <td>{{ maint.maintenance_id }}</td>
                <td>{{ maint.maintenance_type }}</td>
                <td>{{ maint.scheduled_date }}</td>
                <td><span class="status-badge status-{{ maint.status.lower().replace(' ', '-') }}">{{ maint.status }}</span></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p>No maintenance scheduled</p>
    {% endif %}
</div>
{% endblock %}''',

        'flights.html': '''{% extends "base.html" %}
{% block content %}
<h1>Flights</h1>
<a href="{{ url_for('add_flight') }}" class="btn btn-primary" style="margin-bottom: 20px;">✈️ Schedule New Flight</a>
<table>
    <thead>
        <tr>
            <th>Flight ID</th><th>Jet</th><th>Route</th><th>Departure</th><th>Arrival</th><th>Passengers</th><th>Status</th><th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for flight in flights %}
        <tr>
            <td>{{ flight.flight_id }}</td>
            <td>{{ flight.jet_id }}</td>
            <td>{{ flight.departure }} → {{ flight.destination }}</td>
            <td>{{ flight.departure_time }}</td>
            <td>{{ flight.arrival_time }}</td>
            <td>{{ flight.passenger_ids|length }}</td>
            <td><span class="status-badge status-{{ flight.status.lower().replace(' ', '-') }}">{{ flight.status }}</span></td>
            <td><a href="{{ url_for('view_flight', flight_id=flight.flight_id) }}" class="btn btn-primary">View</a></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}''',

        'flight_form.html': '''{% extends "base.html" %}
{% block content %}
<h1>Schedule Flight</h1>
<form method="POST" class="card">
    <div class="form-group">
        <label>Jet *</label>
        <select name="jet_id" required>
            <option value="">Select a jet...</option>
            {% for jet in jets %}
            <option value="{{ jet.jet_id }}">{{ jet.model }} ({{ jet.tail_number }}) - {{ jet.status }}</option>
            {% endfor %}
        </select>
    </div>
    <div class="grid-2">
        <div class="form-group">
            <label>Departure Airport *</label>
            <input type="text" name="departure" placeholder="e.g., KTEB" required>
        </div>
        <div class="form-group">
            <label>Destination Airport *</label>
            <input type="text" name="destination" placeholder="e.g., KLAX" required>
        </div>
    </div>
    <div class="grid-2">
        <div class="form-group">
            <label>Departure Time *</label>
            <input type="datetime-local" name="departure_time" required>
        </div>
        <div class="form-group">
            <label>Arrival Time *</label>
            <input type="datetime-local" name="arrival_time" required>
        </div>
    </div>
    <div class="form-group">
        <label>Passenger IDs (comma-separated) *</label>
        <input type="text" name="passenger_ids" placeholder="e.g., P001, P002" required>
        <small>Available passengers: {% for p in passengers %}{{ p.passenger_id }} ({{ p.name }}){% if not loop.last %}, {% endif %}{% endfor %}</small>
    </div>
    <button type="submit" class="btn btn-success">Schedule Flight</button>
    <a href="{{ url_for('flights') }}" class="btn btn-secondary">Cancel</a>
</form>
{% endblock %}''',

        'flight_detail.html': '''{% extends "base.html" %}
{% block content %}
<a href="{{ url_for('flights') }}" class="btn btn-secondary" style="margin-bottom: 20px;">← Back to Flights</a>
<div class="card">
    <h1>Flight {{ flight.flight_id }}</h1>
    <div style="margin-top: 20px;">
        <p><strong>Route:</strong> {{ flight.departure }} → {{ flight.destination }}</p>
        <p><strong>Jet:</strong> {{ jet.model }} ({{ jet.tail_number }})</p>
        <p><strong>Departure:</strong> {{ flight.departure_time }}</p>
        <p><strong>Arrival:</strong> {{ flight.arrival_time }}</p>
        <p><strong>Status:</strong> <span class="status-badge status-{{ flight.status.lower().replace(' ', '-') }}">{{ flight.status }}</span></p>
    </div>
</div>

<div class="card" style="margin-top: 20px;">
    <h2>Update Status</h2>
    <form method="POST" action="{{ url_for('update_flight_status', flight_id=flight.flight_id) }}">
        <div class="form-group">
            <select name="status" required>
                <option value="Scheduled" {% if flight.status == 'Scheduled' %}selected{% endif %}>Scheduled</option>
                <option value="In Progress" {% if flight.status == 'In Progress' %}selected{% endif %}>In Progress</option>
                <option value="Completed" {% if flight.status == 'Completed' %}selected{% endif %}>Completed</option>
                <option value="Cancelled" {% if flight.status == 'Cancelled' %}selected{% endif %}>Cancelled</option>
            </select>
        </div>
        <button type="submit" class="btn btn-success">Update Status</button>
    </form>
</div>

<div class="card" style="margin-top: 20px;">
    <h2>Passengers</h2>
    <ul>
        {% for passenger in passengers %}
        <li>{{ passenger.name }} ({{ passenger.passenger_id }}) - Passport: {{ passenger.passport_number }}</li>
        {% endfor %}
    </ul>
</div>
{% endblock %}''',

        'maintenance.html': '''{% extends "base.html" %}
{% block content %}
<h1>Maintenance Records</h1>
<a href="{{ url_for('add_maintenance') }}" class="btn btn-primary" style="margin-bottom: 20px;">🔧 Schedule Maintenance</a>
<table>
    <thead>
        <tr>
            <th>ID</th><th>Jet</th><th>Type</th><th>Scheduled Date</th><th>Description</th><th>Status</th><th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for maint in maintenance %}
        <tr>
            <td>{{ maint.maintenance_id }}</td>
            <td>{{ maint.jet_id }}</td>
            <td>{{ maint.maintenance_type }}</td>
            <td>{{ maint.scheduled_date }}</td>
            <td>{{ maint.description[:50] }}...</td>
            <td><span class="status-badge status-{{ maint.status.lower().replace(' ', '-') }}">{{ maint.status }}</span></td>
            <td><a href="{{ url_for('view_maintenance', maintenance_id=maint.maintenance_id) }}" class="btn btn-primary">View</a></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}''',

        'maintenance_form.html': '''{% extends "base.html" %}
{% block content %}
<h1>Schedule Maintenance</h1>
<form method="POST" class="card">
    <div class="form-group">
        <label>Jet *</label>
        <select name="jet_id" required>
            <option value="">Select a jet...</option>
            {% for jet in jets %}
            <option value="{{ jet.jet_id }}">{{ jet.model }} ({{ jet.tail_number }}) - {{ jet.status }}</option>
            {% endfor %}
        </select>
    </div>
    <div class="form-group">
        <label>Scheduled Date *</label>
        <input type="date" name="scheduled_date" required>
    </div>
    <div class="form-group">
        <label>Maintenance Type *</label>
        <select name="maintenance_type" required>
            <option value="Routine">Routine</option>
            <option value="Emergency">Emergency</option>
            <option value="Inspection">Inspection</option>
        </select>
    </div>
    <div class="form-group">
        <label>Description *</label>
        <textarea name="description" rows="4" required></textarea>
    </div>
    <button type="submit" class="btn btn-success">Schedule Maintenance</button>
    <a href="{{ url_for('maintenance') }}" class="btn btn-secondary">Cancel</a>
</form>
{% endblock %}''',

        'maintenance_detail.html': '''{% extends "base.html" %}
{% block content %}
<a href="{{ url_for('maintenance') }}" class="btn btn-secondary" style="margin-bottom: 20px;">← Back to Maintenance</a>
<div class="card">
    <h1>Maintenance {{ maintenance.maintenance_id }}</h1>
    <div style="margin-top: 20px;">
        <p><strong>Jet:</strong> {{ jet.model }} ({{ jet.tail_number }})</p>
        <p><strong>Type:</strong> {{ maintenance.maintenance_type }}</p>
        <p><strong>Scheduled Date:</strong> {{ maintenance.scheduled_date }}</p>
        <p><strong>Description:</strong> {{ maintenance.description }}</p>
        <p><strong>Status:</strong> <span class="status-badge status-{{ maintenance.status.lower().replace(' ', '-') }}">{{ maintenance.status }}</span></p>
        {% if maintenance.completed_date %}
        <p><strong>Completed:</strong> {{ maintenance.completed_date }}</p>
        {% endif %}
    </div>
</div>

<div class="card" style="margin-top: 20px;">
    <h2>Update Status</h2>
    <form method="POST" action="{{ url_for('update_maintenance_status', maintenance_id=maintenance.maintenance_id) }}">
        <div class="form-group">
            <label>Status</label>
            <select name="status" required>
                <option value="Scheduled" {% if maintenance.status == 'Scheduled' %}selected{% endif %}>Scheduled</option>
                <option value="In Progress" {% if maintenance.status == 'In Progress' %}selected{% endif %}>In Progress</option>
                <option value="Completed" {% if maintenance.status == 'Completed' %}selected{% endif %}>Completed</option>
            </select>
        </div>
        <div class="form-group">
            <label>Completed Date (if completed)</label>
            <input type="date" name="completed_date" value="{{ maintenance.completed_date or '' }}">
        </div>
        <button type="submit" class="btn btn-success">Update Status</button>
    </form>
</div>
{% endblock %}''',

        '404.html': '''{% extends "base.html" %}
{% block content %}
<div class="card" style="text-align: center; padding: 60px;">
    <h1 style="font-size: 72px; color: #e74c3c;">404</h1>
    <h2>Page Not Found</h2>
    <p style="margin-top: 20px;">The page you're looking for doesn't exist.</p>
    <a href="{{ url_for('index') }}" class="btn btn-primary" style="margin-top: 20px;">Go to Dashboard</a>
</div>
{% endblock %}''',

        '500.html': '''{% extends "base.html" %}
{% block content %}
<div class="card" style="text-align: center; padding: 60px;">
    <h1 style="font-size: 72px; color: #e74c3c;">500</h1>
    <h2>Server Error</h2>
    <p style="margin-top: 20px;">Something went wrong. Please try again later.</p>
    <a href="{{ url_for('index') }}" class="btn btn-primary" style="margin-top: 20px;">Go to Dashboard</a>
</div>
{% endblock %}'''
    }

    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)

    # Write all templates
    for filename, content in templates.items():
        filepath = os.path.join('templates', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created: {filepath}")

    print(f"\n🎉 Successfully created {len(templates)} template files!")
    print("\nNext steps:")
    print("1. Run: python web_app.py")
    print("2. Open: http://localhost:5000")
    print("3. Test all features")
    print("4. Deploy to Render.com or Heroku")

if __name__ == "__main__":
    create_templates()

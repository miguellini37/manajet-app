"""
Updated Template Generator Part 2 - Flight, Maintenance, and Dashboard templates
Run this after part 1
"""

import os

def create_templates():
    """Generate remaining templates"""

    templates = {
        'flights.html': '''{% extends "base.html" %}
{% block content %}
<h1>Flights</h1>
<a href="{{ url_for('add_flight') }}" class="btn btn-primary" style="margin-bottom: 20px;">✈️ Schedule New Flight</a>
<table>
    <thead>
        <tr>
            <th>Flight ID</th><th>Jet</th><th>Route</th><th>Departure</th><th>Arrival</th><th>Passengers</th><th>Crew</th><th>Status</th><th>Actions</th>
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
            <td>{{ flight.crew_ids|length }}</td>
            <td><span class="status-badge status-{{ flight.status.lower().replace(' ', '-') }}">{{ flight.status }}</span></td>
            <td>
                <a href="{{ url_for('view_flight', flight_id=flight.flight_id) }}" class="btn btn-primary">View</a>
                <a href="{{ url_for('edit_flight', flight_id=flight.flight_id) }}" class="btn btn-success">Edit</a>
                <form method="POST" action="{{ url_for('delete_flight', flight_id=flight.flight_id) }}" style="display:inline;" onsubmit="return confirm('Delete this flight?');">
                    <button type="submit" class="btn btn-danger">Delete</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}''',

        'flight_form.html': '''{% extends "base.html" %}
{% block content %}
<h1>{% if edit_mode %}Edit{% else %}Schedule{% endif %} Flight</h1>
<form method="POST" class="card">
    <div class="form-group">
        <label>Jet *</label>
        <select name="jet_id" required>
            <option value="">Select a jet...</option>
            {% for jet in jets %}
            <option value="{{ jet.jet_id }}" {% if flight and flight.jet_id == jet.jet_id %}selected{% endif %}>
                {{ jet.model }} ({{ jet.tail_number }}) - {{ jet.status }}
            </option>
            {% endfor %}
        </select>
    </div>
    <div class="grid-2">
        <div class="form-group">
            <label>Departure Airport *</label>
            <input type="text" name="departure" value="{{ flight.departure if flight else '' }}" placeholder="e.g., KTEB" required>
        </div>
        <div class="form-group">
            <label>Destination Airport *</label>
            <input type="text" name="destination" value="{{ flight.destination if flight else '' }}" placeholder="e.g., KLAX" required>
        </div>
    </div>
    <div class="grid-2">
        <div class="form-group">
            <label>Departure Time *</label>
            <input type="datetime-local" name="departure_time" value="{{ flight.departure_time.replace(' ', 'T') if flight else '' }}" required>
        </div>
        <div class="form-group">
            <label>Arrival Time *</label>
            <input type="datetime-local" name="arrival_time" value="{{ flight.arrival_time.replace(' ', 'T') if flight else '' }}" required>
        </div>
    </div>
    <div class="form-group">
        <label>Crew Members (comma-separated IDs) *</label>
        <input type="text" name="crew_ids" value="{{ ', '.join(flight.crew_ids) if flight else '' }}" placeholder="e.g., CREW001, CREW002" required>
        <small>Available crew: {% for c in crew %}{{ c.crew_id }} ({{ c.name }} - {{ c.crew_type }}){% if not loop.last %}, {% endif %}{% endfor %}</small>
        <small style="display:block; margin-top:5px; color:#e74c3c;"><strong>⚠️ Required: At least 1 pilot!</strong></small>
    </div>
    <div class="form-group">
        <label>Passenger IDs (comma-separated)</label>
        <input type="text" name="passenger_ids" value="{{ ', '.join(flight.passenger_ids) if flight else '' }}" placeholder="e.g., P001, P002">
        <small>Available passengers: {% for p in passengers %}{{ p.passenger_id }} ({{ p.name }}){% if not loop.last %}, {% endif %}{% endfor %}</small>
    </div>
    {% if edit_mode %}
    <div class="form-group">
        <label>Status</label>
        <select name="status">
            <option value="Scheduled" {% if flight and flight.status == 'Scheduled' %}selected{% endif %}>Scheduled</option>
            <option value="In Progress" {% if flight and flight.status == 'In Progress' %}selected{% endif %}>In Progress</option>
            <option value="Completed" {% if flight and flight.status == 'Completed' %}selected{% endif %}>Completed</option>
            <option value="Cancelled" {% if flight and flight.status == 'Cancelled' %}selected{% endif %}>Cancelled</option>
        </select>
    </div>
    {% endif %}
    <button type="submit" class="btn btn-success">{% if edit_mode %}Update{% else %}Schedule{% endif %} Flight</button>
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
    <div style="margin-top: 20px;">
        <a href="{{ url_for('edit_flight', flight_id=flight.flight_id) }}" class="btn btn-success">Edit Flight</a>
        <form method="POST" action="{{ url_for('delete_flight', flight_id=flight.flight_id) }}" style="display:inline;" onsubmit="return confirm('Delete this flight? This cannot be undone.');">
            <button type="submit" class="btn btn-danger">Delete Flight</button>
        </form>
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
    <h2>Crew Members ({{ crew|length }})</h2>
    <ul>
        {% for crew_member in crew %}
        <li><strong>{{ crew_member.name }}</strong> ({{ crew_member.crew_id }}) - {{ crew_member.crew_type }}{% if crew_member.license_number %} | License: {{ crew_member.license_number }}{% endif %}</li>
        {% endfor %}
    </ul>
</div>

<div class="card" style="margin-top: 20px;">
    <h2>Passengers ({{ passengers|length }})</h2>
    {% if passengers %}
    <ul>
        {% for passenger in passengers %}
        <li>{{ passenger.name }} ({{ passenger.passenger_id }}) - Passport: {{ passenger.passport_number }}</li>
        {% endfor %}
    </ul>
    {% else %}
    <p>No passengers</p>
    {% endif %}
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
            <td>
                <a href="{{ url_for('view_maintenance', maintenance_id=maint.maintenance_id) }}" class="btn btn-primary">View</a>
                <a href="{{ url_for('edit_maintenance', maintenance_id=maint.maintenance_id) }}" class="btn btn-success">Edit</a>
                <form method="POST" action="{{ url_for('delete_maintenance', maintenance_id=maint.maintenance_id) }}" style="display:inline;" onsubmit="return confirm('Delete this maintenance record?');">
                    <button type="submit" class="btn btn-danger">Delete</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}''',

        'maintenance_form.html': '''{% extends "base.html" %}
{% block content %}
<h1>{% if edit_mode %}Edit{% else %}Schedule{% endif %} Maintenance</h1>
<form method="POST" class="card">
    <div class="form-group">
        <label>Jet *</label>
        <select name="jet_id" required>
            <option value="">Select a jet...</option>
            {% for jet in jets %}
            <option value="{{ jet.jet_id }}" {% if maintenance and maintenance.jet_id == jet.jet_id %}selected{% endif %}>
                {{ jet.model }} ({{ jet.tail_number }}) - {{ jet.status }}
            </option>
            {% endfor %}
        </select>
    </div>
    <div class="form-group">
        <label>Scheduled Date *</label>
        <input type="date" name="scheduled_date" value="{{ maintenance.scheduled_date if maintenance else '' }}" required>
    </div>
    <div class="form-group">
        <label>Maintenance Type *</label>
        <select name="maintenance_type" required>
            <option value="Routine" {% if maintenance and maintenance.maintenance_type == 'Routine' %}selected{% endif %}>Routine</option>
            <option value="Emergency" {% if maintenance and maintenance.maintenance_type == 'Emergency' %}selected{% endif %}>Emergency</option>
            <option value="Inspection" {% if maintenance and maintenance.maintenance_type == 'Inspection' %}selected{% endif %}>Inspection</option>
        </select>
    </div>
    <div class="form-group">
        <label>Description *</label>
        <textarea name="description" rows="4" required>{{ maintenance.description if maintenance else '' }}</textarea>
    </div>
    {% if edit_mode %}
    <div class="form-group">
        <label>Status</label>
        <select name="status">
            <option value="Scheduled" {% if maintenance and maintenance.status == 'Scheduled' %}selected{% endif %}>Scheduled</option>
            <option value="In Progress" {% if maintenance and maintenance.status == 'In Progress' %}selected{% endif %}>In Progress</option>
            <option value="Completed" {% if maintenance and maintenance.status == 'Completed' %}selected{% endif %}>Completed</option>
        </select>
    </div>
    <div class="form-group">
        <label>Completed Date (if completed)</label>
        <input type="date" name="completed_date" value="{{ maintenance.completed_date if maintenance and maintenance.completed_date else '' }}">
    </div>
    {% endif %}
    <button type="submit" class="btn btn-success">{% if edit_mode %}Update{% else %}Schedule{% endif %} Maintenance</button>
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
    <div style="margin-top: 20px;">
        <a href="{{ url_for('edit_maintenance', maintenance_id=maintenance.maintenance_id) }}" class="btn btn-success">Edit Maintenance</a>
        <form method="POST" action="{{ url_for('delete_maintenance', maintenance_id=maintenance.maintenance_id) }}" style="display:inline;" onsubmit="return confirm('Delete this maintenance record? This cannot be undone.');">
            <button type="submit" class="btn btn-danger">Delete Maintenance</button>
        </form>
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

        'dashboard.html': '''{% extends "base.html" %}
{% block title %}Dashboard - Private Jet Manager{% endblock %}
{% block content %}
<h1 style="margin-bottom: 30px; color: #2c3e50;">Dashboard Overview</h1>

<div class="grid-4">
    <div class="card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
        <h3 style="color: white; font-size: 36px; margin-bottom: 10px;">{{ stats.total_passengers }}</h3>
        <p style="opacity: 0.9;">Total Passengers</p>
    </div>

    <div class="card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
        <h3 style="color: white; font-size: 36px; margin-bottom: 10px;">{{ stats.total_crew }}</h3>
        <p style="opacity: 0.9;">Crew Members</p>
    </div>

    <div class="card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;">
        <h3 style="color: white; font-size: 36px; margin-bottom: 10px;">{{ stats.total_jets }}</h3>
        <p style="opacity: 0.9;">Total Jets</p>
    </div>

    <div class="card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white;">
        <h3 style="color: white; font-size: 36px; margin-bottom: 10px;">{{ stats.total_flights }}</h3>
        <p style="opacity: 0.9;">Total Flights</p>
    </div>
</div>

<div class="grid-2" style="margin-top: 30px;">
    <div class="card">
        <h2>🛫 Active Operations</h2>
        <div style="margin-top: 20px;">
            <p style="font-size: 18px; margin-bottom: 10px;">
                <strong>Active Flights:</strong>
                <span style="color: #3498db; font-size: 24px; font-weight: bold;">{{ stats.active_flights }}</span>
            </p>
            <p style="font-size: 18px;">
                <strong>Available Jets:</strong>
                <span style="color: #27ae60; font-size: 24px; font-weight: bold;">{{ stats.available_jets }}</span>
            </p>
        </div>
    </div>

    <div class="card">
        <h2>⚡ Quick Actions</h2>
        <div style="margin-top: 20px; display: flex; flex-direction: column; gap: 15px;">
            <a href="{{ url_for('add_passenger') }}" class="btn btn-primary" style="text-align: center;">➕ Add Passenger</a>
            <a href="{{ url_for('add_crew') }}" class="btn btn-primary" style="text-align: center;">👨‍✈️ Add Crew Member</a>
            <a href="{{ url_for('add_jet') }}" class="btn btn-primary" style="text-align: center;">➕ Add Jet</a>
            <a href="{{ url_for('add_flight') }}" class="btn btn-success" style="text-align: center;">✈️ Schedule Flight</a>
            <a href="{{ url_for('add_maintenance') }}" class="btn btn-secondary" style="text-align: center;">🔧 Schedule Maintenance</a>
        </div>
    </div>
</div>

<div class="card" style="margin-top: 30px;">
    <h2>📊 System Information</h2>
    <p style="margin-top: 15px; color: #7f8c8d;">
        This dashboard provides an overview of your private jet operations.
        Use the navigation menu above to manage passengers, crew, jets, flights, and maintenance schedules.
    </p>
    <p style="margin-top: 10px; color: #7f8c8d;">
        <strong>✨ New Features:</strong> Crew management with pilot licensing, full edit/delete capabilities for all records, and automatic status synchronization.
    </p>
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
        print(f"✅ Created/Updated: {filepath}")

    print(f"\n🎉 Successfully created/updated {len(templates)} template files (Part 2/2)!")
    print("\n✅ All templates complete! Your web app is ready.")
    print("\nNext steps:")
    print("1. Run: python web_app.py")
    print("2. Open: http://localhost:5000")
    print("3. Test crew management and edit functionality!")

if __name__ == "__main__":
    create_templates()

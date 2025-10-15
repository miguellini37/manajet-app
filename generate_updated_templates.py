"""
Updated Template Generator - Includes Crew Management and Edit/Delete Functionality
Run this to update all HTML templates with new features
"""

import os

def create_templates():
    """Generate all necessary HTML templates with crew and edit functionality"""

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
            <td>
                <a href="{{ url_for('view_passenger', passenger_id=passenger.passenger_id) }}" class="btn btn-primary">View</a>
                <a href="{{ url_for('edit_passenger', passenger_id=passenger.passenger_id) }}" class="btn btn-success">Edit</a>
                <form method="POST" action="{{ url_for('delete_passenger', passenger_id=passenger.passenger_id) }}" style="display:inline;" onsubmit="return confirm('Delete this passenger?');">
                    <button type="submit" class="btn btn-danger">Delete</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}''',

        'passenger_form.html': '''{% extends "base.html" %}
{% block content %}
<h1>{% if edit_mode %}Edit{% else %}Add{% endif %} Passenger</h1>
<form method="POST" class="card">
    <div class="form-group">
        <label>Full Name *</label>
        <input type="text" name="name" value="{{ passenger.name if passenger else '' }}" required>
    </div>
    <div class="form-group">
        <label>Passport Number *</label>
        <input type="text" name="passport_number" value="{{ passenger.passport_number if passenger else '' }}" required>
    </div>
    <div class="form-group">
        <label>Nationality *</label>
        <input type="text" name="nationality" value="{{ passenger.nationality if passenger else '' }}" required>
    </div>
    <div class="form-group">
        <label>Passport Expiry Date *</label>
        <input type="date" name="passport_expiry" value="{{ passenger.passport_expiry if passenger else '' }}" required>
    </div>
    <div class="form-group">
        <label>Contact (Email/Phone) *</label>
        <input type="text" name="contact" value="{{ passenger.contact if passenger else '' }}" required>
    </div>
    <button type="submit" class="btn btn-success">{% if edit_mode %}Update{% else %}Add{% endif %} Passenger</button>
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
    <div style="margin-top: 20px;">
        <a href="{{ url_for('edit_passenger', passenger_id=passenger.passenger_id) }}" class="btn btn-success">Edit Passenger</a>
        <form method="POST" action="{{ url_for('delete_passenger', passenger_id=passenger.passenger_id) }}" style="display:inline;" onsubmit="return confirm('Delete this passenger? This cannot be undone.');">
            <button type="submit" class="btn btn-danger">Delete Passenger</button>
        </form>
    </div>
</div>
{% endblock %}''',

        'crew.html': '''{% extends "base.html" %}
{% block content %}
<h1>Crew Members</h1>
<a href="{{ url_for('add_crew') }}" class="btn btn-primary" style="margin-bottom: 20px;">➕ Add New Crew Member</a>
<table>
    <thead>
        <tr>
            <th>ID</th><th>Name</th><th>Type</th><th>Passport</th><th>Nationality</th><th>License</th><th>Expiry</th><th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for crew_member in crew %}
        <tr>
            <td>{{ crew_member.crew_id }}</td>
            <td>{{ crew_member.name }}</td>
            <td><span class="status-badge {% if crew_member.crew_type == 'Pilot' %}status-in-progress{% else %}status-available{% endif %}">{{ crew_member.crew_type }}</span></td>
            <td>{{ crew_member.passport_number }}</td>
            <td>{{ crew_member.nationality }}</td>
            <td>{{ crew_member.license_number or 'N/A' }}</td>
            <td>{{ crew_member.passport_expiry }}</td>
            <td>
                <a href="{{ url_for('view_crew', crew_id=crew_member.crew_id) }}" class="btn btn-primary">View</a>
                <a href="{{ url_for('edit_crew', crew_id=crew_member.crew_id) }}" class="btn btn-success">Edit</a>
                <form method="POST" action="{{ url_for('delete_crew', crew_id=crew_member.crew_id) }}" style="display:inline;" onsubmit="return confirm('Delete this crew member?');">
                    <button type="submit" class="btn btn-danger">Delete</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}''',

        'crew_form.html': '''{% extends "base.html" %}
{% block content %}
<h1>{% if edit_mode %}Edit{% else %}Add{% endif %} Crew Member</h1>
<form method="POST" class="card">
    <div class="form-group">
        <label>Full Name *</label>
        <input type="text" name="name" value="{{ crew.name if crew else '' }}" required>
    </div>
    <div class="form-group">
        <label>Crew Type *</label>
        <select name="crew_type" required onchange="toggleLicenseField(this)">
            <option value="">Select type...</option>
            <option value="Pilot" {% if crew and crew.crew_type == 'Pilot' %}selected{% endif %}>Pilot</option>
            <option value="Cabin Crew" {% if crew and crew.crew_type == 'Cabin Crew' %}selected{% endif %}>Cabin Crew</option>
        </select>
    </div>
    <div class="form-group" id="license-group" {% if not crew or crew.crew_type != 'Pilot' %}style="display:none;"{% endif %}>
        <label>License Number *</label>
        <input type="text" name="license_number" id="license_number" value="{{ crew.license_number if crew else '' }}">
        <small>Required for pilots</small>
    </div>
    <div class="form-group">
        <label>Passport Number *</label>
        <input type="text" name="passport_number" value="{{ crew.passport_number if crew else '' }}" required>
    </div>
    <div class="form-group">
        <label>Nationality *</label>
        <input type="text" name="nationality" value="{{ crew.nationality if crew else '' }}" required>
    </div>
    <div class="form-group">
        <label>Passport Expiry Date *</label>
        <input type="date" name="passport_expiry" value="{{ crew.passport_expiry if crew else '' }}" required>
    </div>
    <div class="form-group">
        <label>Contact (Email/Phone) *</label>
        <input type="text" name="contact" value="{{ crew.contact if crew else '' }}" required>
    </div>
    <button type="submit" class="btn btn-success">{% if edit_mode %}Update{% else %}Add{% endif %} Crew Member</button>
    <a href="{{ url_for('crew') }}" class="btn btn-secondary">Cancel</a>
</form>

<script>
function toggleLicenseField(select) {
    const licenseGroup = document.getElementById('license-group');
    const licenseInput = document.getElementById('license_number');
    if (select.value === 'Pilot') {
        licenseGroup.style.display = 'block';
        licenseInput.required = true;
    } else {
        licenseGroup.style.display = 'none';
        licenseInput.required = false;
    }
}
</script>
{% endblock %}''',

        'crew_detail.html': '''{% extends "base.html" %}
{% block content %}
<a href="{{ url_for('crew') }}" class="btn btn-secondary" style="margin-bottom: 20px;">← Back to Crew</a>
<div class="card">
    <h1>{{ crew.name }}</h1>
    <div style="margin-top: 20px;">
        <p><strong>Crew ID:</strong> {{ crew.crew_id }}</p>
        <p><strong>Type:</strong> <span class="status-badge {% if crew.crew_type == 'Pilot' %}status-in-progress{% else %}status-available{% endif %}">{{ crew.crew_type }}</span></p>
        {% if crew.license_number %}
        <p><strong>License Number:</strong> {{ crew.license_number }}</p>
        {% endif %}
        <p><strong>Passport Number:</strong> {{ crew.passport_number }}</p>
        <p><strong>Nationality:</strong> {{ crew.nationality }}</p>
        <p><strong>Passport Expiry:</strong> {{ crew.passport_expiry }}</p>
        <p><strong>Contact:</strong> {{ crew.contact }}</p>
    </div>
    <div style="margin-top: 20px;">
        <a href="{{ url_for('edit_crew', crew_id=crew.crew_id) }}" class="btn btn-success">Edit Crew Member</a>
        <form method="POST" action="{{ url_for('delete_crew', crew_id=crew.crew_id) }}" style="display:inline;" onsubmit="return confirm('Delete this crew member? This cannot be undone.');">
            <button type="submit" class="btn btn-danger">Delete Crew Member</button>
        </form>
    </div>
</div>

{% if flights %}
<div class="card" style="margin-top: 20px;">
    <h2>Assigned Flights</h2>
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
</div>
{% endif %}
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
            <td>
                <a href="{{ url_for('view_jet', jet_id=jet.jet_id) }}" class="btn btn-primary">View Schedule</a>
                <a href="{{ url_for('edit_jet', jet_id=jet.jet_id) }}" class="btn btn-success">Edit</a>
                <form method="POST" action="{{ url_for('delete_jet', jet_id=jet.jet_id) }}" style="display:inline;" onsubmit="return confirm('Delete this jet?');">
                    <button type="submit" class="btn btn-danger">Delete</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}''',

        'jet_form.html': '''{% extends "base.html" %}
{% block content %}
<h1>{% if edit_mode %}Edit{% else %}Add{% endif %} Jet</h1>
<form method="POST" class="card">
    <div class="form-group">
        <label>Jet Model *</label>
        <input type="text" name="model" value="{{ jet.model if jet else '' }}" placeholder="e.g., Gulfstream G650" required>
    </div>
    <div class="form-group">
        <label>Tail Number *</label>
        <input type="text" name="tail_number" value="{{ jet.tail_number if jet else '' }}" placeholder="e.g., N123AB" required>
    </div>
    <div class="form-group">
        <label>Passenger Capacity *</label>
        <input type="number" name="capacity" value="{{ jet.capacity if jet else '' }}" min="1" max="50" required>
    </div>
    <div class="form-group">
        <label>Status</label>
        <select name="status">
            <option value="Available" {% if jet and jet.status == 'Available' %}selected{% endif %}>Available</option>
            <option value="Maintenance" {% if jet and jet.status == 'Maintenance' %}selected{% endif %}>Maintenance</option>
            <option value="In Flight" {% if jet and jet.status == 'In Flight' %}selected{% endif %}>In Flight</option>
        </select>
    </div>
    <button type="submit" class="btn btn-success">{% if edit_mode %}Update{% else %}Add{% endif %} Jet</button>
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
    <div style="margin-top: 20px;">
        <a href="{{ url_for('edit_jet', jet_id=jet.jet_id) }}" class="btn btn-success">Edit Jet</a>
        <form method="POST" action="{{ url_for('delete_jet', jet_id=jet.jet_id) }}" style="display:inline;" onsubmit="return confirm('Delete this jet? This cannot be undone.');">
            <button type="submit" class="btn btn-danger">Delete Jet</button>
        </form>
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

# Continue in next part...
    }

    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)

    # Write all templates
    for filename, content in templates.items():
        filepath = os.path.join('templates', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created/Updated: {filepath}")

    print(f"\n🎉 Successfully created/updated {len(templates)} template files (Part 1/2)!")
    print("\n⚠️  Run generate_updated_templates_part2.py for remaining templates")

if __name__ == "__main__":
    create_templates()

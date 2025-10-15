"""
Private Jet Schedule Management System
Tracks passengers, flights, and maintenance schedules
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class Customer:
    """Represents a customer who owns one or more jets"""

    def __init__(self, customer_id: str, name: str, company: str,
                 email: str, phone: str, address: str):
        self.customer_id = customer_id
        self.name = name
        self.company = company
        self.email = email
        self.phone = phone
        self.address = address

    def to_dict(self) -> Dict:
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'company': self.company,
            'email': self.email,
            'phone': self.phone,
            'address': self.address
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            data['customer_id'],
            data['name'],
            data['company'],
            data['email'],
            data['phone'],
            data['address']
        )

    def __str__(self) -> str:
        return (f"Customer: {self.name} (ID: {self.customer_id})\n"
                f"  Company: {self.company}\n"
                f"  Email: {self.email}\n"
                f"  Phone: {self.phone}\n"
                f"  Address: {self.address}")


class User:
    """Represents a user with login credentials and role-based access"""

    def __init__(self, user_id: str, username: str, password_hash: str, role: str,
                 related_id: str = "", email: str = ""):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role  # customer, crew, mechanic, admin
        self.related_id = related_id  # Links to customer_id, crew_id, etc.
        self.email = email

    def to_dict(self) -> Dict:
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password_hash': self.password_hash,
            'role': self.role,
            'related_id': self.related_id,
            'email': self.email
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            data['user_id'],
            data['username'],
            data['password_hash'],
            data['role'],
            data.get('related_id', ''),
            data.get('email', '')
        )

    def __str__(self) -> str:
        return (f"User: {self.username} (ID: {self.user_id})\n"
                f"  Role: {self.role}\n"
                f"  Related ID: {self.related_id}\n"
                f"  Email: {self.email}")


class Passenger:
    """Represents a passenger with personal and passport information"""

    def __init__(self, passenger_id: str, name: str, passport_number: str,
                 nationality: str, passport_expiry: str, contact: str, customer_id: str = ""):
        self.passenger_id = passenger_id
        self.name = name
        self.passport_number = passport_number
        self.nationality = nationality
        self.passport_expiry = passport_expiry
        self.contact = contact
        self.customer_id = customer_id  # Associates passenger with a customer

    def to_dict(self) -> Dict:
        return {
            'passenger_id': self.passenger_id,
            'name': self.name,
            'passport_number': self.passport_number,
            'nationality': self.nationality,
            'passport_expiry': self.passport_expiry,
            'contact': self.contact,
            'customer_id': self.customer_id
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            data['passenger_id'],
            data['name'],
            data['passport_number'],
            data['nationality'],
            data['passport_expiry'],
            data['contact'],
            data.get('customer_id', '')  # Backwards compatibility
        )

    def __str__(self) -> str:
        return (f"Passenger: {self.name} (ID: {self.passenger_id})\n"
                f"  Passport: {self.passport_number} ({self.nationality})\n"
                f"  Expiry: {self.passport_expiry}\n"
                f"  Contact: {self.contact}\n"
                f"  Customer ID: {self.customer_id}")


class PrivateJet:
    """Represents a private jet with its specifications"""

    def __init__(self, jet_id: str, model: str, tail_number: str,
                 capacity: int, customer_id: str, status: str = "Available"):
        self.jet_id = jet_id
        self.model = model
        self.tail_number = tail_number
        self.capacity = capacity
        self.customer_id = customer_id
        self.status = status  # Available, In Flight, Maintenance

    def to_dict(self) -> Dict:
        return {
            'jet_id': self.jet_id,
            'model': self.model,
            'tail_number': self.tail_number,
            'capacity': self.capacity,
            'customer_id': self.customer_id,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            data['jet_id'],
            data['model'],
            data['tail_number'],
            data['capacity'],
            data.get('customer_id', ''),  # Backwards compatibility
            data.get('status', 'Available')
        )

    def __str__(self) -> str:
        return (f"Jet: {self.model} (ID: {self.jet_id})\n"
                f"  Tail Number: {self.tail_number}\n"
                f"  Capacity: {self.capacity} passengers\n"
                f"  Customer ID: {self.customer_id}\n"
                f"  Status: {self.status}")


class CrewMember:
    """Represents a crew member (pilot or cabin crew) with passport and license information"""

    def __init__(self, crew_id: str, name: str, crew_type: str, passport_number: str,
                 nationality: str, passport_expiry: str, contact: str,
                 license_number: Optional[str] = None):
        self.crew_id = crew_id
        self.name = name
        self.crew_type = crew_type  # Pilot or Cabin Crew
        self.passport_number = passport_number
        self.nationality = nationality
        self.passport_expiry = passport_expiry
        self.contact = contact
        self.license_number = license_number  # Required for pilots

    def to_dict(self) -> Dict:
        return {
            'crew_id': self.crew_id,
            'name': self.name,
            'crew_type': self.crew_type,
            'passport_number': self.passport_number,
            'nationality': self.nationality,
            'passport_expiry': self.passport_expiry,
            'contact': self.contact,
            'license_number': self.license_number
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            data['crew_id'],
            data['name'],
            data['crew_type'],
            data['passport_number'],
            data['nationality'],
            data['passport_expiry'],
            data['contact'],
            data.get('license_number')
        )

    def __str__(self) -> str:
        result = (f"Crew Member: {self.name} (ID: {self.crew_id})\n"
                 f"  Type: {self.crew_type}\n"
                 f"  Passport: {self.passport_number} ({self.nationality})\n"
                 f"  Expiry: {self.passport_expiry}\n"
                 f"  Contact: {self.contact}")
        if self.license_number:
            result += f"\n  License: {self.license_number}"
        return result


class Flight:
    """Represents a scheduled flight"""

    def __init__(self, flight_id: str, jet_id: str, departure: str,
                 destination: str, departure_time: str, arrival_time: str,
                 passenger_ids: List[str], crew_ids: List[str],
                 status: str = "Scheduled"):
        self.flight_id = flight_id
        self.jet_id = jet_id
        self.departure = departure
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.passenger_ids = passenger_ids
        self.crew_ids = crew_ids
        self.status = status  # Scheduled, In Progress, Completed, Cancelled

    def to_dict(self) -> Dict:
        return {
            'flight_id': self.flight_id,
            'jet_id': self.jet_id,
            'departure': self.departure,
            'destination': self.destination,
            'departure_time': self.departure_time,
            'arrival_time': self.arrival_time,
            'passenger_ids': self.passenger_ids,
            'crew_ids': self.crew_ids,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            data['flight_id'],
            data['jet_id'],
            data['departure'],
            data['destination'],
            data['departure_time'],
            data['arrival_time'],
            data['passenger_ids'],
            data.get('crew_ids', []),  # Backwards compatibility
            data.get('status', 'Scheduled')
        )

    def __str__(self) -> str:
        return (f"Flight: {self.flight_id} - {self.status}\n"
                f"  Route: {self.departure} → {self.destination}\n"
                f"  Departure: {self.departure_time}\n"
                f"  Arrival: {self.arrival_time}\n"
                f"  Jet ID: {self.jet_id}\n"
                f"  Passengers: {len(self.passenger_ids)}\n"
                f"  Crew Members: {len(self.crew_ids)}")


class MaintenanceRecord:
    """Represents a maintenance record for a jet"""

    def __init__(self, maintenance_id: str, jet_id: str, scheduled_date: str,
                 maintenance_type: str, description: str, status: str = "Scheduled",
                 completed_date: Optional[str] = None):
        self.maintenance_id = maintenance_id
        self.jet_id = jet_id
        self.scheduled_date = scheduled_date
        self.maintenance_type = maintenance_type
        self.description = description
        self.status = status  # Scheduled, In Progress, Completed
        self.completed_date = completed_date

    def to_dict(self) -> Dict:
        return {
            'maintenance_id': self.maintenance_id,
            'jet_id': self.jet_id,
            'scheduled_date': self.scheduled_date,
            'maintenance_type': self.maintenance_type,
            'description': self.description,
            'status': self.status,
            'completed_date': self.completed_date
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            data['maintenance_id'],
            data['jet_id'],
            data['scheduled_date'],
            data['maintenance_type'],
            data['description'],
            data.get('status', 'Scheduled'),
            data.get('completed_date')
        )

    def __str__(self) -> str:
        result = (f"Maintenance: {self.maintenance_id} - {self.status}\n"
                 f"  Jet ID: {self.jet_id}\n"
                 f"  Type: {self.maintenance_type}\n"
                 f"  Scheduled: {self.scheduled_date}\n"
                 f"  Description: {self.description}")
        if self.completed_date:
            result += f"\n  Completed: {self.completed_date}"
        return result


class JetScheduleManager:
    """Main manager class for the private jet scheduling system"""

    def __init__(self, data_file: str = "jet_schedule_data.json"):
        self.data_file = data_file
        self.users: Dict[str, User] = {}
        self.customers: Dict[str, Customer] = {}
        self.passengers: Dict[str, Passenger] = {}
        self.crew: Dict[str, CrewMember] = {}
        self.jets: Dict[str, PrivateJet] = {}
        self.flights: Dict[str, Flight] = {}
        self.maintenance: Dict[str, MaintenanceRecord] = {}
        self.load_data()

    def _generate_next_id(self, prefix: str, existing_dict: Dict) -> str:
        """Generate next available ID with given prefix"""
        if not existing_dict:
            return f"{prefix}001"

        # Extract numeric parts from existing IDs with this prefix
        numbers = []
        for key in existing_dict.keys():
            if key.startswith(prefix):
                try:
                    num = int(key[len(prefix):])
                    numbers.append(num)
                except ValueError:
                    continue

        # Find next number
        next_num = max(numbers) + 1 if numbers else 1
        return f"{prefix}{next_num:03d}"

    def generate_user_id(self) -> str:
        """Generate next available user ID"""
        return self._generate_next_id("USER", self.users)

    def generate_customer_id(self) -> str:
        """Generate next available customer ID"""
        return self._generate_next_id("CUST", self.customers)

    def generate_passenger_id(self) -> str:
        """Generate next available passenger ID"""
        return self._generate_next_id("P", self.passengers)

    def generate_crew_id(self) -> str:
        """Generate next available crew ID"""
        return self._generate_next_id("CREW", self.crew)

    def generate_jet_id(self) -> str:
        """Generate next available jet ID"""
        return self._generate_next_id("JET", self.jets)

    def generate_flight_id(self) -> str:
        """Generate next available flight ID"""
        return self._generate_next_id("FL", self.flights)

    def generate_maintenance_id(self) -> str:
        """Generate next available maintenance ID"""
        return self._generate_next_id("MAINT", self.maintenance)

    def save_data(self):
        """Save all data to JSON file"""
        data = {
            'users': {k: v.to_dict() for k, v in self.users.items()},
            'customers': {k: v.to_dict() for k, v in self.customers.items()},
            'passengers': {k: v.to_dict() for k, v in self.passengers.items()},
            'crew': {k: v.to_dict() for k, v in self.crew.items()},
            'jets': {k: v.to_dict() for k, v in self.jets.items()},
            'flights': {k: v.to_dict() for k, v in self.flights.items()},
            'maintenance': {k: v.to_dict() for k, v in self.maintenance.items()}
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {self.data_file}")

    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)

            self.users = {k: User.from_dict(v) for k, v in data.get('users', {}).items()}
            self.customers = {k: Customer.from_dict(v) for k, v in data.get('customers', {}).items()}
            self.passengers = {k: Passenger.from_dict(v) for k, v in data.get('passengers', {}).items()}
            self.crew = {k: CrewMember.from_dict(v) for k, v in data.get('crew', {}).items()}
            self.jets = {k: PrivateJet.from_dict(v) for k, v in data.get('jets', {}).items()}
            self.flights = {k: Flight.from_dict(v) for k, v in data.get('flights', {}).items()}
            self.maintenance = {k: MaintenanceRecord.from_dict(v) for k, v in data.get('maintenance', {}).items()}
            print(f"Data loaded from {self.data_file}")

    # User Management
    def add_user(self, user_id: str, username: str, password_hash: str, role: str,
                related_id: str = "", email: str = "") -> str:
        """Add a new user. Returns the user ID (auto-generated if empty)"""
        if not user_id or user_id.strip() == "":
            user_id = self.generate_user_id()

        if user_id in self.users:
            print(f"Error: User ID {user_id} already exists")
            return ""

        # Check if username already exists
        if any(u.username == username for u in self.users.values()):
            print(f"Error: Username {username} already exists")
            return ""

        user = User(user_id, username, password_hash, role, related_id, email)
        self.users[user_id] = user
        print(f"User {username} added successfully with ID: {user_id}")
        return user_id

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    def update_user(self, user_id: str, username: str, password_hash: str, role: str,
                   related_id: str = "", email: str = "") -> bool:
        """Update an existing user"""
        if user_id not in self.users:
            print(f"Error: User ID {user_id} not found")
            return False

        self.users[user_id] = User(user_id, username, password_hash, role, related_id, email)
        print(f"User {user_id} updated successfully")
        return True

    def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        if user_id not in self.users:
            print(f"Error: User ID {user_id} not found")
            return False

        del self.users[user_id]
        print(f"User {user_id} deleted successfully")
        return True

    # Customer Management
    def add_customer(self, customer_id: str, name: str, company: str,
                    email: str, phone: str, address: str) -> str:
        """Add a new customer. Returns the customer ID (auto-generated if empty)"""
        if not customer_id or customer_id.strip() == "":
            customer_id = self.generate_customer_id()

        if customer_id in self.customers:
            print(f"Error: Customer ID {customer_id} already exists")
            return ""

        customer = Customer(customer_id, name, company, email, phone, address)
        self.customers[customer_id] = customer
        print(f"Customer {name} added successfully with ID: {customer_id}")
        return customer_id

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID"""
        return self.customers.get(customer_id)

    def update_customer(self, customer_id: str, name: str, company: str,
                       email: str, phone: str, address: str) -> bool:
        """Update an existing customer"""
        if customer_id not in self.customers:
            print(f"Error: Customer ID {customer_id} not found")
            return False

        self.customers[customer_id] = Customer(customer_id, name, company, email, phone, address)
        print(f"Customer {customer_id} updated successfully")
        return True

    def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer"""
        if customer_id not in self.customers:
            print(f"Error: Customer ID {customer_id} not found")
            return False

        # Check if customer has jets
        customer_jets = [j for j in self.jets.values() if j.customer_id == customer_id]
        if customer_jets:
            print(f"Warning: Customer {customer_id} has {len(customer_jets)} jet(s)")
            print(f"  Jet IDs: {', '.join([j.jet_id for j in customer_jets])}")
            return False

        # Check if customer has passengers
        customer_passengers = [p for p in self.passengers.values() if p.customer_id == customer_id]
        if customer_passengers:
            print(f"Warning: Customer {customer_id} has {len(customer_passengers)} passenger(s)")
            return False

        del self.customers[customer_id]
        print(f"Customer {customer_id} deleted successfully")
        return True

    def list_customers(self):
        """List all customers"""
        if not self.customers:
            print("No customers registered")
            return

        print(f"\n{'='*60}")
        print(f"REGISTERED CUSTOMERS ({len(self.customers)})")
        print(f"{'='*60}")
        for customer in self.customers.values():
            print(f"\n{customer}")
            print(f"{'-'*60}")

    def get_customer_jets(self, customer_id: str) -> List[PrivateJet]:
        """Get all jets owned by a customer"""
        return [j for j in self.jets.values() if j.customer_id == customer_id]

    # Passenger Management
    def add_passenger(self, passenger_id: str, name: str, passport_number: str,
                     nationality: str, passport_expiry: str, contact: str, customer_id: str = "") -> str:
        """Add a new passenger. Returns the passenger ID (auto-generated if empty)"""
        # Auto-generate ID if not provided or empty
        if not passenger_id or passenger_id.strip() == "":
            passenger_id = self.generate_passenger_id()

        if passenger_id in self.passengers:
            print(f"Error: Passenger ID {passenger_id} already exists")
            return ""

        passenger = Passenger(passenger_id, name, passport_number,
                            nationality, passport_expiry, contact, customer_id)
        self.passengers[passenger_id] = passenger
        print(f"Passenger {name} added successfully with ID: {passenger_id}")
        return passenger_id

    def get_passenger(self, passenger_id: str) -> Optional[Passenger]:
        """Get passenger by ID"""
        return self.passengers.get(passenger_id)

    def update_passenger(self, passenger_id: str, name: str, passport_number: str,
                        nationality: str, passport_expiry: str, contact: str, customer_id: str = "") -> bool:
        """Update an existing passenger"""
        if passenger_id not in self.passengers:
            print(f"Error: Passenger ID {passenger_id} not found")
            return False

        self.passengers[passenger_id] = Passenger(passenger_id, name, passport_number,
                                                  nationality, passport_expiry, contact, customer_id)
        print(f"Passenger {passenger_id} updated successfully")
        return True

    def delete_passenger(self, passenger_id: str) -> bool:
        """Delete a passenger"""
        if passenger_id not in self.passengers:
            print(f"Error: Passenger ID {passenger_id} not found")
            return False

        # Check if passenger is assigned to any flights
        assigned_flights = [f for f in self.flights.values() if passenger_id in f.passenger_ids]
        if assigned_flights:
            print(f"Warning: Passenger {passenger_id} is assigned to {len(assigned_flights)} flight(s)")
            print(f"  Flight IDs: {', '.join([f.flight_id for f in assigned_flights])}")
            return False

        del self.passengers[passenger_id]
        print(f"Passenger {passenger_id} deleted successfully")
        return True

    def list_passengers(self):
        """List all passengers"""
        if not self.passengers:
            print("No passengers registered")
            return

        print(f"\n{'='*60}")
        print(f"REGISTERED PASSENGERS ({len(self.passengers)})")
        print(f"{'='*60}")
        for passenger in self.passengers.values():
            print(f"\n{passenger}")
            print(f"{'-'*60}")

    # Crew Management
    def add_crew(self, crew_id: str, name: str, crew_type: str, passport_number: str,
                nationality: str, passport_expiry: str, contact: str,
                license_number: Optional[str] = None) -> str:
        """Add a new crew member. Returns the crew ID (auto-generated if empty)"""
        # Auto-generate ID if not provided or empty
        if not crew_id or crew_id.strip() == "":
            crew_id = self.generate_crew_id()

        if crew_id in self.crew:
            print(f"Error: Crew ID {crew_id} already exists")
            return ""

        # Validate pilot has license number
        if crew_type == "Pilot" and not license_number:
            print(f"Error: Pilots must have a license number")
            return ""

        crew_member = CrewMember(crew_id, name, crew_type, passport_number,
                                nationality, passport_expiry, contact, license_number)
        self.crew[crew_id] = crew_member
        print(f"Crew member {name} ({crew_type}) added successfully with ID: {crew_id}")
        return crew_id

    def get_crew(self, crew_id: str) -> Optional[CrewMember]:
        """Get crew member by ID"""
        return self.crew.get(crew_id)

    def update_crew(self, crew_id: str, name: str, crew_type: str, passport_number: str,
                   nationality: str, passport_expiry: str, contact: str,
                   license_number: Optional[str] = None) -> bool:
        """Update an existing crew member"""
        if crew_id not in self.crew:
            print(f"Error: Crew ID {crew_id} not found")
            return False

        # Validate pilot has license number
        if crew_type == "Pilot" and not license_number:
            print(f"Error: Pilots must have a license number")
            return False

        self.crew[crew_id] = CrewMember(crew_id, name, crew_type, passport_number,
                                       nationality, passport_expiry, contact, license_number)
        print(f"Crew member {crew_id} updated successfully")
        return True

    def delete_crew(self, crew_id: str) -> bool:
        """Delete a crew member"""
        if crew_id not in self.crew:
            print(f"Error: Crew ID {crew_id} not found")
            return False

        # Check if crew member is assigned to any flights
        assigned_flights = [f for f in self.flights.values() if crew_id in f.crew_ids]
        if assigned_flights:
            print(f"Warning: Crew member {crew_id} is assigned to {len(assigned_flights)} flight(s)")
            print(f"  Flight IDs: {', '.join([f.flight_id for f in assigned_flights])}")
            return False

        del self.crew[crew_id]
        print(f"Crew member {crew_id} deleted successfully")
        return True

    def list_crew(self, crew_type_filter: Optional[str] = None):
        """List all crew members, optionally filtered by type"""
        crew_list = list(self.crew.values())

        if crew_type_filter:
            crew_list = [c for c in crew_list if c.crew_type == crew_type_filter]

        if not crew_list:
            print(f"No crew members found{' of type: ' + crew_type_filter if crew_type_filter else ''}")
            return

        print(f"\n{'='*60}")
        print(f"CREW MEMBERS ({len(crew_list)}){' - ' + crew_type_filter if crew_type_filter else ''}")
        print(f"{'='*60}")
        for crew_member in crew_list:
            print(f"\n{crew_member}")
            print(f"{'-'*60}")

    # Jet Management
    def add_jet(self, jet_id: str, model: str, tail_number: str,
                capacity: int, customer_id: str, status: str = "Available") -> str:
        """Add a new jet. Returns the jet ID (auto-generated if empty)"""
        # Auto-generate ID if not provided or empty
        if not jet_id or jet_id.strip() == "":
            jet_id = self.generate_jet_id()

        if jet_id in self.jets:
            print(f"Error: Jet ID {jet_id} already exists")
            return ""

        # Validate customer exists
        if customer_id and customer_id not in self.customers:
            print(f"Error: Customer ID {customer_id} not found")
            return ""

        jet = PrivateJet(jet_id, model, tail_number, capacity, customer_id, status)
        self.jets[jet_id] = jet
        print(f"Jet {model} added successfully with ID: {jet_id}")
        return jet_id

    def get_jet(self, jet_id: str) -> Optional[PrivateJet]:
        """Get jet by ID"""
        return self.jets.get(jet_id)

    def list_jets(self):
        """List all jets"""
        if not self.jets:
            print("No jets registered")
            return

        print(f"\n{'='*60}")
        print(f"REGISTERED JETS ({len(self.jets)})")
        print(f"{'='*60}")
        for jet in self.jets.values():
            print(f"\n{jet}")
            print(f"{'-'*60}")

    # Jet Management (continued)
    def update_jet(self, jet_id: str, model: str, tail_number: str,
                  capacity: int, customer_id: str, status: str) -> bool:
        """Update an existing jet"""
        if jet_id not in self.jets:
            print(f"Error: Jet ID {jet_id} not found")
            return False

        # Validate customer exists
        if customer_id and customer_id not in self.customers:
            print(f"Error: Customer ID {customer_id} not found")
            return False

        self.jets[jet_id] = PrivateJet(jet_id, model, tail_number, capacity, customer_id, status)
        print(f"Jet {jet_id} updated successfully")
        return True

    def delete_jet(self, jet_id: str) -> bool:
        """Delete a jet"""
        if jet_id not in self.jets:
            print(f"Error: Jet ID {jet_id} not found")
            return False

        # Check if jet is assigned to any flights or maintenance
        assigned_flights = [f for f in self.flights.values() if f.jet_id == jet_id]
        assigned_maintenance = [m for m in self.maintenance.values() if m.jet_id == jet_id]

        if assigned_flights or assigned_maintenance:
            print(f"Warning: Jet {jet_id} has {len(assigned_flights)} flight(s) and {len(assigned_maintenance)} maintenance record(s)")
            return False

        del self.jets[jet_id]
        print(f"Jet {jet_id} deleted successfully")
        return True

    # Flight Management
    def schedule_flight(self, flight_id: str, jet_id: str, departure: str,
                       destination: str, departure_time: str, arrival_time: str,
                       passenger_ids: List[str], crew_ids: List[str]) -> str:
        """Schedule a new flight. Returns the flight ID (auto-generated if empty)"""
        # Auto-generate ID if not provided or empty
        if not flight_id or flight_id.strip() == "":
            flight_id = self.generate_flight_id()

        if flight_id in self.flights:
            print(f"Error: Flight ID {flight_id} already exists")
            return ""

        if jet_id not in self.jets:
            print(f"Error: Jet ID {jet_id} not found")
            return ""

        # Require at least one crew member
        if not crew_ids or len(crew_ids) == 0:
            print(f"Error: Flight must have at least one crew member")
            return ""

        # Verify all crew members exist
        for cid in crew_ids:
            if cid not in self.crew:
                print(f"Error: Crew ID {cid} not found")
                return ""

        # Check for at least one pilot
        crew_types = [self.crew[cid].crew_type for cid in crew_ids]
        if "Pilot" not in crew_types:
            print(f"Error: Flight must have at least one pilot")
            return ""

        jet = self.jets[jet_id]

        # Check jet availability status
        if jet.status == "Maintenance":
            active_maintenance = [
                m for m in self.maintenance.values()
                if m.jet_id == jet_id and m.status == "In Progress"
            ]
            if active_maintenance:
                print(f"Warning: Jet {jet_id} is currently in maintenance")
                print(f"  Active maintenance: {', '.join([m.maintenance_id for m in active_maintenance])}")

        if jet.status == "In Flight":
            active_flights = [
                f for f in self.flights.values()
                if f.jet_id == jet_id and f.status == "In Progress"
            ]
            if active_flights:
                print(f"Warning: Jet {jet_id} is currently in flight")
                print(f"  Active flights: {', '.join([f.flight_id for f in active_flights])}")

        if len(passenger_ids) > jet.capacity:
            print(f"Error: Too many passengers ({len(passenger_ids)}) for jet capacity ({jet.capacity})")
            return ""

        for pid in passenger_ids:
            if pid not in self.passengers:
                print(f"Error: Passenger ID {pid} not found")
                return ""

        flight = Flight(flight_id, jet_id, departure, destination,
                       departure_time, arrival_time, passenger_ids, crew_ids)
        self.flights[flight_id] = flight
        print(f"Flight {flight_id} scheduled successfully with {len(crew_ids)} crew member(s)")
        return flight_id

    def update_flight(self, flight_id: str, jet_id: str, departure: str,
                     destination: str, departure_time: str, arrival_time: str,
                     passenger_ids: List[str], crew_ids: List[str], status: str) -> bool:
        """Update an existing flight"""
        if flight_id not in self.flights:
            print(f"Error: Flight ID {flight_id} not found")
            return False

        # Require at least one crew member
        if not crew_ids or len(crew_ids) == 0:
            print(f"Error: Flight must have at least one crew member")
            return False

        # Check for at least one pilot
        crew_types = [self.crew[cid].crew_type for cid in crew_ids if cid in self.crew]
        if "Pilot" not in crew_types:
            print(f"Error: Flight must have at least one pilot")
            return False

        self.flights[flight_id] = Flight(flight_id, jet_id, departure, destination,
                                        departure_time, arrival_time, passenger_ids, crew_ids, status)
        print(f"Flight {flight_id} updated successfully")
        return True

    def delete_flight(self, flight_id: str) -> bool:
        """Delete a flight"""
        if flight_id not in self.flights:
            print(f"Error: Flight ID {flight_id} not found")
            return False

        del self.flights[flight_id]
        print(f"Flight {flight_id} deleted successfully")
        return True

    def get_flight(self, flight_id: str) -> Optional[Flight]:
        """Get flight by ID"""
        return self.flights.get(flight_id)

    def list_flights(self, status_filter: Optional[str] = None):
        """List all flights, optionally filtered by status"""
        flights = list(self.flights.values())

        if status_filter:
            flights = [f for f in flights if f.status == status_filter]

        if not flights:
            print(f"No flights found{' with status: ' + status_filter if status_filter else ''}")
            return

        print(f"\n{'='*60}")
        print(f"FLIGHTS ({len(flights)}){' - ' + status_filter if status_filter else ''}")
        print(f"{'='*60}")
        for flight in flights:
            print(f"\n{flight}")
            print(f"{'-'*60}")

    def update_flight_status(self, flight_id: str, new_status: str) -> bool:
        """Update flight status and synchronize jet status"""
        if flight_id not in self.flights:
            print(f"Error: Flight ID {flight_id} not found")
            return False

        flight = self.flights[flight_id]
        old_status = flight.status
        jet_id = flight.jet_id

        # Update flight status
        flight.status = new_status

        # Synchronize jet status based on flight status
        if jet_id in self.jets:
            jet = self.jets[jet_id]

            if new_status == "In Progress":
                # Flight is active - set jet to In Flight
                jet.status = "In Flight"
                print(f"Flight {flight_id} status updated to {new_status}")
                print(f"→ Jet {jet_id} status automatically updated to 'In Flight'")

            elif new_status in ["Completed", "Cancelled"]:
                # Flight ended - check if there are other active flights for this jet
                other_active_flights = [
                    f for f in self.flights.values()
                    if f.jet_id == jet_id and f.flight_id != flight_id and f.status == "In Progress"
                ]

                if not other_active_flights:
                    # No other active flights, check for active maintenance
                    active_maintenance = [
                        m for m in self.maintenance.values()
                        if m.jet_id == jet_id and m.status == "In Progress"
                    ]

                    if active_maintenance:
                        jet.status = "Maintenance"
                        print(f"Flight {flight_id} status updated to {new_status}")
                        print(f"→ Jet {jet_id} has active maintenance, status remains 'Maintenance'")
                    else:
                        jet.status = "Available"
                        print(f"Flight {flight_id} status updated to {new_status}")
                        print(f"→ Jet {jet_id} status automatically updated to 'Available'")
                else:
                    print(f"Flight {flight_id} status updated to {new_status}")
                    print(f"→ Jet {jet_id} remains 'In Flight' (other active flights exist)")

            elif new_status == "Scheduled":
                # Flight is scheduled - only update jet if it's currently available
                if jet.status == "Available":
                    print(f"Flight {flight_id} status updated to {new_status}")
                    print(f"→ Jet {jet_id} remains 'Available' (flight not yet started)")
                else:
                    print(f"Flight {flight_id} status updated to {new_status}")
        else:
            print(f"Flight {flight_id} status updated to {new_status}")

        return True

    # Maintenance Management
    def schedule_maintenance(self, maintenance_id: str, jet_id: str,
                           scheduled_date: str, maintenance_type: str,
                           description: str) -> str:
        """Schedule maintenance for a jet. Returns the maintenance ID (auto-generated if empty)"""
        # Auto-generate ID if not provided or empty
        if not maintenance_id or maintenance_id.strip() == "":
            maintenance_id = self.generate_maintenance_id()

        if maintenance_id in self.maintenance:
            print(f"Error: Maintenance ID {maintenance_id} already exists")
            return ""

        if jet_id not in self.jets:
            print(f"Error: Jet ID {jet_id} not found")
            return ""

        jet = self.jets[jet_id]

        # Check jet availability status
        if jet.status == "In Flight":
            active_flights = [
                f for f in self.flights.values()
                if f.jet_id == jet_id and f.status == "In Progress"
            ]
            if active_flights:
                print(f"Warning: Jet {jet_id} is currently in flight")
                print(f"  Active flights: {', '.join([f.flight_id for f in active_flights])}")

        if jet.status == "Maintenance":
            active_maintenance = [
                m for m in self.maintenance.values()
                if m.jet_id == jet_id and m.status == "In Progress"
            ]
            if active_maintenance:
                print(f"Warning: Jet {jet_id} already has maintenance in progress")
                print(f"  Active maintenance: {', '.join([m.maintenance_id for m in active_maintenance])}")

        maintenance = MaintenanceRecord(maintenance_id, jet_id, scheduled_date,
                                       maintenance_type, description)
        self.maintenance[maintenance_id] = maintenance
        print(f"Maintenance {maintenance_id} scheduled successfully")
        return maintenance_id

    def update_maintenance(self, maintenance_id: str, jet_id: str, scheduled_date: str,
                          maintenance_type: str, description: str, status: str,
                          completed_date: Optional[str] = None) -> bool:
        """Update an existing maintenance record"""
        if maintenance_id not in self.maintenance:
            print(f"Error: Maintenance ID {maintenance_id} not found")
            return False

        self.maintenance[maintenance_id] = MaintenanceRecord(maintenance_id, jet_id, scheduled_date,
                                                             maintenance_type, description, status, completed_date)
        print(f"Maintenance {maintenance_id} updated successfully")
        return True

    def delete_maintenance(self, maintenance_id: str) -> bool:
        """Delete a maintenance record"""
        if maintenance_id not in self.maintenance:
            print(f"Error: Maintenance ID {maintenance_id} not found")
            return False

        del self.maintenance[maintenance_id]
        print(f"Maintenance {maintenance_id} deleted successfully")
        return True

    def update_maintenance_status(self, maintenance_id: str, new_status: str,
                                  completed_date: Optional[str] = None) -> bool:
        """Update maintenance status and synchronize jet status"""
        if maintenance_id not in self.maintenance:
            print(f"Error: Maintenance ID {maintenance_id} not found")
            return False

        maintenance = self.maintenance[maintenance_id]
        old_status = maintenance.status
        jet_id = maintenance.jet_id

        # Update maintenance status
        maintenance.status = new_status
        if completed_date and new_status == "Completed":
            maintenance.completed_date = completed_date

        # Synchronize jet status based on maintenance status
        if jet_id in self.jets:
            jet = self.jets[jet_id]

            if new_status == "In Progress":
                # Maintenance started - set jet to Maintenance
                jet.status = "Maintenance"
                print(f"Maintenance {maintenance_id} status updated to {new_status}")
                print(f"→ Jet {jet_id} status automatically updated to 'Maintenance'")

            elif new_status == "Completed":
                # Maintenance completed - check if there are other active maintenance tasks
                other_active_maintenance = [
                    m for m in self.maintenance.values()
                    if m.jet_id == jet_id and m.maintenance_id != maintenance_id and m.status == "In Progress"
                ]

                if not other_active_maintenance:
                    # No other active maintenance, check for active flights
                    active_flights = [
                        f for f in self.flights.values()
                        if f.jet_id == jet_id and f.status == "In Progress"
                    ]

                    if active_flights:
                        jet.status = "In Flight"
                        print(f"Maintenance {maintenance_id} status updated to {new_status}")
                        print(f"→ Jet {jet_id} has active flights, status set to 'In Flight'")
                    else:
                        jet.status = "Available"
                        print(f"Maintenance {maintenance_id} status updated to {new_status}")
                        print(f"→ Jet {jet_id} status automatically updated to 'Available'")
                else:
                    print(f"Maintenance {maintenance_id} status updated to {new_status}")
                    print(f"→ Jet {jet_id} remains 'Maintenance' (other maintenance tasks active)")

            elif new_status == "Scheduled":
                # Maintenance is scheduled - check current jet status
                if jet.status == "Available":
                    print(f"Maintenance {maintenance_id} status updated to {new_status}")
                    print(f"→ Jet {jet_id} remains 'Available' (maintenance not yet started)")
                else:
                    print(f"Maintenance {maintenance_id} status updated to {new_status}")
        else:
            print(f"Maintenance {maintenance_id} status updated to {new_status}")

        return True

    def complete_maintenance(self, maintenance_id: str, completed_date: str) -> bool:
        """Mark maintenance as completed (convenience method)"""
        return self.update_maintenance_status(maintenance_id, "Completed", completed_date)

    def list_maintenance(self, jet_id: Optional[str] = None, status_filter: Optional[str] = None):
        """List maintenance records, optionally filtered by jet and/or status"""
        records = list(self.maintenance.values())

        if jet_id:
            records = [m for m in records if m.jet_id == jet_id]

        if status_filter:
            records = [m for m in records if m.status == status_filter]

        if not records:
            print("No maintenance records found")
            return

        print(f"\n{'='*60}")
        print(f"MAINTENANCE RECORDS ({len(records)})")
        print(f"{'='*60}")
        for record in records:
            print(f"\n{record}")
            print(f"{'-'*60}")

    def get_jet_schedule(self, jet_id: str):
        """Get complete schedule for a specific jet including flights and maintenance"""
        if jet_id not in self.jets:
            print(f"Error: Jet ID {jet_id} not found")
            return

        jet = self.jets[jet_id]
        print(f"\n{'='*60}")
        print(f"SCHEDULE FOR JET: {jet.model} ({jet_id})")
        print(f"{'='*60}")
        print(f"\n{jet}\n")

        # Flights
        flights = [f for f in self.flights.values() if f.jet_id == jet_id]
        print(f"\nFLIGHTS ({len(flights)}):")
        print(f"{'-'*60}")
        if flights:
            for flight in flights:
                print(f"\n{flight}")
        else:
            print("No flights scheduled")

        # Maintenance
        maintenance = [m for m in self.maintenance.values() if m.jet_id == jet_id]
        print(f"\n\nMAINTENANCE ({len(maintenance)}):")
        print(f"{'-'*60}")
        if maintenance:
            for record in maintenance:
                print(f"\n{record}")
        else:
            print("No maintenance scheduled")


if __name__ == "__main__":
    print("Private Jet Schedule Management System")
    print("This is the core module. Use jet_manager_cli.py for interactive management.")

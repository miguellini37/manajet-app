"""
Initial Setup Script for Private Jet Manager
Creates admin user, sample customers, crew, and mechanics
Run this ONCE after setting up the application
"""

from jet_manager import JetScheduleManager
import bcrypt
import os

def hash_password(password: str) -> str:
    """Secure password hashing with bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def setup():
    """Create initial data"""
    print("="*60)
    print("PRIVATE JET MANAGER - INITIAL SETUP")
    print("="*60)

    manager = JetScheduleManager()

    # Check if users already exist
    if len(manager.users) > 0:
        print("\nUsers already exist in the system.")
        response = input("Do you want to add more users? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return

    print("\n1. Creating Admin User...")
    admin_password = "admin123"  # Change this!
    admin_user_id = manager.add_user(
        "",
        "admin",
        hash_password(admin_password),
        "admin",
        "",
        "admin@jetmanager.com"
    )
    if admin_user_id:
        print(f"   [OK]Admin user created: admin / {admin_password}")
        print(f"     USER ID: {admin_user_id}")

    print("\n2. Creating Sample Customers...")

    # Customer 1
    cust1_id = manager.add_customer(
        "",
        "John Smith",
        "Smith Enterprises",
        "john@smithent.com",
        "+1-555-0101",
        "123 Business Ave, New York, NY"
    )
    if cust1_id:
        print(f"   [OK]Customer created: {cust1_id} - John Smith (Smith Enterprises)")

        # Create user account for customer 1
        user1_id = manager.add_user(
            "",
            "johnsmith",
            hash_password("customer123"),
            "customer",
            cust1_id,
            "john@smithent.com"
        )
        if user1_id:
            print(f"     [OK]Login: johnsmith / customer123")

    # Customer 2
    cust2_id = manager.add_customer(
        "",
        "Sarah Johnson",
        "Johnson Aviation LLC",
        "sarah@johnsonaviation.com",
        "+1-555-0202",
        "456 Sky Lane, Miami, FL"
    )
    if cust2_id:
        print(f"   [OK]Customer created: {cust2_id} - Sarah Johnson (Johnson Aviation LLC)")

        # Create user account for customer 2
        user2_id = manager.add_user(
            "",
            "sarahjohnson",
            hash_password("customer123"),
            "customer",
            cust2_id,
            "sarah@johnsonaviation.com"
        )
        if user2_id:
            print(f"     [OK]Login: sarahjohnson / customer123")

    print("\n3. Creating Sample Crew Members...")

    # Pilot 1
    pilot1_id = manager.add_crew(
        "",
        "Captain Mike Anderson",
        "Pilot",
        "P12345678",
        "USA",
        "2028-12-31",
        "+1-555-1001",
        "ATP-123456"
    )
    if pilot1_id:
        print(f"   [OK]Pilot created: {pilot1_id} - Captain Mike Anderson")

        # Create user account for pilot
        pilot_user_id = manager.add_user(
            "",
            "pilot_mike",
            hash_password("crew123"),
            "crew",
            pilot1_id,
            "mike@jetmanager.com"
        )
        if pilot_user_id:
            print(f"     [OK]Login: pilot_mike / crew123")

    # Pilot 2
    pilot2_id = manager.add_crew(
        "",
        "Captain Lisa Chen",
        "Pilot",
        "P87654321",
        "USA",
        "2029-06-30",
        "+1-555-1002",
        "ATP-789012"
    )
    if pilot2_id:
        print(f"   [OK]Pilot created: {pilot2_id} - Captain Lisa Chen")

    # Cabin Crew 1
    crew1_id = manager.add_crew(
        "",
        "Emily Davis",
        "Cabin Crew",
        "C11223344",
        "USA",
        "2027-03-15",
        "+1-555-1003",
        None
    )
    if crew1_id:
        print(f"   [OK]Cabin Crew created: {crew1_id} - Emily Davis")

    # Cabin Crew 2
    crew2_id = manager.add_crew(
        "",
        "Robert Taylor",
        "Cabin Crew",
        "C55667788",
        "USA",
        "2028-09-20",
        "+1-555-1004",
        None
    )
    if crew2_id:
        print(f"   [OK]Cabin Crew created: {crew2_id} - Robert Taylor")

    print("\n4. Creating Mechanic User...")

    # Mechanic doesn't need to be crew, just a user
    mechanic_user_id = manager.add_user(
        "",
        "mechanic_joe",
        hash_password("mech123"),
        "mechanic",
        "",
        "joe@jetmanager.com"
    )
    if mechanic_user_id:
        print(f"   [OK]Mechanic user created: mechanic_joe / mech123")

    print("\n5. Creating Sample Jets...")

    # Jet 1 for Customer 1
    jet1_id = manager.add_jet(
        "",
        "Gulfstream G650",
        "N123AB",
        14,
        cust1_id,
        "Available"
    )
    if jet1_id:
        print(f"   [OK]Jet created: {jet1_id} - Gulfstream G650 (Owner: {cust1_id})")

    # Jet 2 for Customer 1
    jet2_id = manager.add_jet(
        "",
        "Bombardier Global 7500",
        "N456CD",
        17,
        cust1_id,
        "Available"
    )
    if jet2_id:
        print(f"   [OK]Jet created: {jet2_id} - Bombardier Global 7500 (Owner: {cust1_id})")

    # Jet 3 for Customer 2
    jet3_id = manager.add_jet(
        "",
        "Cessna Citation X",
        "N789EF",
        12,
        cust2_id,
        "Available"
    )
    if jet3_id:
        print(f"   [OK]Jet created: {jet3_id} - Cessna Citation X (Owner: {cust2_id})")

    print("\n6. Creating Sample Passengers...")

    # Passengers for Customer 1
    pass1_id = manager.add_passenger(
        "",
        "Alice Williams",
        "PP1234567",
        "USA",
        "2027-05-15",
        "+1-555-2001",
        cust1_id
    )
    if pass1_id:
        print(f"   [OK]Passenger created: {pass1_id} - Alice Williams (Customer: {cust1_id})")

    pass2_id = manager.add_passenger(
        "",
        "Bob Martinez",
        "PP2345678",
        "USA",
        "2028-08-20",
        "+1-555-2002",
        cust1_id
    )
    if pass2_id:
        print(f"   [OK]Passenger created: {pass2_id} - Bob Martinez (Customer: {cust1_id})")

    # Passengers for Customer 2
    pass3_id = manager.add_passenger(
        "",
        "Carol Thompson",
        "PP3456789",
        "UK",
        "2029-01-10",
        "+44-555-3001",
        cust2_id
    )
    if pass3_id:
        print(f"   [OK]Passenger created: {pass3_id} - Carol Thompson (Customer: {cust2_id})")

    # Save all data
    manager.save_data()

    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print("\nYou can now log in with:")
    print("\n  Admin:")
    print("    Username: admin")
    print("    Password: admin123")
    print("\n  Customer 1 (John Smith):")
    print("    Username: johnsmith")
    print("    Password: customer123")
    print("\n  Customer 2 (Sarah Johnson):")
    print("    Username: sarahjohnson")
    print("    Password: customer123")
    print("\n  Crew (Pilot):")
    print("    Username: pilot_mike")
    print("    Password: crew123")
    print("\n  Mechanic:")
    print("    Username: mechanic_joe")
    print("    Password: mech123")
    print("\n[!] IMPORTANT: Change these passwords after first login!")
    print("\nStart the application with: python web_app.py")
    print("="*60)

if __name__ == "__main__":
    setup()

"""
Migrate Data from JSON to PostgreSQL
Reads jet_schedule_data.json and imports all data into PostgreSQL
"""

import json
import sys
import os
from datetime import datetime
from db_config import USE_POSTGRES, SessionLocal
from db_models import (
    CustomerModel, UserModel, PassengerModel, CrewModel,
    JetModel, FlightModel, MaintenanceModel
)

def migrate_data():
    """Migrate all data from JSON to PostgreSQL"""

    if not USE_POSTGRES:
        print("❌ ERROR: DATABASE_URL not set")
        print("Set DATABASE_URL environment variable to use PostgreSQL")
        sys.exit(1)

    # Check if JSON file exists
    json_file = 'jet_schedule_data.json'
    if not os.path.exists(json_file):
        print(f"❌ ERROR: {json_file} not found")
        print("No data to migrate. Run setup_initial_data.py to create sample data.")
        sys.exit(1)

    print("🔄 Starting migration from JSON to PostgreSQL...")
    print(f"📂 Reading from: {json_file}")

    try:
        # Load JSON data
        with open(json_file, 'r') as f:
            data = json.load(f)

        print(f"✅ Loaded JSON data")

        # Create database session
        db = SessionLocal()

        try:
            # Migrate Customers
            if 'customers' in data:
                print(f"\n👥 Migrating {len(data['customers'])} customers...")
                for cust_id, cust_data in data['customers'].items():
                    customer = CustomerModel(
                        customer_id=cust_data['customer_id'],
                        name=cust_data['name'],
                        company=cust_data['company'],
                        email=cust_data['email'],
                        phone=cust_data['phone'],
                        address=cust_data['address']
                    )
                    db.merge(customer)  # Insert or update
                db.commit()
                print(f"✅ Migrated {len(data['customers'])} customers")

            # Migrate Users
            if 'users' in data:
                print(f"\n🔐 Migrating {len(data['users'])} users...")
                for user_id, user_data in data['users'].items():
                    user = UserModel(
                        user_id=user_data['user_id'],
                        username=user_data['username'],
                        password_hash=user_data['password_hash'],
                        role=user_data['role'],
                        related_id=user_data.get('related_id', ''),
                        email=user_data.get('email', '')
                    )
                    db.merge(user)
                db.commit()
                print(f"✅ Migrated {len(data['users'])} users")

            # Migrate Passengers
            if 'passengers' in data:
                print(f"\n🧳 Migrating {len(data['passengers'])} passengers...")
                for pass_id, pass_data in data['passengers'].items():
                    passenger = PassengerModel(
                        passenger_id=pass_data['passenger_id'],
                        name=pass_data['name'],
                        passport_number=pass_data['passport_number'],
                        nationality=pass_data['nationality'],
                        passport_expiry=pass_data['passport_expiry'],
                        contact=pass_data['contact'],
                        customer_id=pass_data.get('customer_id', '')
                    )
                    db.merge(passenger)
                db.commit()
                print(f"✅ Migrated {len(data['passengers'])} passengers")

            # Migrate Crew
            if 'crew' in data:
                print(f"\n✈️ Migrating {len(data['crew'])} crew members...")
                for crew_id, crew_data in data['crew'].items():
                    crew = CrewModel(
                        crew_id=crew_data['crew_id'],
                        name=crew_data['name'],
                        role=crew_data['role'],
                        license_number=crew_data['license_number'],
                        license_expiry=crew_data['license_expiry'],
                        contact=crew_data['contact']
                    )
                    db.merge(crew)
                db.commit()
                print(f"✅ Migrated {len(data['crew'])} crew members")

            # Migrate Jets
            if 'jets' in data:
                print(f"\n🛩️ Migrating {len(data['jets'])} aircraft...")
                for jet_id, jet_data in data['jets'].items():
                    jet = JetModel(
                        jet_id=jet_data['jet_id'],
                        model=jet_data['model'],
                        registration=jet_data['registration'],
                        capacity=jet_data['capacity'],
                        status=jet_data['status'],
                        customer_id=jet_data.get('customer_id', '')
                    )
                    db.merge(jet)
                db.commit()
                print(f"✅ Migrated {len(data['jets'])} aircraft")

            # Migrate Flights
            if 'flights' in data:
                print(f"\n🛫 Migrating {len(data['flights'])} flights...")
                for flight_id, flight_data in data['flights'].items():
                    flight = FlightModel(
                        flight_id=flight_data['flight_id'],
                        jet_id=flight_data['jet_id'],
                        departure=flight_data['departure'],
                        destination=flight_data['destination'],
                        departure_time=flight_data['departure_time'],
                        arrival_time=flight_data['arrival_time'],
                        passenger_ids=flight_data['passenger_ids'],
                        crew_ids=flight_data['crew_ids'],
                        status=flight_data['status'],
                        customer_id=flight_data.get('customer_id', '')
                    )
                    db.merge(flight)
                db.commit()
                print(f"✅ Migrated {len(data['flights'])} flights")

            # Migrate Maintenance
            if 'maintenance' in data:
                print(f"\n🔧 Migrating {len(data['maintenance'])} maintenance records...")
                for maint_id, maint_data in data['maintenance'].items():
                    maintenance = MaintenanceModel(
                        maintenance_id=maint_data['maintenance_id'],
                        jet_id=maint_data['jet_id'],
                        maintenance_type=maint_data['maintenance_type'],
                        scheduled_date=maint_data['scheduled_date'],
                        completion_date=maint_data.get('completion_date', ''),
                        description=maint_data['description'],
                        status=maint_data['status'],
                        performed_by=maint_data.get('performed_by', ''),
                        customer_id=maint_data.get('customer_id', '')
                    )
                    db.merge(maintenance)
                db.commit()
                print(f"✅ Migrated {len(data['maintenance'])} maintenance records")

            print("\n" + "="*50)
            print("✅ Migration completed successfully!")
            print("="*50)

            # Create backup of JSON file
            backup_file = f'jet_schedule_data_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            os.rename(json_file, backup_file)
            print(f"\n📦 Original JSON file backed up to: {backup_file}")

            print("\n🎉 Your app is now using PostgreSQL!")
            print("\nNext step: Deploy updated app to DigitalOcean")

        except Exception as e:
            db.rollback()
            print(f"\n❌ Error during migration: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        finally:
            db.close()

    except json.JSONDecodeError as e:
        print(f"❌ Error reading JSON file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    migrate_data()

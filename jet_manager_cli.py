"""
Command-Line Interface for Private Jet Schedule Management System
"""

from jet_manager import JetScheduleManager


def print_menu():
    """Display main menu"""
    print("\n" + "="*60)
    print("PRIVATE JET SCHEDULE MANAGEMENT SYSTEM")
    print("="*60)
    print("\nPASSENGER MANAGEMENT")
    print("  1. Add Passenger")
    print("  2. List All Passengers")
    print("  3. View Passenger Details")
    print("\nJET MANAGEMENT")
    print("  4. Add Jet")
    print("  5. List All Jets")
    print("  6. View Jet Schedule")
    print("\nFLIGHT MANAGEMENT")
    print("  7. Schedule Flight")
    print("  8. List All Flights")
    print("  9. Update Flight Status")
    print("\nMAINTENANCE MANAGEMENT")
    print("  10. Schedule Maintenance")
    print("  11. Complete Maintenance")
    print("  12. List Maintenance Records")
    print("\nDATA MANAGEMENT")
    print("  13. Save Data")
    print("  14. Exit")
    print("="*60)


def add_passenger(manager: JetScheduleManager):
    """Add a new passenger"""
    print("\n--- ADD PASSENGER ---")
    passenger_id = input("Passenger ID (press Enter for auto-generated): ").strip()
    name = input("Full Name: ").strip()
    passport_number = input("Passport Number: ").strip()
    nationality = input("Nationality: ").strip()
    passport_expiry = input("Passport Expiry Date (YYYY-MM-DD): ").strip()
    contact = input("Contact (email/phone): ").strip()

    result_id = manager.add_passenger(passenger_id, name, passport_number,
                                      nationality, passport_expiry, contact)
    if result_id and not passenger_id:
        print(f"\nAuto-generated ID: {result_id}")


def view_passenger(manager: JetScheduleManager):
    """View passenger details"""
    print("\n--- VIEW PASSENGER ---")
    passenger_id = input("Passenger ID: ").strip()
    passenger = manager.get_passenger(passenger_id)

    if passenger:
        print(f"\n{passenger}")
    else:
        print(f"Passenger ID {passenger_id} not found")


def add_jet(manager: JetScheduleManager):
    """Add a new jet"""
    print("\n--- ADD JET ---")
    jet_id = input("Jet ID (press Enter for auto-generated): ").strip()
    model = input("Jet Model: ").strip()
    tail_number = input("Tail Number: ").strip()
    capacity = int(input("Passenger Capacity: ").strip())
    status = input("Status (Available/Maintenance) [Available]: ").strip() or "Available"

    result_id = manager.add_jet(jet_id, model, tail_number, capacity, status)
    if result_id and not jet_id:
        print(f"\nAuto-generated ID: {result_id}")


def schedule_flight(manager: JetScheduleManager):
    """Schedule a new flight"""
    print("\n--- SCHEDULE FLIGHT ---")
    flight_id = input("Flight ID (press Enter for auto-generated): ").strip()
    jet_id = input("Jet ID: ").strip()
    departure = input("Departure Airport: ").strip()
    destination = input("Destination Airport: ").strip()
    departure_time = input("Departure Time (YYYY-MM-DD HH:MM): ").strip()
    arrival_time = input("Arrival Time (YYYY-MM-DD HH:MM): ").strip()

    passenger_count = int(input("Number of passengers: ").strip())
    passenger_ids = []
    for i in range(passenger_count):
        pid = input(f"  Passenger {i+1} ID: ").strip()
        passenger_ids.append(pid)

    result_id = manager.schedule_flight(flight_id, jet_id, departure, destination,
                                        departure_time, arrival_time, passenger_ids)
    if result_id and not flight_id:
        print(f"\nAuto-generated ID: {result_id}")


def update_flight_status(manager: JetScheduleManager):
    """Update flight status"""
    print("\n--- UPDATE FLIGHT STATUS ---")
    flight_id = input("Flight ID: ").strip()
    print("\nStatus Options: Scheduled, In Progress, Completed, Cancelled")
    new_status = input("New Status: ").strip()

    manager.update_flight_status(flight_id, new_status)


def schedule_maintenance(manager: JetScheduleManager):
    """Schedule maintenance"""
    print("\n--- SCHEDULE MAINTENANCE ---")
    maintenance_id = input("Maintenance ID (press Enter for auto-generated): ").strip()
    jet_id = input("Jet ID: ").strip()
    scheduled_date = input("Scheduled Date (YYYY-MM-DD): ").strip()
    maintenance_type = input("Maintenance Type (Routine/Emergency/Inspection): ").strip()
    description = input("Description: ").strip()

    result_id = manager.schedule_maintenance(maintenance_id, jet_id, scheduled_date,
                                             maintenance_type, description)
    if result_id and not maintenance_id:
        print(f"\nAuto-generated ID: {result_id}")


def complete_maintenance(manager: JetScheduleManager):
    """Complete maintenance"""
    print("\n--- COMPLETE MAINTENANCE ---")
    maintenance_id = input("Maintenance ID: ").strip()
    completed_date = input("Completion Date (YYYY-MM-DD): ").strip()

    manager.complete_maintenance(maintenance_id, completed_date)


def list_maintenance(manager: JetScheduleManager):
    """List maintenance records with filters"""
    print("\n--- LIST MAINTENANCE ---")
    jet_id = input("Filter by Jet ID (or press Enter for all): ").strip() or None
    status = input("Filter by Status (Scheduled/In Progress/Completed, or press Enter for all): ").strip() or None

    manager.list_maintenance(jet_id, status)


def view_jet_schedule(manager: JetScheduleManager):
    """View complete schedule for a jet"""
    print("\n--- VIEW JET SCHEDULE ---")
    jet_id = input("Jet ID: ").strip()
    manager.get_jet_schedule(jet_id)


def main():
    """Main CLI loop"""
    manager = JetScheduleManager()

    while True:
        print_menu()
        choice = input("\nSelect an option (1-14): ").strip()

        try:
            if choice == "1":
                add_passenger(manager)
            elif choice == "2":
                manager.list_passengers()
            elif choice == "3":
                view_passenger(manager)
            elif choice == "4":
                add_jet(manager)
            elif choice == "5":
                manager.list_jets()
            elif choice == "6":
                view_jet_schedule(manager)
            elif choice == "7":
                schedule_flight(manager)
            elif choice == "8":
                status_filter = input("Filter by status (or press Enter for all): ").strip() or None
                manager.list_flights(status_filter)
            elif choice == "9":
                update_flight_status(manager)
            elif choice == "10":
                schedule_maintenance(manager)
            elif choice == "11":
                complete_maintenance(manager)
            elif choice == "12":
                list_maintenance(manager)
            elif choice == "13":
                manager.save_data()
            elif choice == "14":
                print("\nSave data before exiting? (y/n): ", end="")
                if input().strip().lower() == 'y':
                    manager.save_data()
                print("\nThank you for using the Private Jet Schedule Management System!")
                break
            else:
                print("\nInvalid option. Please select 1-14.")

        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()

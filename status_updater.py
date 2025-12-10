"""
Automatic Status Updater
Updates flight and maintenance status based on current time
"""

from datetime import datetime
from typing import Dict, List
import json
import os
import logging
from date_utils import parse_datetime

logger = logging.getLogger(__name__)

class StatusUpdater:
    """Automatically update status based on time"""

    def __init__(self, manager):
        self.manager = manager

    def update_flight_status(self, flight):
        """Update single flight status based on time"""
        now = datetime.now()
        updated = False

        # Parse times
        departure_dt = parse_datetime(flight.departure_time)
        arrival_dt = parse_datetime(flight.arrival_time)

        if not departure_dt or not arrival_dt:
            return False

        old_status = flight.status

        # Determine new status
        if now < departure_dt:
            new_status = 'Scheduled'
        elif departure_dt <= now < arrival_dt:
            new_status = 'In Progress'
        elif now >= arrival_dt:
            new_status = 'Completed'
        else:
            new_status = flight.status

        # Update if changed
        if new_status != old_status:
            flight.status = new_status
            updated = True
            logger.info(f"Flight {flight.flight_id}: {old_status} -> {new_status}")

        return updated

    def update_maintenance_status(self, maintenance):
        """Update single maintenance status based on time"""
        now = datetime.now()
        updated = False

        # Parse dates
        scheduled_dt = parse_datetime(maintenance.scheduled_date)
        completed_dt = parse_datetime(maintenance.completed_date)

        if not scheduled_dt:
            return False

        old_status = maintenance.status

        # Determine new status based on dates
        if completed_dt and now >= completed_dt:
            new_status = 'Completed'
        elif now >= scheduled_dt and not completed_dt:
            new_status = 'In Progress'
        else:
            new_status = maintenance.status

        # Don't override manually set status if already completed
        if old_status == 'Completed' and new_status != 'Completed':
            return False

        # Update if changed
        if new_status != old_status:
            maintenance.status = new_status
            updated = True
            logger.info(f"Maintenance {maintenance.maintenance_id}: {old_status} -> {new_status}")

        return updated

    def update_all_statuses(self):
        """Update all flights and maintenance statuses"""
        logger.info("Running automatic status updates...")
        logger.info(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        flights_updated = 0
        maintenance_updated = 0

        # Update all flights
        for flight in self.manager.flights.values():
            if self.update_flight_status(flight):
                flights_updated += 1

        # Update all maintenance
        for maint in self.manager.maintenance.values():
            if self.update_maintenance_status(maint):
                maintenance_updated += 1

        # Save if any changes
        if flights_updated > 0 or maintenance_updated > 0:
            self.manager.save_data()
            logger.info(f"Updated {flights_updated} flights and {maintenance_updated} maintenance records")
        else:
            logger.info("No status updates needed")

        return {
            'flights_updated': flights_updated,
            'maintenance_updated': maintenance_updated,
            'timestamp': datetime.now().isoformat()
        }

    def get_upcoming_events(self, hours=24):
        """Get flights and maintenance in next X hours"""
        now = datetime.now()
        upcoming = {
            'flights': [],
            'maintenance': []
        }

        for flight in self.manager.flights.values():
            departure_dt = parse_datetime(flight.departure_time)
            if departure_dt:
                time_diff = (departure_dt - now).total_seconds() / 3600
                if 0 < time_diff <= hours:
                    upcoming['flights'].append({
                        'flight_id': flight.flight_id,
                        'departure': flight.departure,
                        'destination': flight.destination,
                        'time': flight.departure_time,
                        'hours_until': round(time_diff, 1)
                    })

        for maint in self.manager.maintenance.values():
            scheduled_dt = parse_datetime(maint.scheduled_date)
            if scheduled_dt and maint.status != 'Completed':
                time_diff = (scheduled_dt - now).total_seconds() / 3600
                if 0 < time_diff <= hours:
                    upcoming['maintenance'].append({
                        'maintenance_id': maint.maintenance_id,
                        'jet_id': maint.jet_id,
                        'type': maint.maintenance_type,
                        'time': maint.scheduled_date,
                        'hours_until': round(time_diff, 1)
                    })

        return upcoming


# Background task runner
class BackgroundUpdater:
    """Run status updates in background"""

    def __init__(self, manager, interval_minutes=5):
        self.manager = manager
        self.updater = StatusUpdater(manager)
        self.interval = interval_minutes * 60  # Convert to seconds
        self.last_run = None

    def should_run(self):
        """Check if it's time to run update"""
        if not self.last_run:
            return True

        now = datetime.now()
        elapsed = (now - self.last_run).total_seconds()
        return elapsed >= self.interval

    def run_if_needed(self):
        """Run update if interval has passed"""
        if self.should_run():
            result = self.updater.update_all_statuses()
            self.last_run = datetime.now()
            return result
        return None


def create_scheduled_task(manager, interval_minutes=5):
    """Create a background updater instance"""
    return BackgroundUpdater(manager, interval_minutes)

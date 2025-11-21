"""
Activity Log System
Tracks all user actions in the system for auditing and history
"""

import json
import os
from datetime import datetime
from typing import Optional

class ActivityLogger:
    """Log user activities to file and/or database"""

    def __init__(self, log_file='activity_log.json'):
        self.log_file = log_file
        self.logs = self._load_logs()

    def _load_logs(self):
        """Load existing logs from file"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_logs(self):
        """Save logs to file"""
        try:
            with open(self.log_file, 'w') as f:
                # Keep only last 1000 entries
                json.dump(self.logs[-1000:], f, indent=2)
        except Exception as e:
            print(f"Error saving activity log: {e}")

    def log(self, user_id: str, username: str, action: str,
            entity_type: str, entity_id: str, details: Optional[str] = None):
        """
        Log an activity

        Args:
            user_id: User performing the action
            username: Username performing the action
            action: Action performed (created, updated, deleted, viewed, etc.)
            entity_type: Type of entity (flight, passenger, jet, etc.)
            entity_id: ID of the entity
            details: Optional additional details
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'username': username,
            'action': action,
            'entity_type': entity_type,
            'entity_id': entity_id,
            'details': details or ''
        }

        self.logs.append(log_entry)
        self._save_logs()

    def get_recent(self, limit=50):
        """Get recent activity logs"""
        return list(reversed(self.logs[-limit:]))

    def get_by_user(self, user_id: str, limit=50):
        """Get activity logs for specific user"""
        user_logs = [log for log in self.logs if log['user_id'] == user_id]
        return list(reversed(user_logs[-limit:]))

    def get_by_entity(self, entity_type: str, entity_id: str):
        """Get activity logs for specific entity"""
        return [log for log in self.logs
                if log['entity_type'] == entity_type and log['entity_id'] == entity_id]

    def get_stats(self):
        """Get activity statistics"""
        if not self.logs:
            return {
                'total_activities': 0,
                'unique_users': 0,
                'most_active_user': None,
                'most_common_action': None
            }

        users = {}
        actions = {}

        for log in self.logs:
            user = log['username']
            action = log['action']

            users[user] = users.get(user, 0) + 1
            actions[action] = actions.get(action, 0) + 1

        most_active = max(users.items(), key=lambda x: x[1]) if users else (None, 0)
        most_common = max(actions.items(), key=lambda x: x[1]) if actions else (None, 0)

        return {
            'total_activities': len(self.logs),
            'unique_users': len(users),
            'most_active_user': most_active[0],
            'most_active_count': most_active[1],
            'most_common_action': most_common[0],
            'most_common_count': most_common[1]
        }

# Global activity logger instance
activity_logger = ActivityLogger()

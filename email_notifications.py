"""
Email Notification System
Send automated emails for flights, maintenance, and other events
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Optional

class EmailNotifier:
    """Send email notifications"""

    def __init__(self):
        # Get email configuration from environment variables
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.sendgrid.net')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.smtp_username = os.environ.get('SMTP_USERNAME', '')
        self.smtp_password = os.environ.get('SMTP_PASSWORD', '')
        self.from_email = os.environ.get('FROM_EMAIL', 'noreply@manajet.app')
        self.from_name = os.environ.get('FROM_NAME', 'Manajet Aviation')

        self.enabled = bool(self.smtp_username and self.smtp_password)

    def _send_email(self, to_email: str, subject: str, html_content: str, text_content: Optional[str] = None):
        """Send an email"""
        if not self.enabled:
            print(f"📧 Email notifications disabled (SMTP not configured)")
            print(f"   Would send to: {to_email}")
            print(f"   Subject: {subject}")
            return False

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f'{self.from_name} <{self.from_email}>'
            msg['To'] = to_email

            # Add text version
            if text_content:
                part1 = MIMEText(text_content, 'plain')
                msg.attach(part1)

            # Add HTML version
            part2 = MIMEText(html_content, 'html')
            msg.attach(part2)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            print(f"✅ Email sent to {to_email}: {subject}")
            return True

        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False

    def send_flight_confirmation(self, flight_data: dict, passenger_data: dict):
        """Send flight confirmation to passenger"""
        subject = f"Flight Confirmation - {flight_data['flight_id']}"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9fafb; padding: 30px; }}
                .flight-info {{ background: white; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .info-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e5e7eb; }}
                .label {{ font-weight: bold; color: #6366f1; }}
                .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✈️ Flight Confirmed</h1>
                    <p>Your flight has been scheduled</p>
                </div>
                <div class="content">
                    <p>Dear {passenger_data['name']},</p>
                    <p>Your flight has been confirmed. Please review the details below:</p>

                    <div class="flight-info">
                        <div class="info-row">
                            <span class="label">Flight Number:</span>
                            <span>{flight_data['flight_id']}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">Departure:</span>
                            <span>{flight_data['departure']}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">Destination:</span>
                            <span>{flight_data['destination']}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">Departure Time:</span>
                            <span>{flight_data['departure_time']}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">Arrival Time:</span>
                            <span>{flight_data['arrival_time']}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">Aircraft:</span>
                            <span>{flight_data.get('aircraft_model', 'N/A')}</span>
                        </div>
                    </div>

                    <p><strong>Important Reminders:</strong></p>
                    <ul>
                        <li>Please arrive 30 minutes before departure</li>
                        <li>Bring your passport and travel documents</li>
                        <li>Contact us if you need to make any changes</li>
                    </ul>

                    <p>If you have any questions, please don't hesitate to contact us.</p>
                    <p>Safe travels!</p>
                </div>
                <div class="footer">
                    <p>&copy; 2025 Manajet Aviation Management</p>
                    <p>Professional Aviation Services</p>
                </div>
            </div>
        </body>
        </html>
        """

        text = f"""
        Flight Confirmation - {flight_data['flight_id']}

        Dear {passenger_data['name']},

        Your flight has been confirmed:

        Flight Number: {flight_data['flight_id']}
        Departure: {flight_data['departure']}
        Destination: {flight_data['destination']}
        Departure Time: {flight_data['departure_time']}
        Arrival Time: {flight_data['arrival_time']}

        Please arrive 30 minutes before departure.

        Safe travels!

        Manajet Aviation Management
        """

        return self._send_email(passenger_data['contact'], subject, html, text)

    def send_maintenance_reminder(self, maintenance_data: dict, jet_data: dict, recipient_email: str):
        """Send maintenance reminder"""
        subject = f"Maintenance Reminder - {jet_data['model']} ({jet_data['registration']})"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9fafb; padding: 30px; }}
                .alert-box {{ background: #fef3c7; border-left: 4px solid #f59e0b; padding: 20px; margin: 20px 0; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔧 Maintenance Reminder</h1>
                </div>
                <div class="content">
                    <div class="alert-box">
                        <h3>Scheduled Maintenance</h3>
                        <p><strong>Aircraft:</strong> {jet_data['model']} ({jet_data['registration']})</p>
                        <p><strong>Type:</strong> {maintenance_data['maintenance_type']}</p>
                        <p><strong>Scheduled Date:</strong> {maintenance_data['scheduled_date']}</p>
                        <p><strong>Description:</strong> {maintenance_data['description']}</p>
                    </div>
                    <p>Please ensure the aircraft is available for maintenance on the scheduled date.</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self._send_email(recipient_email, subject, html)

    def send_welcome_email(self, customer_data: dict):
        """Send welcome email to new customer"""
        subject = "Welcome to Manajet Aviation"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: white; padding: 40px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9fafb; padding: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✈️ Welcome to Manajet!</h1>
                </div>
                <div class="content">
                    <p>Dear {customer_data['name']},</p>
                    <p>Welcome to Manajet Aviation Management!</p>
                    <p>We're excited to have you on board. Our team is committed to providing you with exceptional private aviation services.</p>
                    <p><strong>Your Account Details:</strong></p>
                    <ul>
                        <li>Company: {customer_data['company']}</li>
                        <li>Email: {customer_data['email']}</li>
                        <li>Phone: {customer_data['phone']}</li>
                    </ul>
                    <p>You can now access your personalized dashboard to manage your flights, aircraft, and more.</p>
                    <p>If you have any questions, our team is here to help!</p>
                    <p>Best regards,<br>The Manajet Team</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self._send_email(customer_data['email'], subject, html)

# Global email notifier instance
email_notifier = EmailNotifier()

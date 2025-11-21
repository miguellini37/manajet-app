"""
PDF Report Generator for Manajet
Generates professional PDF documents for flight manifests, trip sheets, and aircraft reports
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
from io import BytesIO


class PDFGenerator:
    """Generate professional PDF reports for Manajet"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=20,
            alignment=TA_CENTER
        ))

        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ))

    def _add_header(self, canvas_obj, doc):
        """Add header to each page"""
        canvas_obj.saveState()
        canvas_obj.setFont('Helvetica-Bold', 20)
        canvas_obj.setFillColor(colors.HexColor('#6366f1'))
        canvas_obj.drawString(inch, doc.height + doc.topMargin - 0.3 * inch, "✈ MANAJET")
        canvas_obj.setFont('Helvetica', 9)
        canvas_obj.setFillColor(colors.HexColor('#64748b'))
        canvas_obj.drawString(inch, doc.height + doc.topMargin - 0.5 * inch, "Private Jet Schedule Management")
        canvas_obj.line(inch, doc.height + doc.topMargin - 0.6 * inch,
                       doc.width + inch, doc.height + doc.topMargin - 0.6 * inch)
        canvas_obj.restoreState()

    def _add_footer(self, canvas_obj, doc):
        """Add footer to each page"""
        canvas_obj.saveState()
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.setFillColor(colors.HexColor('#94a3b8'))
        canvas_obj.line(inch, 0.75 * inch, doc.width + inch, 0.75 * inch)
        canvas_obj.drawString(inch, 0.5 * inch, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        canvas_obj.drawRightString(doc.width + inch, 0.5 * inch, f"Page {doc.page}")
        canvas_obj.restoreState()

    def generate_flight_manifest(self, flight, jet, passengers, crew, output_path=None):
        """Generate a flight manifest PDF"""
        buffer = BytesIO() if output_path is None else output_path

        # Create document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch
        )

        # Container for elements
        elements = []

        # Title
        elements.append(Paragraph("FLIGHT MANIFEST", self.styles['CustomTitle']))
        elements.append(Paragraph(f"Flight {flight.flight_id}", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 0.3 * inch))

        # Flight Information
        elements.append(Paragraph("Flight Information", self.styles['SectionHeader']))

        flight_data = [
            ['Flight ID:', flight.flight_id, 'Status:', flight.status],
            ['Departure:', flight.departure, 'Destination:', flight.destination],
            ['Departure Time:', flight.departure_time, 'Arrival Time:', flight.arrival_time],
        ]

        flight_table = Table(flight_data, colWidths=[1.5 * inch, 2 * inch, 1.5 * inch, 2 * inch])
        flight_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#0f172a')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
        ]))
        elements.append(flight_table)
        elements.append(Spacer(1, 0.3 * inch))

        # Aircraft Information
        elements.append(Paragraph("Aircraft Information", self.styles['SectionHeader']))

        aircraft_data = [
            ['Aircraft ID:', jet.jet_id],
            ['Model:', jet.model],
            ['Tail Number:', jet.tail_number],
            ['Capacity:', f"{jet.capacity} passengers"],
            ['Status:', jet.status]
        ]

        aircraft_table = Table(aircraft_data, colWidths=[2 * inch, 5 * inch])
        aircraft_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#0f172a')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
        ]))
        elements.append(aircraft_table)
        elements.append(Spacer(1, 0.3 * inch))

        # Passenger List
        elements.append(Paragraph("Passenger Manifest", self.styles['SectionHeader']))

        if passengers:
            passenger_data = [['#', 'Name', 'Passport', 'Nationality', 'Contact']]
            for idx, passenger in enumerate(passengers, 1):
                passenger_data.append([
                    str(idx),
                    passenger.name,
                    passenger.passport_number,
                    passenger.nationality,
                    passenger.contact
                ])

            passenger_table = Table(passenger_data, colWidths=[0.4 * inch, 1.8 * inch, 1.5 * inch, 1.3 * inch, 2 * inch])
            passenger_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
            ]))
            elements.append(passenger_table)
        else:
            elements.append(Paragraph("No passengers listed", self.styles['Normal']))

        elements.append(Spacer(1, 0.3 * inch))

        # Crew List
        elements.append(Paragraph("Crew Members", self.styles['SectionHeader']))

        if crew:
            crew_data = [['Name', 'Type', 'License', 'Contact']]
            for member in crew:
                crew_data.append([
                    member.name,
                    member.crew_type,
                    member.license_number or 'N/A',
                    member.contact
                ])

            crew_table = Table(crew_data, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch, 2 * inch])
            crew_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fdfa')])
            ]))
            elements.append(crew_table)
        else:
            elements.append(Paragraph("No crew assigned", self.styles['Normal']))

        # Build PDF
        doc.build(elements, onFirstPage=self._add_header, onLaterPages=self._add_header)

        if output_path is None:
            buffer.seek(0)
            return buffer

    def generate_aircraft_report(self, jet, customer, flights, maintenance, output_path=None):
        """Generate an aircraft information report PDF"""
        buffer = BytesIO() if output_path is None else output_path

        # Create document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch
        )

        elements = []

        # Title
        elements.append(Paragraph("AIRCRAFT REPORT", self.styles['CustomTitle']))
        elements.append(Paragraph(f"{jet.model} - {jet.tail_number}", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 0.3 * inch))

        # Aircraft Details
        elements.append(Paragraph("Aircraft Information", self.styles['SectionHeader']))

        aircraft_data = [
            ['Aircraft ID:', jet.jet_id],
            ['Model:', jet.model],
            ['Tail Number:', jet.tail_number],
            ['Capacity:', f"{jet.capacity} passengers"],
            ['Current Status:', jet.status]
        ]

        if customer:
            aircraft_data.append(['Owner:', customer.name])
            aircraft_data.append(['Company:', customer.company])

        aircraft_table = Table(aircraft_data, colWidths=[2 * inch, 5 * inch])
        aircraft_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#0f172a')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
        ]))
        elements.append(aircraft_table)
        elements.append(Spacer(1, 0.3 * inch))

        # Flight History
        elements.append(Paragraph("Recent Flights", self.styles['SectionHeader']))

        if flights:
            flight_data = [['Date', 'Flight ID', 'Route', 'Status']]
            for flight in flights[-10:]:  # Last 10 flights
                route = f"{flight.departure} → {flight.destination}"
                flight_data.append([
                    flight.departure_time.split()[0] if ' ' in flight.departure_time else flight.departure_time,
                    flight.flight_id,
                    route,
                    flight.status
                ])

            flight_table = Table(flight_data, colWidths=[1.2 * inch, 1.2 * inch, 2.8 * inch, 1.8 * inch])
            flight_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
            ]))
            elements.append(flight_table)
        else:
            elements.append(Paragraph("No flight history", self.styles['Normal']))

        elements.append(Spacer(1, 0.3 * inch))

        # Maintenance Records
        elements.append(Paragraph("Maintenance History", self.styles['SectionHeader']))

        if maintenance:
            maint_data = [['Date', 'Type', 'Description', 'Status']]
            for maint in maintenance[-10:]:  # Last 10 maintenance records
                maint_data.append([
                    maint.scheduled_date,
                    maint.maintenance_type,
                    maint.description[:30] + '...' if len(maint.description) > 30 else maint.description,
                    maint.status
                ])

            maint_table = Table(maint_data, colWidths=[1.2 * inch, 1.5 * inch, 3 * inch, 1.3 * inch])
            maint_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f59e0b')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fffbeb')])
            ]))
            elements.append(maint_table)
        else:
            elements.append(Paragraph("No maintenance history", self.styles['Normal']))

        # Build PDF
        doc.build(elements, onFirstPage=self._add_header, onLaterPages=self._add_header)

        if output_path is None:
            buffer.seek(0)
            return buffer


# Global instance
pdf_generator = PDFGenerator()

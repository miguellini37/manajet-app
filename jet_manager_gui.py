"""
Graphical User Interface for Private Jet Schedule Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from jet_manager import JetScheduleManager


class JetManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Private Jet Schedule Management System")
        self.root.geometry("1200x800")

        # Initialize the manager
        self.manager = JetScheduleManager()

        # Create main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Private Jet Schedule Management System",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=10)

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create tabs
        self.create_passenger_tab()
        self.create_jet_tab()
        self.create_flight_tab()
        self.create_maintenance_tab()
        self.create_dashboard_tab()

        # Bottom buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=10)

        ttk.Button(button_frame, text="Save Data", command=self.save_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh All", command=self.refresh_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.exit_app).pack(side=tk.LEFT, padx=5)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E))

        # Initial refresh
        self.refresh_all()

    def create_passenger_tab(self):
        """Create passenger management tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Passengers")

        # Left side - Form
        form_frame = ttk.LabelFrame(tab, text="Add/Edit Passenger", padding="10")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.N, tk.W, tk.E))

        # Form fields
        ttk.Label(form_frame, text="Passenger ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.pass_id_var = tk.StringVar()
        pass_id_entry = ttk.Entry(form_frame, textvariable=self.pass_id_var, width=30, state='readonly')
        pass_id_entry.grid(row=0, column=1, pady=5)
        ttk.Label(form_frame, text="(auto-generated)", font=('Arial', 8), foreground='gray').grid(row=0, column=2, sticky=tk.W)

        ttk.Label(form_frame, text="Full Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.pass_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.pass_name_var, width=30).grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Passport Number:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.pass_passport_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.pass_passport_var, width=30).grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Nationality:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.pass_nation_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.pass_nation_var, width=30).grid(row=3, column=1, pady=5)

        ttk.Label(form_frame, text="Passport Expiry:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.pass_expiry_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.pass_expiry_var, width=30).grid(row=4, column=1, pady=5)
        ttk.Label(form_frame, text="(YYYY-MM-DD)", font=('Arial', 8)).grid(row=4, column=2, sticky=tk.W)

        ttk.Label(form_frame, text="Contact:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.pass_contact_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.pass_contact_var, width=30).grid(row=5, column=1, pady=5)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="Add Passenger", command=self.add_passenger).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_passenger_form).pack(side=tk.LEFT, padx=5)

        # Right side - List
        list_frame = ttk.LabelFrame(tab, text="Registered Passengers", padding="10")
        list_frame.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Configure grid weights
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Treeview
        columns = ("ID", "Name", "Passport", "Nationality", "Expiry", "Contact")
        self.passenger_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=20)

        for col in columns:
            self.passenger_tree.heading(col, text=col)
            self.passenger_tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.passenger_tree.yview)
        self.passenger_tree.configure(yscrollcommand=scrollbar.set)

        self.passenger_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Bind double-click to load passenger
        self.passenger_tree.bind('<Double-1>', self.load_passenger)

    def create_jet_tab(self):
        """Create jet management tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Jets")

        # Left side - Form
        form_frame = ttk.LabelFrame(tab, text="Add/Edit Jet", padding="10")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.N, tk.W, tk.E))

        ttk.Label(form_frame, text="Jet ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.jet_id_var = tk.StringVar()
        jet_id_entry = ttk.Entry(form_frame, textvariable=self.jet_id_var, width=30, state='readonly')
        jet_id_entry.grid(row=0, column=1, pady=5)
        ttk.Label(form_frame, text="(auto-generated)", font=('Arial', 8), foreground='gray').grid(row=0, column=2, sticky=tk.W)

        ttk.Label(form_frame, text="Model:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.jet_model_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.jet_model_var, width=30).grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Tail Number:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.jet_tail_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.jet_tail_var, width=30).grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Capacity:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.jet_capacity_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.jet_capacity_var, width=30).grid(row=3, column=1, pady=5)

        ttk.Label(form_frame, text="Status:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.jet_status_var = tk.StringVar(value="Available")
        status_combo = ttk.Combobox(form_frame, textvariable=self.jet_status_var, width=28)
        status_combo['values'] = ("Available", "In Flight", "Maintenance")
        status_combo.grid(row=4, column=1, pady=5)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Add Jet", command=self.add_jet).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_jet_form).pack(side=tk.LEFT, padx=5)

        # Right side - List
        list_frame = ttk.LabelFrame(tab, text="Registered Jets", padding="10")
        list_frame.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.N, tk.S, tk.E, tk.W))

        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        columns = ("ID", "Model", "Tail Number", "Capacity", "Status")
        self.jet_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=20)

        for col in columns:
            self.jet_tree.heading(col, text=col)
            self.jet_tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.jet_tree.yview)
        self.jet_tree.configure(yscrollcommand=scrollbar.set)

        self.jet_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.jet_tree.bind('<Double-1>', self.load_jet)

    def create_flight_tab(self):
        """Create flight scheduling tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Flights")

        # Left side - Form
        form_frame = ttk.LabelFrame(tab, text="Schedule Flight", padding="10")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.N, tk.W, tk.E))

        ttk.Label(form_frame, text="Flight ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.flight_id_var = tk.StringVar()
        flight_id_entry = ttk.Entry(form_frame, textvariable=self.flight_id_var, width=30, state='readonly')
        flight_id_entry.grid(row=0, column=1, pady=5)
        ttk.Label(form_frame, text="(auto-generated)", font=('Arial', 8), foreground='gray').grid(row=0, column=2, sticky=tk.W)

        ttk.Label(form_frame, text="Jet ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.flight_jet_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.flight_jet_var, width=30).grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Departure:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.flight_dep_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.flight_dep_var, width=30).grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Destination:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.flight_dest_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.flight_dest_var, width=30).grid(row=3, column=1, pady=5)

        ttk.Label(form_frame, text="Departure Time:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.flight_deptime_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.flight_deptime_var, width=30).grid(row=4, column=1, pady=5)
        ttk.Label(form_frame, text="(YYYY-MM-DD HH:MM)", font=('Arial', 8)).grid(row=4, column=2, sticky=tk.W)

        ttk.Label(form_frame, text="Arrival Time:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.flight_arrtime_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.flight_arrtime_var, width=30).grid(row=5, column=1, pady=5)
        ttk.Label(form_frame, text="(YYYY-MM-DD HH:MM)", font=('Arial', 8)).grid(row=5, column=2, sticky=tk.W)

        ttk.Label(form_frame, text="Passenger IDs:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.flight_passengers_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.flight_passengers_var, width=30).grid(row=6, column=1, pady=5)
        ttk.Label(form_frame, text="(comma-separated)", font=('Arial', 8)).grid(row=6, column=2, sticky=tk.W)

        ttk.Label(form_frame, text="Status:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.flight_status_var = tk.StringVar(value="Scheduled")
        status_combo = ttk.Combobox(form_frame, textvariable=self.flight_status_var, width=28)
        status_combo['values'] = ("Scheduled", "In Progress", "Completed", "Cancelled")
        status_combo.grid(row=7, column=1, pady=5)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=8, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="Schedule Flight", command=self.schedule_flight).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Status", command=self.update_flight_status_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_flight_form).pack(side=tk.LEFT, padx=5)

        # Right side - List
        list_frame = ttk.LabelFrame(tab, text="Scheduled Flights", padding="10")
        list_frame.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.N, tk.S, tk.E, tk.W))

        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        columns = ("ID", "Jet", "Route", "Departure", "Arrival", "Passengers", "Status")
        self.flight_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=20)

        widths = [80, 80, 150, 120, 120, 80, 100]
        for col, width in zip(columns, widths):
            self.flight_tree.heading(col, text=col)
            self.flight_tree.column(col, width=width)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.flight_tree.yview)
        self.flight_tree.configure(yscrollcommand=scrollbar.set)

        self.flight_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.flight_tree.bind('<Double-1>', self.load_flight)

    def create_maintenance_tab(self):
        """Create maintenance management tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Maintenance")

        # Left side - Form
        form_frame = ttk.LabelFrame(tab, text="Schedule Maintenance", padding="10")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.N, tk.W, tk.E))

        ttk.Label(form_frame, text="Maintenance ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.maint_id_var = tk.StringVar()
        maint_id_entry = ttk.Entry(form_frame, textvariable=self.maint_id_var, width=30, state='readonly')
        maint_id_entry.grid(row=0, column=1, pady=5)
        ttk.Label(form_frame, text="(auto-generated)", font=('Arial', 8), foreground='gray').grid(row=0, column=2, sticky=tk.W)

        ttk.Label(form_frame, text="Jet ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.maint_jet_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.maint_jet_var, width=30).grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Scheduled Date:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.maint_date_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.maint_date_var, width=30).grid(row=2, column=1, pady=5)
        ttk.Label(form_frame, text="(YYYY-MM-DD)", font=('Arial', 8)).grid(row=2, column=2, sticky=tk.W)

        ttk.Label(form_frame, text="Type:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.maint_type_var = tk.StringVar(value="Routine")
        type_combo = ttk.Combobox(form_frame, textvariable=self.maint_type_var, width=28)
        type_combo['values'] = ("Routine", "Emergency", "Inspection")
        type_combo.grid(row=3, column=1, pady=5)

        ttk.Label(form_frame, text="Description:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.maint_desc_text = tk.Text(form_frame, width=30, height=4)
        self.maint_desc_text.grid(row=4, column=1, pady=5)

        ttk.Label(form_frame, text="Status:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.maint_status_var = tk.StringVar(value="Scheduled")
        status_combo = ttk.Combobox(form_frame, textvariable=self.maint_status_var, width=28)
        status_combo['values'] = ("Scheduled", "In Progress", "Completed")
        status_combo.grid(row=5, column=1, pady=5)

        ttk.Label(form_frame, text="Completed Date:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.maint_completed_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.maint_completed_var, width=30).grid(row=6, column=1, pady=5)
        ttk.Label(form_frame, text="(optional)", font=('Arial', 8)).grid(row=6, column=2, sticky=tk.W)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=7, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="Schedule Maintenance", command=self.schedule_maintenance).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Status", command=self.update_maintenance_status_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_maintenance_form).pack(side=tk.LEFT, padx=5)

        # Right side - List
        list_frame = ttk.LabelFrame(tab, text="Maintenance Records", padding="10")
        list_frame.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.N, tk.S, tk.E, tk.W))

        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        columns = ("ID", "Jet", "Scheduled", "Type", "Description", "Status", "Completed")
        self.maint_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=20)

        widths = [80, 80, 100, 100, 200, 100, 100]
        for col, width in zip(columns, widths):
            self.maint_tree.heading(col, text=col)
            self.maint_tree.column(col, width=width)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.maint_tree.yview)
        self.maint_tree.configure(yscrollcommand=scrollbar.set)

        self.maint_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.maint_tree.bind('<Double-1>', self.load_maintenance)

    def create_dashboard_tab(self):
        """Create dashboard/overview tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Dashboard")

        # Statistics frame
        stats_frame = ttk.LabelFrame(tab, text="System Statistics", padding="10")
        stats_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))

        self.stats_text = tk.Text(stats_frame, width=80, height=10, font=('Courier', 10))
        self.stats_text.pack()

        # Jet schedule viewer
        schedule_frame = ttk.LabelFrame(tab, text="View Jet Schedule", padding="10")
        schedule_frame.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        tab.rowconfigure(1, weight=1)
        tab.columnconfigure(0, weight=1)

        input_frame = ttk.Frame(schedule_frame)
        input_frame.pack(fill=tk.X, pady=5)

        ttk.Label(input_frame, text="Jet ID:").pack(side=tk.LEFT, padx=5)
        self.schedule_jet_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.schedule_jet_var, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="View Schedule", command=self.view_jet_schedule).pack(side=tk.LEFT, padx=5)

        self.schedule_text = scrolledtext.ScrolledText(schedule_frame, width=100, height=25, font=('Courier', 9))
        self.schedule_text.pack(fill=tk.BOTH, expand=True)

    # Passenger methods
    def add_passenger(self):
        try:
            # The ID field is empty or readonly, let the manager auto-generate
            passenger_id = self.manager.add_passenger(
                "",  # Empty string triggers auto-generation
                self.pass_name_var.get(),
                self.pass_passport_var.get(),
                self.pass_nation_var.get(),
                self.pass_expiry_var.get(),
                self.pass_contact_var.get()
            )
            if passenger_id:
                self.refresh_passenger_list()
                self.clear_passenger_form()
                self.status_var.set(f"Passenger added successfully with ID: {passenger_id}")
                messagebox.showinfo("Success", f"Passenger added with ID: {passenger_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_passenger_form(self):
        self.pass_id_var.set("")
        self.pass_name_var.set("")
        self.pass_passport_var.set("")
        self.pass_nation_var.set("")
        self.pass_expiry_var.set("")
        self.pass_contact_var.set("")

    def load_passenger(self, event):
        selection = self.passenger_tree.selection()
        if selection:
            item = self.passenger_tree.item(selection[0])
            values = item['values']
            self.pass_id_var.set(values[0])
            self.pass_name_var.set(values[1])
            self.pass_passport_var.set(values[2])
            self.pass_nation_var.set(values[3])
            self.pass_expiry_var.set(values[4])
            self.pass_contact_var.set(values[5])

    def refresh_passenger_list(self):
        # Clear existing items
        for item in self.passenger_tree.get_children():
            self.passenger_tree.delete(item)

        # Add passengers
        for passenger in self.manager.passengers.values():
            self.passenger_tree.insert("", tk.END, values=(
                passenger.passenger_id,
                passenger.name,
                passenger.passport_number,
                passenger.nationality,
                passenger.passport_expiry,
                passenger.contact
            ))

    # Jet methods
    def add_jet(self):
        try:
            # The ID field is empty or readonly, let the manager auto-generate
            jet_id = self.manager.add_jet(
                "",  # Empty string triggers auto-generation
                self.jet_model_var.get(),
                self.jet_tail_var.get(),
                int(self.jet_capacity_var.get()),
                self.jet_status_var.get()
            )
            if jet_id:
                self.refresh_jet_list()
                self.clear_jet_form()
                self.status_var.set(f"Jet added successfully with ID: {jet_id}")
                messagebox.showinfo("Success", f"Jet added with ID: {jet_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_jet_form(self):
        self.jet_id_var.set("")
        self.jet_model_var.set("")
        self.jet_tail_var.set("")
        self.jet_capacity_var.set("")
        self.jet_status_var.set("Available")

    def load_jet(self, event):
        selection = self.jet_tree.selection()
        if selection:
            item = self.jet_tree.item(selection[0])
            values = item['values']
            self.jet_id_var.set(values[0])
            self.jet_model_var.set(values[1])
            self.jet_tail_var.set(values[2])
            self.jet_capacity_var.set(values[3])
            self.jet_status_var.set(values[4])

    def refresh_jet_list(self):
        for item in self.jet_tree.get_children():
            self.jet_tree.delete(item)

        for jet in self.manager.jets.values():
            self.jet_tree.insert("", tk.END, values=(
                jet.jet_id,
                jet.model,
                jet.tail_number,
                jet.capacity,
                jet.status
            ))

    # Flight methods
    def schedule_flight(self):
        try:
            passenger_ids = [p.strip() for p in self.flight_passengers_var.get().split(',') if p.strip()]
            # The ID field is empty or readonly, let the manager auto-generate
            flight_id = self.manager.schedule_flight(
                "",  # Empty string triggers auto-generation
                self.flight_jet_var.get(),
                self.flight_dep_var.get(),
                self.flight_dest_var.get(),
                self.flight_deptime_var.get(),
                self.flight_arrtime_var.get(),
                passenger_ids
            )
            if flight_id:
                self.refresh_flight_list()
                self.clear_flight_form()
                self.status_var.set(f"Flight scheduled successfully with ID: {flight_id}")
                messagebox.showinfo("Success", f"Flight scheduled with ID: {flight_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_flight_form(self):
        self.flight_id_var.set("")
        self.flight_jet_var.set("")
        self.flight_dep_var.set("")
        self.flight_dest_var.set("")
        self.flight_deptime_var.set("")
        self.flight_arrtime_var.set("")
        self.flight_passengers_var.set("")
        self.flight_status_var.set("Scheduled")

    def load_flight(self, event):
        selection = self.flight_tree.selection()
        if selection:
            item = self.flight_tree.item(selection[0])
            values = item['values']
            flight_id = values[0]
            flight = self.manager.get_flight(flight_id)
            if flight:
                self.flight_id_var.set(flight.flight_id)
                self.flight_jet_var.set(flight.jet_id)
                self.flight_dep_var.set(flight.departure)
                self.flight_dest_var.set(flight.destination)
                self.flight_deptime_var.set(flight.departure_time)
                self.flight_arrtime_var.set(flight.arrival_time)
                self.flight_passengers_var.set(", ".join(flight.passenger_ids))
                self.flight_status_var.set(flight.status)

    def refresh_flight_list(self):
        for item in self.flight_tree.get_children():
            self.flight_tree.delete(item)

        for flight in self.manager.flights.values():
            route = f"{flight.departure} → {flight.destination}"
            self.flight_tree.insert("", tk.END, values=(
                flight.flight_id,
                flight.jet_id,
                route,
                flight.departure_time,
                flight.arrival_time,
                len(flight.passenger_ids),
                flight.status
            ))

    def update_flight_status_gui(self):
        """Update flight status from the form"""
        flight_id = self.flight_id_var.get()
        if not flight_id:
            messagebox.showwarning("Warning", "Please select a flight first (double-click on a flight)")
            return

        new_status = self.flight_status_var.get()
        if self.manager.update_flight_status(flight_id, new_status):
            self.refresh_flight_list()
            self.refresh_jet_list()  # Refresh to show updated jet status
            self.refresh_dashboard()
            messagebox.showinfo("Success", f"Flight {flight_id} status updated to {new_status}\nCheck console for related status updates")
        else:
            messagebox.showerror("Error", "Failed to update flight status")

    # Maintenance methods
    def schedule_maintenance(self):
        try:
            description = self.maint_desc_text.get("1.0", tk.END).strip()
            completed = self.maint_completed_var.get() or None

            # The ID field is empty or readonly, let the manager auto-generate
            maint_id = self.manager.schedule_maintenance(
                "",  # Empty string triggers auto-generation
                self.maint_jet_var.get(),
                self.maint_date_var.get(),
                self.maint_type_var.get(),
                description
            )

            if maint_id and completed:
                self.manager.complete_maintenance(maint_id, completed)

            if maint_id:
                self.refresh_maintenance_list()
                self.clear_maintenance_form()
                self.status_var.set(f"Maintenance scheduled successfully with ID: {maint_id}")
                messagebox.showinfo("Success", f"Maintenance scheduled with ID: {maint_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_maintenance_form(self):
        self.maint_id_var.set("")
        self.maint_jet_var.set("")
        self.maint_date_var.set("")
        self.maint_type_var.set("Routine")
        self.maint_desc_text.delete("1.0", tk.END)
        self.maint_status_var.set("Scheduled")
        self.maint_completed_var.set("")

    def load_maintenance(self, event):
        selection = self.maint_tree.selection()
        if selection:
            item = self.maint_tree.item(selection[0])
            values = item['values']
            maint_id = values[0]
            maint = self.manager.maintenance.get(maint_id)
            if maint:
                self.maint_id_var.set(maint.maintenance_id)
                self.maint_jet_var.set(maint.jet_id)
                self.maint_date_var.set(maint.scheduled_date)
                self.maint_type_var.set(maint.maintenance_type)
                self.maint_desc_text.delete("1.0", tk.END)
                self.maint_desc_text.insert("1.0", maint.description)
                self.maint_status_var.set(maint.status)
                self.maint_completed_var.set(maint.completed_date or "")

    def refresh_maintenance_list(self):
        for item in self.maint_tree.get_children():
            self.maint_tree.delete(item)

        for maint in self.manager.maintenance.values():
            self.maint_tree.insert("", tk.END, values=(
                maint.maintenance_id,
                maint.jet_id,
                maint.scheduled_date,
                maint.maintenance_type,
                maint.description[:50] + "..." if len(maint.description) > 50 else maint.description,
                maint.status,
                maint.completed_date or ""
            ))

    def update_maintenance_status_gui(self):
        """Update maintenance status from the form"""
        maint_id = self.maint_id_var.get()
        if not maint_id:
            messagebox.showwarning("Warning", "Please select a maintenance record first (double-click on a record)")
            return

        new_status = self.maint_status_var.get()
        completed_date = self.maint_completed_var.get() if new_status == "Completed" else None

        if self.manager.update_maintenance_status(maint_id, new_status, completed_date):
            self.refresh_maintenance_list()
            self.refresh_jet_list()  # Refresh to show updated jet status
            self.refresh_dashboard()
            messagebox.showinfo("Success", f"Maintenance {maint_id} status updated to {new_status}\nCheck console for related status updates")
        else:
            messagebox.showerror("Error", "Failed to update maintenance status")

    # Dashboard methods
    def refresh_dashboard(self):
        self.stats_text.delete("1.0", tk.END)

        stats = f"""
        SYSTEM STATISTICS
        {'='*60}

        Total Passengers:     {len(self.manager.passengers)}
        Total Jets:           {len(self.manager.jets)}
        Total Flights:        {len(self.manager.flights)}
        Total Maintenance:    {len(self.manager.maintenance)}

        JETS BY STATUS
        {'='*60}
        """

        jet_status = {}
        for jet in self.manager.jets.values():
            jet_status[jet.status] = jet_status.get(jet.status, 0) + 1

        for status, count in jet_status.items():
            stats += f"        {status:20} {count}\n"

        stats += f"""
        FLIGHTS BY STATUS
        {'='*60}
        """

        flight_status = {}
        for flight in self.manager.flights.values():
            flight_status[flight.status] = flight_status.get(flight.status, 0) + 1

        for status, count in flight_status.items():
            stats += f"        {status:20} {count}\n"

        stats += f"""
        MAINTENANCE BY STATUS
        {'='*60}
        """

        maint_status = {}
        for maint in self.manager.maintenance.values():
            maint_status[maint.status] = maint_status.get(maint.status, 0) + 1

        for status, count in maint_status.items():
            stats += f"        {status:20} {count}\n"

        self.stats_text.insert("1.0", stats)

    def view_jet_schedule(self):
        jet_id = self.schedule_jet_var.get()
        if not jet_id:
            messagebox.showwarning("Warning", "Please enter a Jet ID")
            return

        self.schedule_text.delete("1.0", tk.END)

        if jet_id not in self.manager.jets:
            self.schedule_text.insert("1.0", f"Jet ID {jet_id} not found")
            return

        jet = self.manager.jets[jet_id]
        output = f"""
{'='*70}
SCHEDULE FOR JET: {jet.model} ({jet_id})
{'='*70}

JET DETAILS:
    Tail Number: {jet.tail_number}
    Capacity:    {jet.capacity} passengers
    Status:      {jet.status}

"""

        # Flights
        flights = [f for f in self.manager.flights.values() if f.jet_id == jet_id]
        output += f"FLIGHTS ({len(flights)}):\n"
        output += "-" * 70 + "\n"

        if flights:
            for flight in flights:
                output += f"""
Flight ID:   {flight.flight_id}
Route:       {flight.departure} → {flight.destination}
Departure:   {flight.departure_time}
Arrival:     {flight.arrival_time}
Passengers:  {len(flight.passenger_ids)}
Status:      {flight.status}
{"-" * 70}
"""
        else:
            output += "No flights scheduled\n\n"

        # Maintenance
        maintenance = [m for m in self.manager.maintenance.values() if m.jet_id == jet_id]
        output += f"\nMAINTENANCE ({len(maintenance)}):\n"
        output += "-" * 70 + "\n"

        if maintenance:
            for maint in maintenance:
                output += f"""
Maintenance ID: {maint.maintenance_id}
Type:           {maint.maintenance_type}
Scheduled:      {maint.scheduled_date}
Status:         {maint.status}
Description:    {maint.description}
Completed:      {maint.completed_date or 'N/A'}
{"-" * 70}
"""
        else:
            output += "No maintenance scheduled\n"

        self.schedule_text.insert("1.0", output)

    # General methods
    def refresh_all(self):
        self.refresh_passenger_list()
        self.refresh_jet_list()
        self.refresh_flight_list()
        self.refresh_maintenance_list()
        self.refresh_dashboard()
        self.status_var.set("All data refreshed")

    def save_data(self):
        self.manager.save_data()
        self.status_var.set("Data saved successfully")
        messagebox.showinfo("Success", "Data saved successfully")

    def exit_app(self):
        if messagebox.askyesno("Exit", "Do you want to save data before exiting?"):
            self.manager.save_data()
        self.root.quit()


def main():
    root = tk.Tk()
    app = JetManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

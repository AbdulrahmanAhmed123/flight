import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database_operations # Import database functions

def populate_reservations_tree(app_instance, reservations_list):
    """Populates the Treeview with the given list of reservation dictionaries."""
    for item in app_instance.reservations_tree.get_children():
        app_instance.reservations_tree.delete(item)

    for res in reservations_list:
        action_icons = "✏️  🗑️"
        app_instance.reservations_tree.insert("", "end", values=(
            res["Flight Number"],
            res["Name"],
            res["Departure"],
            res["Destination"],
            res["Date"],
            res["Seat"],
            action_icons
        ))

def search_reservations(app_instance):
    """Searches for a reservation by Flight Number and updates the Treeview."""
    search_flight_number_str = app_instance.search_entry.get().strip()
    if not search_flight_number_str or search_flight_number_str == "Search by Flight Number...":
        messagebox.showwarning("Search", "Please enter a Flight Number to search.")
        show_view_reservations_ui(app_instance) # Show all if search box is empty
        return

    # Clear existing items in the treeview
    for item in app_instance.reservations_tree.get_children():
        app_instance.reservations_tree.delete(item)

    found_reservation = database_operations.get_reservation_by_flight_number_db(search_flight_number_str)

    if found_reservation:
        action_icons = "✏️  🗑️"
        app_instance.reservations_tree.insert("", "end", values=(
            found_reservation["Flight Number"],
            found_reservation["Name"],
            found_reservation["Departure"],
            found_reservation["Destination"],
            found_reservation["Date"],
            found_reservation["Seat"],
            action_icons
        ))
    else:
        messagebox.showinfo("Search Results", f"No reservation found for Flight Number: {search_flight_number_str}")

def handle_table_click(app_instance, event):
    """Handles clicks on the Treeview to trigger edit or delete actions."""
    item_id = app_instance.reservations_tree.identify_row(event.y)
    if not item_id:
        return

    column = app_instance.reservations_tree.identify_column(event.x)
    col_name = app_instance.reservations_tree.heading(column, 'text')

    if col_name == "Actions":
        x, y, width, height = app_instance.reservations_tree.bbox(item_id, column)
        if x is not None:
            edit_icon_area_end = x + (width / 2)

            if event.x < edit_icon_area_end:
                app_instance.edit_reservation(event)
            else:
                app_instance.delete_reservation(event)

def show_view_reservations_ui(app_instance):
    """Displays the view reservations page UI."""
    app_instance.clear_content_area()

    header_frame = ttk.Frame(app_instance.content_area, style="TFrame")
    header_frame.pack(fill="x", pady=(20, 10))

    ttk.Label(header_frame, text="Your Reservations", style="Title.TLabel", font=("Inter", 20, "bold")).pack(side="left", padx=20)

    search_frame = ttk.Frame(header_frame, style="TFrame")
    search_frame.pack(side="right", padx=20)

    app_instance.search_entry = ttk.Entry(search_frame, width=30, font=("Inter", 10))
    app_instance.search_entry.insert(0, "Search by Flight Number...")
    app_instance.search_entry.pack(side="left", padx=(0, 10))

    ttk.Button(search_frame, text="Search", style="Primary.TButton", command=lambda: search_reservations(app_instance)).pack(side="left", padx=(0, 5))
    ttk.Button(search_frame, text="Book New Flight", style="Primary.TButton", command=app_instance.show_book_flight).pack(side="left")

    reservations_display_frame = ttk.Frame(app_instance.content_area, style="Card.TFrame", padding="20 20 20 20")
    reservations_display_frame.pack(fill="both", expand=True, padx=20, pady=10)

    app_instance.reservations = database_operations.get_all_reservations_db()

    if not app_instance.reservations:
        no_reservations_frame = ttk.Frame(reservations_display_frame, style="NoReservations.TFrame", padding="40 40 40 40")
        no_reservations_frame.pack(fill="both", expand=True)

        ttk.Label(no_reservations_frame, text="No Reservations Found", style="NoReservationsTitle.TLabel").pack(pady=(50, 10))
        ttk.Label(no_reservations_frame, text="You haven't booked any flights yet.", style="NoReservationsSubtitle.TLabel").pack(pady=(0, 30))

        ttk.Button(no_reservations_frame, text="Book Your First Flight", style="Large.Primary.TButton", command=app_instance.show_book_flight).pack(pady=(0, 50))
    else:
        columns = ("Flight Number", "Name", "Departure", "Destination", "Date", "Seat", "Actions")
        app_instance.reservations_tree = ttk.Treeview(reservations_display_frame, columns=columns, show="headings", style="Treeview")

        for col in columns:
            app_instance.reservations_tree.heading(col, text=col, anchor="w")
            if col == "Flight Number":
                app_instance.reservations_tree.column(col, width=100, stretch=tk.NO, anchor="center")
            elif col == "Actions":
                app_instance.reservations_tree.column(col, width=100, stretch=tk.NO, anchor="center")
            elif col == "Date":
                app_instance.reservations_tree.column(col, width=100, stretch=tk.NO)
            else:
                app_instance.reservations_tree.column(col, width=120, stretch=tk.YES)

        app_instance.reservations_tree.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(reservations_display_frame, orient="vertical", command=app_instance.reservations_tree.yview)
        app_instance.reservations_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        app_instance.reservations_tree.bind("<Button-1>", lambda e: handle_table_click(app_instance, e))

        populate_reservations_tree(app_instance, app_instance.reservations)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar

def open_date_picker(app_instance, date_entry_var):
    """Opens a Toplevel window with a calendar to select a date."""
    top = tk.Toplevel(app_instance.root)
    top.title("Select Date")
    top.transient(app_instance.root)
    top.grab_set()

    cal = Calendar(top, selectmode='day',
                   font="Inter 10",
                   background="#007bff", foreground='white',
                   normalbackground="white", weekendbackground="#f0f2f5",
                   bordercolor="#007bff", othermonthforeground="#888888",
                   othermonthbackground="#e0e0e0", headersbackground="#007bff",
                   headersforeground="white", selectbackground="#0056b3",
                   selectforeground="white")
    cal.pack(pady=20, padx=20)

    def set_date():
        selected_date = cal.selection_get()
        if selected_date:
            date_entry_var.set(selected_date.strftime("%Y-%m-%d"))
        top.destroy()

    ttk.Button(top, text="Select", style="Primary.TButton", command=set_date).pack(pady=10)

    app_instance.root.update_idletasks()
    x = app_instance.root.winfo_x() + (app_instance.root.winfo_width() // 2) - (top.winfo_width() // 2)
    y = app_instance.root.winfo_y() + (app_instance.root.winfo_height() // 2) - (top.winfo_height() // 2)
    top.geometry(f"+{x}+{y}")

def show_book_flight_ui(app_instance, reservation_data=None):
    """
    Displays the flight booking form, optionally pre-filling it for editing.
    :param app_instance: The main FlySkyApp instance.
    :param reservation_data: A dictionary containing reservation data to pre-fill the form, or None for a new booking.
    """
    app_instance.clear_content_area()

    app_instance.editing_flight_number = reservation_data.get("Flight Number") if reservation_data else None

    header_frame = ttk.Frame(app_instance.content_area, style="TFrame")
    header_frame.pack(fill="x", pady=(20, 10))

    ttk.Label(header_frame, text="Book a Flight", style="Title.TLabel", font=("Inter", 20, "bold")).pack(side="left", padx=20)

    form_frame = ttk.Frame(app_instance.content_area, style="Card.TFrame", padding="30 30 30 30")
    form_frame.pack(fill="x", padx=20, pady=10)

    form_frame.columnconfigure(0, weight=1)
    form_frame.columnconfigure(1, weight=3)

    # Full Name
    ttk.Label(form_frame, text="Full Name", style="FormLabel.TLabel", anchor="w").grid(row=0, column=0, sticky="w", pady=(10, 0), padx=5)
    name_entry = ttk.Entry(form_frame, width=50, style="TEntry")
    name_entry.insert(0, reservation_data.get("Name", "Enter your full name") if reservation_data else "Enter your full name")
    name_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15), padx=5)

    # Flight Number
    ttk.Label(form_frame, text="Flight Number", style="FormLabel.TLabel", anchor="w").grid(row=2, column=0, sticky="w", pady=(10, 0), padx=5)
    flight_number_entry = ttk.Entry(form_frame, width=50, style="TEntry")
    flight_number_entry.insert(0, reservation_data.get("Flight Number", "e.g. FS123") if reservation_data else "e.g. FS123")
    flight_number_entry.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15), padx=5)

    # Departure and Destination (side by side)
    ttk.Label(form_frame, text="Departure", style="FormLabel.TLabel", anchor="w").grid(row=4, column=0, sticky="w", pady=(10, 0), padx=5)
    departure_entry = ttk.Entry(form_frame, width=25, style="TEntry")
    departure_entry.insert(0, reservation_data.get("Departure", "e.g. New York") if reservation_data else "e.g. New York")
    departure_entry.grid(row=5, column=0, sticky="ew", pady=(0, 15), padx=5)

    ttk.Label(form_frame, text="Destination", style="FormLabel.TLabel", anchor="w").grid(row=4, column=1, sticky="w", pady=(10, 0), padx=5)
    destination_entry = ttk.Entry(form_frame, width=25, style="TEntry")
    destination_entry.insert(0, reservation_data.get("Destination", "e.g. London") if reservation_data else "e.g. London")
    destination_entry.grid(row=5, column=1, sticky="ew", pady=(0, 15), padx=5)

    # Date and Seat Number (side by side)
    ttk.Label(form_frame, text="Date", style="FormLabel.TLabel", anchor="w").grid(row=6, column=0, sticky="w", pady=(10, 0), padx=5)
    date_frame = ttk.Frame(form_frame, style="Card.TFrame")
    date_frame.grid(row=7, column=0, sticky="ew", pady=(0, 15), padx=5)

    app_instance.date_var.set(reservation_data.get("Date", "Pick a date") if reservation_data else "Pick a date")
    date_entry = ttk.Entry(date_frame, width=20, style="TEntry", textvariable=app_instance.date_var)
    date_entry.pack(side="left", fill="x", expand=True)

    calendar_icon = ttk.Label(date_frame, text="🗓️", font=("Segoe UI Emoji", 12), cursor="hand2")
    calendar_icon.pack(side="right", padx=(5, 0))
    calendar_icon.bind("<Button-1>", lambda e: open_date_picker(app_instance, app_instance.date_var))

    ttk.Label(form_frame, text="Seat Number", style="FormLabel.TLabel", anchor="w").grid(row=6, column=1, sticky="w", pady=(10, 0), padx=5)
    seat_number_entry = ttk.Entry(form_frame, width=25, style="TEntry")
    seat_number_entry.insert(0, reservation_data.get("Seat", "e.g. 12A") if reservation_data else "e.g. 12A")
    seat_number_entry.grid(row=7, column=1, sticky="ew", pady=(0, 15), padx=5)

    # Buttons (Cancel and Book Flight)
    button_frame = ttk.Frame(form_frame, style="Card.TFrame")
    button_frame.grid(row=8, column=0, columnspan=2, sticky="e", pady=(20, 0))

    ttk.Button(button_frame, text="Cancel", style="Secondary.TButton", command=app_instance.show_home).pack(side="left", padx=(0, 10))

    submit_button_text = "Update Reservation" if app_instance.editing_flight_number is not None else "Confirm Booking"
    ttk.Button(button_frame, text=submit_button_text, style="Primary.TButton", command=lambda: app_instance.submit_booking(
        name_entry.get(), flight_number_entry.get(), departure_entry.get(),
        destination_entry.get(), app_instance.date_var.get(), seat_number_entry.get()
    )).pack(side="left")

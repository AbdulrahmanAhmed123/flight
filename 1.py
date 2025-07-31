import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from tkinter import messagebox # For simple messages instead of alerts
from tkcalendar import Calendar # Import the Calendar widget
import learn as ln
class FlySkyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FlySky Reservations")
        self.root.geometry("900x700") # Increased size for the table
        self.root.minsize(800, 650) # Minimum size

        # List to store reservations
        self.reservations = [] # This will hold dictionaries of reservation data
        self.editing_reservation_index = None # To track which reservation is being edited

        # Configure a style for better aesthetics
        self.style = ttk.Style()
        self.style.theme_use('clam') # Use 'clam' theme for a modern look

        # Custom fonts
        self.title_font = tkFont.Font(family="Inter", size=24, weight="bold")
        self.subtitle_font = tkFont.Font(family="Inter", size=10)
        self.nav_font = tkFont.Font(family="Inter", size=10, weight="bold")
        self.card_title_font = tkFont.Font(family="Inter", size=14, weight="bold")
        self.card_desc_font = tkFont.Font(family="Inter", size=9)
        self.button_font = tkFont.Font(family="Inter", size=10, weight="bold")
        self.large_button_font = tkFont.Font(family="Inter", size=12, weight="bold")
        self.no_reservations_title_font = tkFont.Font(family="Inter", size=16, weight="bold")
        self.no_reservations_subtitle_font = tkFont.Font(family="Inter", size=10)
        self.form_label_font = tkFont.Font(family="Inter", size=10, weight="bold")
        self.entry_font = tkFont.Font(family="Inter", size=10)
        self.table_header_font = tkFont.Font(family="Inter", size=10, weight="bold")
        self.table_row_font = tkFont.Font(family="Inter", size=10)


        # Style configurations
        self.style.configure("TFrame", background="#f0f2f5") # Light grey background
        self.style.configure("Blue.TFrame", background="#007bff") # Blue for header
        self.style.configure("Title.TLabel", font=self.title_font, foreground="#333333", background="#f0f2f5")
        self.style.configure("Subtitle.TLabel", font=self.subtitle_font, foreground="#555555", background="#f0f2f5")
        self.style.configure("Nav.TLabel", font=self.nav_font, foreground="white", background="#007bff")
        self.style.configure("NavButton.TButton", font=self.nav_font, foreground="white", background="#007bff",
                             borderwidth=0, focuscolor="#007bff")
        self.style.map("NavButton.TButton",
                       background=[('active', '#0056b3')], # Darker blue on hover
                       foreground=[('active', 'white')])

        self.style.configure("Card.TFrame", background="white", relief="solid", borderwidth=1,
                             focusthickness=0, focuscolor="none") # White cards with border
        self.style.map("Card.TFrame",
                       background=[('active', '#e0f0ff')]) # Light blue on hover

        self.style.configure("CardTitle.TLabel", font=self.card_title_font, foreground="#007bff", background="white")
        self.style.configure("CardDesc.TLabel", font=self.card_desc_font, foreground="#666666", background="white")

        self.style.configure("Primary.TButton", font=self.button_font, foreground="white", background="#007bff",
                             relief="flat", borderwidth=0, padding=(10, 5))
        self.style.map("Primary.TButton",
                       background=[('active', '#0056b3')], # Darker blue on hover
                       foreground=[('active', 'white')])

        self.style.configure("Secondary.TButton", font=self.button_font, foreground="#007bff", background="white",
                             relief="flat", borderwidth=1, padding=(10, 5))
        self.style.map("Secondary.TButton",
                       background=[('active', '#e0e0e0')], # Light grey on hover
                       foreground=[('active', '#0056b3')])

        self.style.configure("Large.Primary.TButton", font=self.large_button_font, foreground="white", background="#007bff",
                             relief="flat", borderwidth=0, padding=(15, 10))
        self.style.map("Large.Primary.TButton",
                       background=[('active', '#0056b3')], # Darker blue on hover
                       foreground=[('active', 'white')])

        self.style.configure("NoReservations.TFrame", background="white", relief="solid", borderwidth=1,
                             focusthickness=0, focuscolor="none")
        self.style.configure("NoReservationsTitle.TLabel", font=self.no_reservations_title_font, foreground="#333333", background="white")
        self.style.configure("NoReservationsSubtitle.TLabel", font=self.no_reservations_subtitle_font, foreground="#666666", background="white")

        self.style.configure("FormLabel.TLabel", font=self.form_label_font, foreground="#333333", background="white")
        self.style.configure("TEntry", font=self.entry_font, padding=(5, 5)) # Padding for entry fields
        self.style.map("TEntry", fieldbackground=[('focus', '#e0f0ff')]) # Light blue on focus

        # Treeview Styles
        self.style.configure("Treeview.Heading", font=self.table_header_font, background="#e0e0e0", foreground="#333333")
        self.style.configure("Treeview", font=self.table_row_font, rowheight=30)
        self.style.map("Treeview", background=[('selected', '#cceeff')], foreground=[('selected', 'black')])


        self.create_widgets()
        ln.setup_flight_database()

    def create_widgets(self):
        # Main container frame
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.pack(fill="both", expand=True)

        # --- Top Navigation Bar ---
        nav_frame = ttk.Frame(main_frame, style="Blue.TFrame", height=50)
        nav_frame.pack(fill="x", pady=0)
        nav_frame.pack_propagate(False) # Prevent frame from resizing to content

        # FlySky Reservations Logo/Text
        logo_label = ttk.Label(nav_frame, text="✈️ FlySky Reservations", style="Nav.TLabel", font=("Inter", 14, "bold"))
        logo_label.pack(side="left", padx=20)

        # Navigation buttons on the right
        nav_buttons_frame = ttk.Frame(nav_frame, style="Blue.TFrame")
        nav_buttons_frame.pack(side="right", padx=10)

        ttk.Button(nav_buttons_frame, text="Home", style="NavButton.TButton", command=self.show_home).pack(side="left", padx=5)
        ttk.Button(nav_buttons_frame, text="Book Flight", style="NavButton.TButton", command=self.show_book_flight).pack(side="left", padx=5)
        ttk.Button(nav_buttons_frame, text="View Reservations", style="NavButton.TButton", command=self.show_view_reservations).pack(side="left", padx=5)

        # --- Main Content Area ---
        self.content_area = ttk.Frame(main_frame, style="TFrame")
        self.content_area.pack(fill="both", expand=True, padx=20, pady=20)

        self.show_home() # Show the home page initially


    def clear_content_area(self):
        """Clears all widgets from the content area."""
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content_area()

        # Welcome Section
        welcome_frame = ttk.Frame(self.content_area, style="TFrame")
        welcome_frame.pack(pady=(30, 20))

        welcome_label = ttk.Label(welcome_frame, text="Welcome to FlySky Reservations", style="Title.TLabel")
        welcome_label.pack(pady=(0, 10))

        subtitle_text = "Book your flights and manage your reservations with our simple and intuitive system."
        subtitle_label = ttk.Label(welcome_frame, text=subtitle_text, style="Subtitle.TLabel", wraplength=600)
        subtitle_label.pack()

        # Cards Section
        cards_frame = ttk.Frame(self.content_area, style="TFrame")
        cards_frame.pack(pady=30)

        # Book a Flight Card
        book_flight_card = ttk.Frame(cards_frame, style="Card.TFrame", padding="20 20 20 20")
        book_flight_card.pack(side="left", padx=20, ipadx=10, ipady=10) # ipadx/y for internal padding

        # Icon for Book a Flight (using a simple text emoji as a placeholder)
        ttk.Label(book_flight_card, text="✈️", font=("Segoe UI Emoji", 40), background="white").pack(pady=(0, 10))
        ttk.Label(book_flight_card, text="Book a Flight", style="CardTitle.TLabel").pack(pady=(0, 5))
        book_flight_desc = "Reserve your next flight by providing your details and flight information."
        ttk.Label(book_flight_card, text=book_flight_desc, style="CardDesc.TLabel", wraplength=200).pack(pady=(0, 15))
        ttk.Button(book_flight_card, text="Book Flight", style="Primary.TButton", command=self.show_book_flight).pack()

        # View Reservations Card
        view_reservations_card = ttk.Frame(cards_frame, style="Card.TFrame", padding="20 20 20 20")
        view_reservations_card.pack(side="left", padx=20, ipadx=10, ipady=10)

        # Icon for View Reservations
        ttk.Label(view_reservations_card, text="📋", font=("Segoe UI Emoji", 40), background="white").pack(pady=(0, 10))
        ttk.Label(view_reservations_card, text="View Reservations", style="CardTitle.TLabel").pack(pady=(0, 5))
        view_reservations_desc = "Manage your existing reservations, view details, edit or cancel if needed."
        ttk.Label(view_reservations_card, text=view_reservations_desc, style="CardDesc.TLabel", wraplength=200).pack(pady=(0, 15))
        ttk.Button(view_reservations_card, text="View Reservations", style="Primary.TButton", command=self.show_view_reservations).pack()

    def open_date_picker(self, date_entry_var):
        """Opens a Toplevel window with a calendar to select a date."""
        top = tk.Toplevel(self.root)
        top.title("Select Date")
        top.transient(self.root) # Make it appear on top of the main window
        top.grab_set() # Disable interaction with the main window

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
                date_entry_var.set(selected_date.strftime("%Y-%m-%d")) # Format as YYYY-MM-DD
            top.destroy()

        ttk.Button(top, text="Select", style="Primary.TButton", command=set_date).pack(pady=10)

        # Center the Toplevel window relative to its parent
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (top.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (top.winfo_height() // 2)
        top.geometry(f"+{x}+{y}")


    def show_book_flight(self, reservation_data=None):
        """
        Displays the flight booking form, optionally pre-filling it for editing.
        :param reservation_data: A dictionary containing reservation data to pre-fill the form, or None for a new booking.
        """
        self.clear_content_area()

        # Set the editing_reservation_index based on whether we are editing or creating
        if reservation_data:
            try:
                self.editing_reservation_index = self.reservations.index(reservation_data)
            except ValueError:
                self.editing_reservation_index = None # Should not happen if passed correctly
        else:
            self.editing_reservation_index = None

        # Header for the Book Flight page
        header_frame = ttk.Frame(self.content_area, style="TFrame")
        header_frame.pack(fill="x", pady=(20, 10))

        ttk.Label(header_frame, text="Book a Flight", style="Title.TLabel", font=("Inter", 20, "bold")).pack(side="left", padx=20)

        # Form content frame
        form_frame = ttk.Frame(self.content_area, style="Card.TFrame", padding="30 30 30 30")
        form_frame.pack(fill="x", padx=20, pady=10)

        # Grid configuration for the form
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=3) # Make entry fields wider

        # Full Name
        ttk.Label(form_frame, text="Full Name", style="FormLabel.TLabel", anchor="w").grid(row=0, column=0, sticky="w", pady=(10, 0), padx=5)
        full_name_entry = ttk.Entry(form_frame, width=50, style="TEntry")
        full_name_entry.insert(0, reservation_data.get("Name", "Enter your full name") if reservation_data else "Enter your full name")
        full_name_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15), padx=5)

        # Flight Number
        ttk.Label(form_frame, text="Flight Number", style="FormLabel.TLabel", anchor="w").grid(row=2, column=0, sticky="w", pady=(10, 0), padx=5)
        flight_number_entry = ttk.Entry(form_frame, width=50, style="TEntry")
        flight_number_entry.insert(0, reservation_data.get("Flight Number", "e.g. FS123") if reservation_data else "e.g. FS123")
        flight_number_entry.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15), padx=5)

        # Departure and Destination (side by side)
        # Departure
        ttk.Label(form_frame, text="Departure", style="FormLabel.TLabel", anchor="w").grid(row=4, column=0, sticky="w", pady=(10, 0), padx=5)
        departure_entry = ttk.Entry(form_frame, width=25, style="TEntry")
        departure_entry.insert(0, reservation_data.get("Departure", "e.g. New York") if reservation_data else "e.g. New York")
        departure_entry.grid(row=5, column=0, sticky="ew", pady=(0, 15), padx=5)

        # Destination
        ttk.Label(form_frame, text="Destination", style="FormLabel.TLabel", anchor="w").grid(row=4, column=1, sticky="w", pady=(10, 0), padx=5)
        destination_entry = ttk.Entry(form_frame, width=25, style="TEntry")
        destination_entry.insert(0, reservation_data.get("Destination", "e.g. London") if reservation_data else "e.g. London")
        destination_entry.grid(row=5, column=1, sticky="ew", pady=(0, 15), padx=5)

        # Date and Seat Number (side by side)
        # Date
        ttk.Label(form_frame, text="Date", style="FormLabel.TLabel", anchor="w").grid(row=6, column=0, sticky="w", pady=(10, 0), padx=5)
        date_frame = ttk.Frame(form_frame, style="Card.TFrame")
        date_frame.grid(row=7, column=0, sticky="ew", pady=(0, 15), padx=5)

        self.date_var = tk.StringVar(value=reservation_data.get("Date", "Pick a date") if reservation_data else "Pick a date")
        date_entry = ttk.Entry(date_frame, width=20, style="TEntry", textvariable=self.date_var)
        date_entry.pack(side="left", fill="x", expand=True)

        calendar_icon = ttk.Label(date_frame, text="🗓️", font=("Segoe UI Emoji", 12), cursor="hand2")
        calendar_icon.pack(side="right", padx=(5, 0))
        calendar_icon.bind("<Button-1>", lambda e: self.open_date_picker(self.date_var))

        # Seat Number
        ttk.Label(form_frame, text="Seat Number", style="FormLabel.TLabel", anchor="w").grid(row=6, column=1, sticky="w", pady=(10, 0), padx=5)
        seat_number_entry = ttk.Entry(form_frame, width=25, style="TEntry")
        seat_number_entry.insert(0, reservation_data.get("Seat", "e.g. 12A") if reservation_data else "e.g. 12A")
        seat_number_entry.grid(row=7, column=1, sticky="ew", pady=(0, 15), padx=5)

        # Buttons (Cancel and Book Flight)
        button_frame = ttk.Frame(form_frame, style="Card.TFrame")
        button_frame.grid(row=8, column=0, columnspan=2, sticky="e", pady=(20, 0))

        ttk.Button(button_frame, text="Cancel", style="Secondary.TButton", command=self.show_home).pack(side="left", padx=(0, 10))

        # Change button text based on whether it's an edit or new booking
        submit_button_text = "Update Reservation" if self.editing_reservation_index is not None else "Book Flight"
        ttk.Button(button_frame, text=submit_button_text, style="Primary.TButton", command=lambda: self.submit_booking(
            full_name_entry.get(), flight_number_entry.get(), departure_entry.get(),
            destination_entry.get(), self.date_var.get(), seat_number_entry.get()
        )).pack(side="left")

    def submit_booking(self, full_name, flight_number, departure, destination, date, seat_number):
        """Handles the submission of the booking form."""
        if not all([full_name, flight_number, departure, destination, date, seat_number]) or date == "Pick a date":
            messagebox.showerror("Booking Error", "Please fill in all fields.")
            return

        reservation = {
            "Flight Number": flight_number,
            "Name": full_name,
            "Departure": departure,
            "Destination": destination,
            "Date": date,
            "Seat": seat_number
        }

        if self.editing_reservation_index is not None:
            # Update existing reservation
            self.reservations[self.editing_reservation_index] = reservation
            ln.update_reservation(reservation_id=reservation["Flight Number"],new_data=reservation)
            print(f'update_reservation\n{ln.view_all_reservations()}')

            messagebox.showinfo("Reservation Updated",
                                f"Reservation for {full_name} on flight {flight_number} has been updated!")
        else:
            # Add new reservation
            self.reservations.append(reservation)
            ln.add_reservation(namev=full_name,departurev=departure,datev=date,destinationv=destination,flight_numberv=flight_number,seat_numberv=seat_number)
            print(f'add_reservation\n{ln.view_all_reservations()}')

            messagebox.showinfo("Booking Confirmed",
                                f"Booking for {full_name} on flight {flight_number} from {departure} to {destination} on {date} (Seat: {seat_number}) has been submitted!")

        self.editing_reservation_index = None # Reset editing state
        self.show_view_reservations() # Navigate to view reservations after booking or update

    def edit_reservation(self, event):
        """Initiates the editing process for a selected reservation."""
        item_id = self.reservations_tree.identify_row(event.y)
        values = self.reservations_tree.item(item_id, 'values')
        if not item_id:
            return

        # Get the index from the item's tags
        try:
            dataaaa=ln.get_reservation_by_id()
            a,_,_,_,_,_,_,=dataaaa[0]
            index_to_edit = int(self.reservations_tree.item(item_id, "tags")[0])
            reservation_to_edit = self.reservations[index_to_edit]
            ln.update_reservation(reservation_id=a)
            

            self.show_book_flight(reservation_data=reservation_to_edit) # Pass data to pre-fill form
        except (IndexError, ValueError):
            messagebox.showerror("Error", "Could not retrieve reservation for editing.")


    def delete_reservation(self, event):
        """Deletes a reservation from the list and refreshes the view."""
        item_id = self.reservations_tree.identify_row(event.y)
        values = self.reservations_tree.item(item_id, 'values')
        if not item_id:
            return

        if messagebox.askyesno("Delete Reservation", "Are you sure you want to delete this reservation?"):
            try:
                # Get the index from the item's tags
                index_to_delete = int(self.reservations_tree.item(item_id, "tags")[0])

                # Remove from the internal list
                del self.reservations[index_to_delete]
                ln.delete_reservation(reservation_id=values[0])
                print(f'delete_reservation\n{ln.view_all_reservations()}')

                # Re-populate the Treeview to ensure correct indices and display
                self.show_view_reservations()

            except (IndexError, ValueError):
                messagebox.showerror("Error", "Could not delete reservation.")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")


    def show_view_reservations(self):
        self.clear_content_area()

        # Header section for "Your Reservations"
        header_frame = ttk.Frame(self.content_area, style="TFrame")
        header_frame.pack(fill="x", pady=(20, 10))

        # "Your Reservations" title
        ttk.Label(header_frame, text="Your Reservations", style="Title.TLabel", font=("Inter", 20, "bold")).pack(side="left", padx=20)

        # Search bar and "Book New Flight" button
        search_frame = ttk.Frame(header_frame, style="TFrame")
        search_frame.pack(side="right", padx=20)

        # Search Entry
        search_entry = ttk.Entry(search_frame, width=30, font=("Inter", 10))
        search_entry.insert(0, "Search reservations...") # Placeholder text
        search_entry.pack(side="left", padx=(0, 10))

        # Book New Flight Button
        ttk.Button(search_frame, text="Book New Flight", style="Primary.TButton", command=self.show_book_flight).pack(side="left")

        # Main content area for reservations (or no reservations message)
        reservations_display_frame = ttk.Frame(self.content_area, style="Card.TFrame", padding="20 20 20 20")
        reservations_display_frame.pack(fill="both", expand=True, padx=20, pady=10)

        if not self.reservations:
            # "No Reservations Found" message
            no_reservations_frame = ttk.Frame(reservations_display_frame, style="NoReservations.TFrame", padding="40 40 40 40")
            no_reservations_frame.pack(fill="both", expand=True) # Fill the parent frame

            ttk.Label(no_reservations_frame, text="No Reservations Found", style="NoReservationsTitle.TLabel").pack(pady=(50, 10))
            ttk.Label(no_reservations_frame, text="You haven't booked any flights yet.", style="NoReservationsSubtitle.TLabel").pack(pady=(0, 30))

            # "Book Your First Flight" button
            ttk.Button(no_reservations_frame, text="Book Your First Flight", style="Large.Primary.TButton", command=self.show_book_flight).pack(pady=(0, 50))
        else:
            # Display reservations in a Treeview table
            columns = ("Flight Number", "Name", "Departure", "Destination", "Date", "Seat", "Actions")
            self.reservations_tree = ttk.Treeview(reservations_display_frame, columns=columns, show="headings", style="Treeview")

            # Define column headings
            for col in columns:
                self.reservations_tree.heading(col, text=col, anchor="w")
                # Adjust column width based on content or a fixed size
                if col == "Actions":
                    self.reservations_tree.column(col, width=100, stretch=tk.NO, anchor="center")
                elif col == "Date":
                    self.reservations_tree.column(col, width=100, stretch=tk.NO)
                else:
                    self.reservations_tree.column(col, width=120, stretch=tk.YES)

            # Pack the Treeview before populating it with data and binding events
            self.reservations_tree.pack(fill="both", expand=True)

            # Add a scrollbar
            scrollbar = ttk.Scrollbar(reservations_display_frame, orient="vertical", command=self.reservations_tree.yview)
            self.reservations_tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

            # Bind a click event to the Treeview for action icons
            self.reservations_tree.bind("<Button-1>", self.handle_table_click)
            data_reservations=ln.get_all_reservations_db()
            print(f'Populate the Treeview with data\n{data_reservations}')
            # Populate the Treeview with data
            for a0,a1,a2,a3,a4,a5,a6 in data_reservations:
                # Insert data into the treeview
                # Store the original index as a tag for easy retrieval during actions
                # Combine edit and delete emojis into a single string for the cell
                action_icons = "✏️  🗑️" # Two spaces for visual separation
                self.reservations_tree.insert("", "end", values=(
                  a1,a2,a3,a4,a5,a6,
                    action_icons
                )) # Use index as a simple tag for now

    def handle_table_click(self, event):
        """Handles clicks on the Treeview to trigger edit or delete actions."""
        item_id = self.reservations_tree.identify_row(event.y)
        
        if not item_id:
            return

        column = self.reservations_tree.identify_column(event.x)
        col_index = int(column[1:]) - 1 # Get numerical index from '#1', '#2' etc.

        # Check if the click was in the "Actions" column (last column)
        if col_index == len(self.reservations_tree["columns"]) - 1:
            # Determine if it's an edit or delete click based on x-coordinate within the cell
            x, y, width, height = self.reservations_tree.bbox(item_id, column)
            if x is not None: # Ensure the cell is visible
                # Calculate the approximate center of the edit icon (left part of the cell)
                # and delete icon (right part of the cell)
                # This is a heuristic and might need fine-tuning based on font and spacing
                edit_icon_area_end = x + (width / 2)
                
                if event.x < edit_icon_area_end:
                    self.edit_reservation(event)
                else:
                    self.delete_reservation(event)


if __name__ == "__main__":
    root = tk.Tk()
    app = FlySkyApp(root)
    root.mainloop()










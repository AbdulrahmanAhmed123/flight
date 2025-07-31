import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from tkinter import messagebox

# Import UI and database modules
import database_operations
import home_ui
import booking_ui
import reservations_ui
import action_handlers

class FlySkyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FlySky Reservations")
        self.root.geometry("900x700")
        self.root.minsize(800, 650)

        # Instance variables for UI elements that need to be accessed across modules
        self.reservations_tree = None # Will be set in reservations_ui
        self.search_entry = None # Will be set in reservations_ui
        self.date_var = tk.StringVar() # For date picker

        # State variable for editing mode
        self.editing_flight_number = None

        # Configure a style for better aesthetics
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Custom fonts (defined here as they are used across multiple UI modules)
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

        # Apply styles (can be moved to a separate styling module if it grows larger)
        self.style.configure("TFrame", background="#f0f2f5")
        self.style.configure("Blue.TFrame", background="#007bff")
        self.style.configure("Title.TLabel", font=self.title_font, foreground="#333333", background="#f0f2f5")
        self.style.configure("Subtitle.TLabel", font=self.subtitle_font, foreground="#555555", background="#f0f2f5")
        self.style.configure("Nav.TLabel", font=self.nav_font, foreground="white", background="#007bff")
        self.style.configure("NavButton.TButton", font=self.nav_font, foreground="white", background="#007bff",
                             borderwidth=0, focuscolor="#007bff")
        self.style.map("NavButton.TButton",
                       background=[('active', '#0056b3')],
                       foreground=[('active', 'white')])
        self.style.configure("Card.TFrame", background="white", relief="solid", borderwidth=1,
                             focusthickness=0, focuscolor="none")
        self.style.map("Card.TFrame",
                       background=[('active', '#e0f0ff')])
        self.style.configure("CardTitle.TLabel", font=self.card_title_font, foreground="#007bff", background="white")
        self.style.configure("CardDesc.TLabel", font=self.card_desc_font, foreground="#666666", background="white")
        self.style.configure("Primary.TButton", font=self.button_font, foreground="white", background="#007bff",
                             relief="flat", borderwidth=0, padding=(10, 5))
        self.style.map("Primary.TButton",
                       background=[('active', '#0056b3')],
                       foreground=[('active', 'white')])
        self.style.configure("Secondary.TButton", font=self.button_font, foreground="#007bff", background="white",
                             relief="flat", borderwidth=1, padding=(10, 5))
        self.style.map("Secondary.TButton",
                       background=[('active', '#e0e0e0')],
                       foreground=[('active', '#0056b3')])
        self.style.configure("Large.Primary.TButton", font=self.large_button_font, foreground="white", background="#007bff",
                             relief="flat", borderwidth=0, padding=(15, 10))
        self.style.map("Large.Primary.TButton",
                       background=[('active', '#0056b3')],
                       foreground=[('active', 'white')])
        self.style.configure("NoReservations.TFrame", background="white", relief="solid", borderwidth=1,
                             focusthickness=0, focuscolor="none")
        self.style.configure("NoReservationsTitle.TLabel", font=self.no_reservations_title_font, foreground="#333333", background="white")
        self.style.configure("NoReservationsSubtitle.TLabel", font=self.no_reservations_subtitle_font, foreground="#666666", background="white")
        self.style.configure("FormLabel.TLabel", font=self.form_label_font, foreground="#333333", background="white")
        self.style.configure("TEntry", font=self.entry_font, padding=(5, 5))
        self.style.map("TEntry", fieldbackground=[('focus', '#e0f0ff')])
        self.style.configure("Treeview.Heading", font=self.table_header_font, background="#e0e0e0", foreground="#333333")
        self.style.configure("Treeview", font=self.table_row_font, rowheight=30)
        self.style.map("Treeview", background=[('selected', '#cceeff')], foreground=[('selected', 'black')])

        database_operations.init_db() # Initialize the database
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.pack(fill="both", expand=True)

        nav_frame = ttk.Frame(main_frame, style="Blue.TFrame", height=50)
        nav_frame.pack(fill="x", pady=0)
        nav_frame.pack_propagate(False)

        logo_label = ttk.Label(nav_frame, text="✈️ FlySky Reservations", style="Nav.TLabel", font=("Inter", 14, "bold"))
        logo_label.pack(side="left", padx=20)

        nav_buttons_frame = ttk.Frame(nav_frame, style="Blue.TFrame")
        nav_buttons_frame.pack(side="right", padx=10)

        ttk.Button(nav_buttons_frame, text="Home", style="NavButton.TButton", command=self.show_home).pack(side="left", padx=5)
        ttk.Button(nav_buttons_frame, text="Book Flight", style="NavButton.TButton", command=self.show_book_flight).pack(side="left", padx=5)
        ttk.Button(nav_buttons_frame, text="View Reservations", style="NavButton.TButton", command=self.show_view_reservations).pack(side="left", padx=5)

        self.content_area = ttk.Frame(main_frame, style="TFrame")
        self.content_area.pack(fill="both", expand=True, padx=20, pady=20)

        self.show_home()

    def clear_content_area(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # --- UI Navigation Methods (calling functions from other modules) ---
    def show_home(self):
        home_ui.show_home_ui(self)

    def show_book_flight(self, reservation_data=None):
        booking_ui.show_book_flight_ui(self, reservation_data)

    def show_view_reservations(self):
        reservations_ui.show_view_reservations_ui(self)

    # --- Booking Logic (calls database operations) ---
    def submit_booking(self, name, flight_number, departure, destination, date, seat_number):
        if not all([name, flight_number, departure, destination, date, seat_number]) or date == "Pick a date":
            messagebox.showerror("Booking Error", "Please fill in all fields.")
            return

        reservation_data = {
            "Name": name,
            "Flight Number": flight_number,
            "Departure": departure,
            "Destination": destination,
            "Date": date,
            "Seat": seat_number
        }

        if self.editing_flight_number is not None:
            success = database_operations.update_reservation_db(self.editing_flight_number, reservation_data)
            if success:
                messagebox.showinfo("Reservation Updated",
                                    f"Reservation for {name} on flight {flight_number} has been updated!")
        else:
            success = database_operations.insert_reservation_db(reservation_data)
            if success:
                messagebox.showinfo("Booking Confirmed",
                                    f"Booking for {name} on flight {flight_number} from {departure} to {destination} on {date} (Seat: {seat_number}) has been submitted!")

        self.editing_flight_number = None
        self.show_view_reservations()

    # --- Action Handlers (delegated to action_handlers module) ---
    def edit_reservation(self, event):
        action_handlers.edit_reservation_handler(self, event)

    def delete_reservation(self, event):
        action_handlers.delete_reservation_handler(self, event)

    # --- Search Logic (delegated to reservations_ui module) ---
    def _search_reservations(self):
        reservations_ui.search_reservations(self)

    # --- Date Picker (delegated to booking_ui module) ---
    def open_date_picker(self, date_entry_var):
        booking_ui.open_date_picker(self, date_entry_var)

    # --- Populate Treeview (delegated to reservations_ui module) ---
    def _populate_reservations_tree(self, reservations_list):
        reservations_ui.populate_reservations_tree(self, reservations_list)

    # --- Table Click Handler (delegated to reservations_ui module) ---
    def handle_table_click(self, event):
        reservations_ui.handle_table_click(self, event)


if __name__ == "__main__":
    root = tk.Tk()
    app = FlySkyApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk

def show_home_ui(app_instance):
    """Displays the home page UI."""
    app_instance.clear_content_area()

    welcome_frame = ttk.Frame(app_instance.content_area, style="TFrame")
    welcome_frame.pack(pady=(30, 20))

    welcome_label = ttk.Label(welcome_frame, text="Welcome to FlySky Reservations", style="Title.TLabel")
    welcome_label.pack(pady=(0, 10))

    subtitle_text = "Book your flights and manage your reservations with our simple and intuitive system."
    subtitle_label = ttk.Label(welcome_frame, text=subtitle_text, style="Subtitle.TLabel", wraplength=600)
    subtitle_label.pack()

    cards_frame = ttk.Frame(app_instance.content_area, style="TFrame")
    cards_frame.pack(pady=30)

    # Book a Flight Card
    book_flight_card = ttk.Frame(cards_frame, style="Card.TFrame", padding="20 20 20 20")
    book_flight_card.pack(side="left", padx=20, ipadx=10, ipady=10)

    ttk.Label(book_flight_card, text="✈️", font=("Segoe UI Emoji", 40), background="white").pack(pady=(0, 10))
    ttk.Label(book_flight_card, text="Book a Flight", style="CardTitle.TLabel").pack(pady=(0, 5))
    book_flight_desc = "Reserve your next flight by providing your details and flight information."
    ttk.Label(book_flight_card, text=book_flight_desc, style="CardDesc.TLabel", wraplength=200).pack(pady=(0, 15))
    ttk.Button(book_flight_card, text="Book Flight", style="Primary.TButton", command=app_instance.show_book_flight).pack()

    # View Reservations Card
    view_reservations_card = ttk.Frame(cards_frame, style="Card.TFrame", padding="20 20 20 20")
    view_reservations_card.pack(side="left", padx=20, ipadx=10, ipady=10)

    ttk.Label(view_reservations_card, text="📋", font=("Segoe UI Emoji", 40), background="white").pack(pady=(0, 10))
    ttk.Label(view_reservations_card, text="View Reservations", style="CardTitle.TLabel").pack(pady=(0, 5))
    view_reservations_desc = "Manage your existing reservations, view details, edit or cancel if needed."
    ttk.Label(view_reservations_card, text=view_reservations_desc, style="CardDesc.TLabel", wraplength=200).pack(pady=(0, 15))
    ttk.Button(view_reservations_card, text="View Reservations", style="Primary.TButton", command=app_instance.show_view_reservations).pack()

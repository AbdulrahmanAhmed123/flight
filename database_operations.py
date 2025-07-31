import sqlite3
from tkinter import messagebox # Used for displaying errors

def init_db():
    """Initializes the SQLite database and creates the reservations table."""
    conn = None
    try:
        conn = sqlite3.connect('flights.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                flight_number TEXT PRIMARY KEY UNIQUE NOT NULL,
                name TEXT NOT NULL,
                departure TEXT NOT NULL,
                destination TEXT NOT NULL,
                date TEXT NOT NULL,
                seat_number TEXT NOT NULL
            )
        ''')
        conn.commit()
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

def insert_reservation_db(reservation_data):
    """Inserts a new reservation into the database."""
    conn = None
    try:
        conn = sqlite3.connect('flights.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reservations (flight_number, name, departure, destination, date, seat_number)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (reservation_data['Flight Number'], reservation_data['name'],
              reservation_data['Departure'], reservation_data['Destination'],
              reservation_data['Date'], reservation_data['Seat']))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Booking Error", f"Flight Number '{reservation_data['Flight Number']}' already exists. Please use a unique Flight Number.")
        return False
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error inserting reservation: {e}")
        return False
    finally:
        if conn:
            conn.close()

def update_reservation_db(old_flight_number, reservation_data):
    """Updates an existing reservation in the database."""
    conn = None
    try:
        conn = sqlite3.connect('flights.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE reservations
            SET name = ?, flight_number = ?, departure = ?, destination = ?, date = ?, seat_number = ?
            WHERE flight_number = ?
        ''', (reservation_data['name'], reservation_data['Flight Number'],
              reservation_data['Departure'], reservation_data['Destination'],
              reservation_data['Date'], reservation_data['Seat'], old_flight_number))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Update Error", f"New Flight Number '{reservation_data['Flight Number']}' already exists. Please use a unique Flight Number.")
        return False
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error updating reservation: {e}")
        return False
    finally:
        if conn:
            conn.close()

def delete_reservation_db(flight_number):
    """Deletes a reservation from the database."""
    conn = None
    try:
        conn = sqlite3.connect('flights.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM reservations WHERE flight_number = ?', (flight_number,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error deleting reservation: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_all_reservations_db():
    """Retrieves all reservations from the database."""
    conn = None
    try:
        conn = sqlite3.connect('flights.db')
        cursor = conn.cursor()
        cursor.execute('SELECT flight_number, name, departure, destination, date, seat_number FROM reservations')
        rows = cursor.fetchall()
        reservations_list = []
        for row in rows:
            reservations_list.append({
                "Flight Number": row[0],
                "Name": row[1],
                "Departure": row[2],
                "Destination": row[3],
                "Date": row[4],
                "Seat": row[5]
            })
        return reservations_list
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error fetching reservations: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_reservation_by_flight_number_db(flight_number):
    """Retrieves a single reservation from the database by Flight Number."""
    conn = None
    try:
        conn = sqlite3.connect('flights.db')
        cursor = conn.cursor()
        cursor.execute('SELECT flight_number, name, departure, destination, date, seat_number FROM reservations WHERE flight_number = ?', (flight_number,))
        row = cursor.fetchone()
        if row:
            return {
                "Flight Number": row[0],
                "Name": row[1],
                "Departure": row[2],
                "Destination": row[3],
                "Date": row[4],
                "Seat": row[5]
            }
        return None
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error fetching reservation by Flight Number: {e}")
        return None
    finally:
        if conn:
            conn.close()

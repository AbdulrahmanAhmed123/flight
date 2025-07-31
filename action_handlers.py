from tkinter import messagebox
import database_operations # Import database functions

def edit_reservation_handler(app_instance, event):
    """Initiates the editing process for a selected reservation."""
    item_id = app_instance.reservations_tree.identify_row(event.y)
    if not item_id:
        return

    values = app_instance.reservations_tree.item(item_id, 'values')
    if values and len(values) > 0:
        flight_number_to_edit = values[0]
        reservation_to_edit = database_operations.get_reservation_by_flight_number_db(flight_number_to_edit)
        if reservation_to_edit:
            app_instance.show_book_flight(reservation_data=reservation_to_edit)
        else:
            messagebox.showerror("Error", "Could not retrieve reservation details from database.")
    else:
        messagebox.showerror("Error", "No reservation data found for editing.")

def delete_reservation_handler(app_instance, event):
    """Deletes a reservation from the database and refreshes the view."""
    item_id = app_instance.reservations_tree.identify_row(event.y)
    if not item_id:
        return

    values = app_instance.reservations_tree.item(item_id, 'values')
    if not values or len(values) == 0:
        messagebox.showerror("Error", "No reservation data found for deletion.")
        return

    flight_number_to_delete = values[0]

    if messagebox.askyesno("Delete Reservation", f"Are you sure you want to delete reservation for Flight Number: {flight_number_to_delete}?"):
        success = database_operations.delete_reservation_db(flight_number_to_delete)
        if success:
            messagebox.showinfo("Deletion Successful", "Reservation deleted from database.")
            app_instance.show_view_reservations()
        else:
            messagebox.showerror("Deletion Failed", "Could not delete reservation from database.")

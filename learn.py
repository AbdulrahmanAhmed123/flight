import sqlite3
from tkinter import ttk, messagebox

def setup_flight_database():
    """
    يتصل بقاعدة بيانات flights.db SQLite أو ينشئها
    ويقوم بإعداد جدول 'reservations'.
    """
    conn = None # تهيئة الاتصال لضمان إغلاقه في النهاية
    try:
        # 1. الاتصال بقاعدة بيانات SQLite.
        # إذا لم يكن flights.db موجودًا، فسيتم إنشاؤه.
        # إذا كان موجودًا، فسيتم إنشاء اتصال به.
        conn = sqlite3.connect('flights.db')
        cursor = conn.cursor()
        print("تم الاتصال بنجاح بقاعدة بيانات flights.db")

        # 2. تصميم وإنشاء جدول 'reservations'.
        # سيخزن الجدول تفاصيل حجوزات الطيران.
        # - id: مفتاح أساسي، يزيد تلقائيًا لكل حجز جديد.
        # - name: يخزن اسم الراكب (نص).
        # - flight_number: يخزن رقم الرحلة (نص).
        # - departure: يخزن مدينة/مطار المغادرة (نص).
        # - destination: يخزن مدينة/مطار الوجهة (نص).
        # - date: يخزن تاريخ الرحلة (نص، مثال: 'YYYY-MM-DD').
        # - seat_number: يخزن رقم المقعد المخصص (نص).
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                flight_number TEXT NOT NULL,
                departure TEXT NOT NULL,
                destination TEXT NOT NULL,
                date TEXT NOT NULL,
                seat_number TEXT NOT NULL
            )
        ''')
        print("تم إنشاء جدول 'reservations' أو أنه موجود بالفعل.")
        conn.commit()
        print("اكتمل إعداد قاعدة البيانات.")

    except sqlite3.Error as e:
        # التعامل مع أي أخطاء SQLite قد تحدث.
        print(f"حدث خطأ: {e}")
    finally:
        # التأكد من إغلاق اتصال قاعدة البيانات، حتى لو حدث خطأ.
        if conn:
            conn.close()
            print("تم إغلاق اتصال قاعدة البيانات.")

def add_reservation(namev, flight_numberv, departurev, destinationv, datev, seat_numberv):
    """
    يضيف حجزًا جديدًا إلى جدول 'reservations'.
    """
    conn = None
    try:
        conn = sqlite3.connect('flights.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reservations (name, flight_number, departure, destination, date, seat_number)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (namev, flight_numberv, departurev, destinationv, datev, seat_numberv))
        conn.commit()
        print(f"تم إضافة الحجز لـ {namev} بنجاح.")
        return cursor.lastrowid # إرجاع ID الحجز الجديد
    except sqlite3.Error as e:
        print(f"خطأ في إضافة الحجز: {e}")
        return None
    finally:
        if conn:
            conn.close()

def update_reservation(reservation_id, new_data):
    """
    يحدث حجزًا موجودًا في جدول 'reservations'.
    new_data هو قاموس يحتوي على الأعمدة والقيم المراد تحديثها.
    """
    conn = None
    try:
        conn = sqlite3.connect('flights.db')
        cursor = conn.cursor()
        
        # بناء جزء SET من استعلام UPDATE ديناميكيًا
        set_clauses = []
        values = []
        for key, value in new_data.items():
            set_clauses.append(f"{key} = ?")
            values.append(value)
        
        if not set_clauses:
            print("لا توجد بيانات لتحديثها.")
            return False

        sql_query = f"UPDATE reservations SET {', '.join(set_clauses)} WHERE id = ?"
        values.append(reservation_id)

        cursor.execute(sql_query, tuple(values))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"تم تحديث الحجز رقم {reservation_id} بنجاح.")
            return True
        else:
            print(f"لم يتم العثور على حجز بالرقم {reservation_id} للتحديث.")
            return False
    except sqlite3.Error as e:
        print(f"خطأ في تحديث الحجز: {e}")
        return False
    finally:
        if conn:
            conn.close()

def delete_reservation(reservation_id):
    """
    يحذف حجزًا من جدول 'reservations' بناءً على معرف الحجز.
    """
    conn = None
    try:
        conn = sqlite3.connect('flights.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM reservations WHERE id = ?', (reservation_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"تم حذف الحجز رقم {reservation_id} بنجاح.")
            return True
        else:
            print(f"لم يتم العثور على حجز بالرقم {reservation_id} للحذف.")
            return False
    except sqlite3.Error as e:
        print(f"خطأ في حذف الحجز: {e}")
        return False
    finally:
        if conn:
            conn.close()

def view_all_reservations():
    """
    يعرض جميع الحجوزات الموجودة في جدول 'reservations'.
    """
    conn = None
    try:
        conn = sqlite3.connect('flights.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reservations')
        reservations = cursor.fetchall()

        if not reservations:
            print("لا توجد حجوزات لعرضها.")
            return []

        print("\n--- جميع الحجوزات ---")
        for row in reservations:
            print(f"ID: {row[0]}, الاسم: {row[1]}, الرحلة: {row[2]}, من: {row[3]}, إلى: {row[4]}, التاريخ: {row[5]}, المقعد: {row[6]}")
        print("--------------------\n")
        return reservations
    except sqlite3.Error as e:
        print(f"خطأ في عرض الحجوزات: {e}")
        return []
    finally:
        if conn:
            conn.close()
            

def get_reservation_by_id(reservation_id):
    """
    يسترد حجزًا واحدًا من جدول 'reservations' باستخدام معرف الحجز (ID).

    :param reservation_id: معرف الحجز المراد استرداده.
    :return: صف الحجز كقائمة (list) إذا تم العثور عليه، وإلا فـ None.
    """
    conn = None
    try:
        conn = sqlite3.connect('flights.db')
        cursor = conn.cursor()
        # تنفيذ استعلام SELECT مع شرط WHERE لاسترداد الحجز بالمعرف المحدد
        cursor.execute('SELECT * FROM reservations WHERE id = ?', (reservation_id,))
        reservation = cursor.fetchone() # استخدام fetchone() لأنه من المتوقع وجود صف واحد فقط

        if reservation:
            print(f"\n--- تفاصيل الحجز (ID: {reservation_id}) ---")
            print(f"ID: {reservation[0]}, الاسم: {reservation[1]}, الرحلة: {reservation[2]}, من: {reservation[3]}, إلى: {reservation[4]}, التاريخ: {reservation[5]}, المقعد: {reservation[6]}")
            print("------------------------------------\n")
            return list(reservation) # تحويل الصف إلى قائمة وإرجاعه
        else:
            print(f"لا يوجد حجز بالمعرف: {reservation_id}")
            return None
    except sqlite3.Error as e:
        print(f"خطأ في استرداد الحجز: {e}")
        return None
    finally:
        if conn:
            conn.close()

# مثال على كيفية استخدام الوظائف:
if __name__ == "__main__":
    # 1. إعداد قاعدة البيانات (سيتم إنشاؤها إذا لم تكن موجودة)
    setup_flight_database()

    # 2. عرض الحجوزات الموجودة (يجب أن تكون فارغة في البداية)
    print("\nعرض الحجوزات بعد الإعداد (يجب أن تكون فارغة):")
    view_all_reservations()

    # 3. إضافة بعض الحجوزات
    print("\nإضافة حجوزات جديدة:")
    res_id1 = add_reservation("أحمد علي", "FL101", "القاهرة", "دبي", "2025-08-15", "12A")
    res_id2 = add_reservation("ليلى محمد", "FL202", "جدة", "الرياض", "2025-09-01", "05B")
    add_reservation("خالد محمود", "FL303", "الدمام", "أبو ظبي", "2025-08-20", "21F")

    # 4. عرض الحجوزات بعد الإضافة
    print("\nعرض الحجوزات بعد الإضافة:")
    view_all_reservations()

    # 5. تحديث حجز (مثال: تحديث رقم مقعد أحمد علي)
    if res_id1:
        print(f"\nتحديث الحجز رقم {res_id1}:")
        update_reservation(res_id1, {'seat_number': '14C', 'destination': 'لندن'})
        print("\nعرض الحجوزات بعد التحديث:")
        view_all_reservations()

    # 6. حذف حجز (مثال: حذف حجز ليلى محمد)
    if res_id2:
        print(f"\nحذف الحجز رقم {res_id2}:")
        delete_reservation(res_id2)
        print("\nعرض الحجوزات بعد الحذف:")
        view_all_reservations()

    # 7. محاولة تحديث/حذف حجز غير موجود
    print("\nمحاولة تحديث حجز غير موجود:")
    update_reservation(999, {'name': 'اسم وهمي'})
    print("\nمحاولة حذف حجز غير موجود:")
    delete_reservation(998)
def get_all_reservations_db():
    """
    يسترجع جميع الحجوزات من جدول 'reservations' في قاعدة البيانات.
    """
    conn = None
    try:
        conn = sqlite3.connect('flights.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reservations')
        reservations = cursor.fetchall()
        return reservations
    except sqlite3.Error as e:
        messagebox.showerror("خطأ في قاعدة البيانات", f"خطأ في استرجاع الحجوزات: {e}")
        return []
    finally:
        if conn:
            conn.close()
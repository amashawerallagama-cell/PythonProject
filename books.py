import os
import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import time
import calendar
from datetime import datetime

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Database connection
def connect_db():
    return mysql.connector.connect(
        host="",
        user="",
        password="",
        database="online_bookstore" 
    )

# insert data
def insert_author(name, birthdate, address, phone_number):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO authors (author_name, birthdate, address, phone_number) VALUES (%s, %s, %s, %s)", (name, birthdate, address, phone_number))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Author details added successfully")

def insert_book(title, author_id, category, price):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author_id, category, price) VALUES (%s, %s, %s, %s)", (title, author_id, category, price))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Book details added successfully")

def insert_order(customer_name, book_id, order_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (customer_name, book_id, order_date) VALUES (%s, %s, %s)", (customer_name, book_id, order_date))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Order placed successfully")

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "user" and password == "root":
        login_window.destroy()
        main_interface()
    else:
        messagebox.showerror("Error", "Incorrect username or password")

def main_interface():
    root = tk.Tk()
    root.title("Online Bookstore Management System")
    root.state('zoomed')  

    # Set the background image
    bg_image_path = os.path.join(script_dir, 'images', 'wooden-table-with-blurred-background.jpg')
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((1366, 768), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    # Create main interface
    main_frame = tk.Frame(root, bg='lightsalmon', bd=5)
    main_frame.place(relwidth=0.8, relheight=0.1, relx=0.1, rely=0.05)

    title_label = tk.Label(main_frame, text="You have successfully logged in to the database, now you can manage your data!\nClick the buttons to open the forms to enter,update and delete the data.", font=('Segoe UI', 16), bg='coral')
    title_label.pack()

    # Add image at the right middle
    book_image_path = os.path.join(script_dir, 'images', 'book image.jpeg')
    book_image = Image.open(book_image_path)
    book_image = book_image.resize((500, 350), Image.LANCZOS)  
    book_photo = ImageTk.PhotoImage(book_image)

    book_label = tk.Label(root, image=book_photo)
    book_label.place(relx=0.05, rely=0.25)  

    def open_author_form():
        author_window = tk.Toplevel(root)
        author_window.title("Author Details")

        tk.Label(author_window, text="Author ID (for View/Update/Delete):").grid(row=0, column=0, sticky='w')
        author_id_entry = tk.Entry(author_window)
        author_id_entry.grid(row=0, column=1, padx=5)

        tk.Label(author_window, text="Author Name:").grid(row=1, column=0, sticky='w')
        author_name_entry = tk.Entry(author_window)
        author_name_entry.grid(row=1, column=1, padx=5)

        tk.Label(author_window, text="Birthdate (YYYY-MM-DD):").grid(row=2, column=0, sticky='w')
        birthdate_entry = tk.Entry(author_window)
        birthdate_entry.grid(row=2, column=1, padx=5)

        tk.Label(author_window, text="Address:").grid(row=3, column=0, sticky='w')
        address_entry = tk.Entry(author_window)
        address_entry.grid(row=3, column=1, padx=5)

        tk.Label(author_window, text="Phone Number:").grid(row=4, column=0, sticky='w')
        phone_number_entry = tk.Entry(author_window)
        phone_number_entry.grid(row=4, column=1, padx=5)

        def clear_fields():
            author_id_entry.delete(0, tk.END)
            author_name_entry.delete(0, tk.END)
            birthdate_entry.delete(0, tk.END)
            address_entry.delete(0, tk.END)
            phone_number_entry.delete(0, tk.END)

        def update_author():
            author_id = author_id_entry.get()
            name = author_name_entry.get()
            birthdate = birthdate_entry.get()
            address = address_entry.get()
            phone_number = phone_number_entry.get()
            
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE authors SET author_name=%s, birthdate=%s, address=%s, phone_number=%s WHERE author_id=%s",
                           (name, birthdate, address, phone_number, author_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Author details updated successfully")
            clear_fields()

        def delete_author():
            author_id = author_id_entry.get()
            
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM authors WHERE author_id=%s", (author_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Author deleted successfully")
            clear_fields()

        def view_author():
            author_id = author_id_entry.get()
            if not author_id:
                messagebox.showwarning("Input Error", "Author ID is required for viewing author details.")
                return

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT author_name, birthdate, address, phone_number FROM authors WHERE author_id=%s", (author_id,))
            result = cursor.fetchone()

            if result:
                author_name_entry.delete(0, tk.END)
                author_name_entry.insert(0, result[0])
                
                birthdate_entry.delete(0, tk.END)
                birthdate_entry.insert(0, result[1])
                
                address_entry.delete(0, tk.END)
                address_entry.insert(0, result[2])
                
                phone_number_entry.delete(0, tk.END)
                phone_number_entry.insert(0, result[3])
            else:
                messagebox.showinfo("Not Found", "Author ID not found in the database.")
            conn.close()
            
        def read_all_authors():
            read_window = tk.Toplevel(root)
            read_window.title("All Authors")

            columns = ('Author ID', 'Author Name', 'Birthdate', 'Address', 'Phone Number')
            tree = ttk.Treeview(read_window, columns=columns, show='headings')

            for col in columns:
                tree.heading(col, text=col)

            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar = ttk.Scrollbar(read_window, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT author_id, author_name, birthdate, address, phone_number FROM authors")
            result = cursor.fetchall()

            for row in result:
                tree.insert('', tk.END, values=row)

            conn.close()

     #Buttons
        tk.Button(author_window, text="Add Author", command=lambda: insert_author(author_name_entry.get(), birthdate_entry.get(), address_entry.get(), phone_number_entry.get()), bg='green', fg='white').grid(row=5, column=0, padx=5, pady=10, columnspan=2, sticky='ew')
        tk.Button(author_window, text="View Author", command=view_author, bg='orange', fg='white').grid(row=5, column=2, padx=5, pady=10)
        tk.Button(author_window, text="Update Author", command=update_author, bg='yellow', fg='black').grid(row=5, column=3, padx=5, pady=10)
        tk.Button(author_window, text="Delete Author", command=delete_author, bg='red', fg='white').grid(row=5, column=4, padx=5, pady=10)
        tk.Button(author_window, text="Clear", command=clear_fields, bg='blue', fg='white').grid(row=5, column=5, padx=5, pady=10)

        read_all_authors_button = tk.Button(author_window, text="READ ALL AUTHORS", command=read_all_authors, bg='lightgreen', fg='black')
        read_all_authors_button.grid(row=6, column=0, columnspan=6, pady=20)

    def open_book_form():
        book_window = tk.Toplevel(root)
        book_window.title("Book Details")

        tk.Label(book_window, text="Book ID (for View/Update/Delete):").grid(row=0, column=0, sticky='w')
        book_id_entry = tk.Entry(book_window)
        book_id_entry.grid(row=0, column=1, padx=5)

        tk.Label(book_window, text="Title:").grid(row=1, column=0, sticky='w')
        title_entry = tk.Entry(book_window)
        title_entry.grid(row=1, column=1, padx=5)

        tk.Label(book_window, text="Author ID:").grid(row=2, column=0, sticky='w')
        author_id_entry = tk.Entry(book_window)
        author_id_entry.grid(row=2, column=1, padx=5)

        tk.Label(book_window, text="Category:").grid(row=3, column=0, sticky='w')
        category_entry = tk.Entry(book_window)
        category_entry.grid(row=3, column=1, padx=5)

        tk.Label(book_window, text="Price:").grid(row=4, column=0, sticky='w')
        price_entry = tk.Entry(book_window)
        price_entry.grid(row=4, column=1, padx=5)

        def clear_fields():
            book_id_entry.delete(0, tk.END)
            title_entry.delete(0, tk.END)
            author_id_entry.delete(0, tk.END)
            category_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)

        def update_book():
            book_id = book_id_entry.get()
            title = title_entry.get()
            author_id = author_id_entry.get()
            category = category_entry.get()
            price = price_entry.get()

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE books SET title=%s, author_id=%s, category=%s, price=%s WHERE book_id=%s",
                        (title, author_id, category, price, book_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Book details updated successfully")
            clear_fields()

        def delete_book():
            book_id = book_id_entry.get()

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE book_id=%s", (book_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Book deleted successfully")
            clear_fields()
        def view_book():
            book_id = book_id_entry.get()
            if not book_id:
                messagebox.showwarning("Input Error", "Book ID is required for viewing book details.")
                return

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT title, author_id, category, price FROM books WHERE book_id=%s", (book_id,))
            result = cursor.fetchone()

            if result:
                title_entry.delete(0, tk.END)
                title_entry.insert(0, result[0])

                author_id_entry.delete(0, tk.END)
                author_id_entry.insert(0, result[1])

                category_entry.delete(0, tk.END)
                category_entry.insert(0, result[2])

                price_entry.delete(0, tk.END)
                price_entry.insert(0, result[3])
            else:
                messagebox.showinfo("Not Found", "Book ID not found in the database.")
            conn.close()
         # Read all books function
        def read_all_books():
            books_window = tk.Toplevel(book_window)
            books_window.title("All Books")

            # Treeview to display the books
            columns = ('Book ID', 'Title', 'Author ID', 'Category', 'Price')
            tree = ttk.Treeview(books_window, columns=columns, show='headings')

            # Define headings
            for col in columns:
                tree.heading(col, text=col)

            tree.grid(row=0, column=0, padx=10, pady=10)

            # Scrollbar for the Treeview
            scrollbar = ttk.Scrollbar(books_window, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.grid(row=0, column=1, sticky='ns')

            # Fetch and display all books from the database
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT book_id, title, author_id, category, price FROM books")
            books = cursor.fetchall()

            for book in books:
                tree.insert('', tk.END, values=book)

            conn.close()

         #Buttons
        tk.Button(book_window, text="Add Book", command=lambda: insert_book(title_entry.get(), author_id_entry.get(), category_entry.get(), price_entry.get()), bg='green', fg='white').grid(row=5, column=0, padx=5, pady=10, columnspan=2, sticky='ew')
        tk.Button(book_window, text="View Book", command=view_book, bg='orange', fg='white').grid(row=5, column=2, padx=5, pady=10)
        tk.Button(book_window, text="Update Book", command=update_book, bg='yellow', fg='black').grid(row=5, column=3, padx=5, pady=10)
        tk.Button(book_window, text="Delete Book", command=delete_book, bg='red', fg='white').grid(row=5, column=4, padx=5, pady=10)
        tk.Button(book_window, text="Clear", command=clear_fields, bg='blue', fg='white').grid(row=5, column=5, padx=5, pady=10)
        
        read_all_books_button = tk.Button(book_window, text="READ ALL BOOKS", command=read_all_books, bg='lightgreen', fg='black')
        read_all_books_button.grid(row=6, column=0, columnspan=6, pady=20)


    def open_order_form():
        order_window = tk.Toplevel(root)
        order_window.title("Order Details")

        # Add Order ID for Update/Delete operations
        tk.Label(order_window, text="Order ID (for View/Update/Delete):").grid(row=0, column=0, sticky='w')
        order_id_entry = tk.Entry(order_window)
        order_id_entry.grid(row=0, column=1, padx=5)

        tk.Label(order_window, text="Customer Name:").grid(row=1, column=0, sticky='w')
        customer_name_entry = tk.Entry(order_window)
        customer_name_entry.grid(row=1, column=1, padx=5)

        tk.Label(order_window, text="Book ID:").grid(row=2, column=0, sticky='w')
        book_id_entry = tk.Entry(order_window)
        book_id_entry.grid(row=2, column=1, padx=5)

        tk.Label(order_window, text="Order Date (YYYY-MM-DD):").grid(row=3, column=0, sticky='w')
        order_date_entry = tk.Entry(order_window)
        order_date_entry.grid(row=3, column=1, padx=5)

        def clear_fields():
            order_id_entry.delete(0, tk.END)
            customer_name_entry.delete(0, tk.END)
            book_id_entry.delete(0, tk.END)
            order_date_entry.delete(0, tk.END)

        def update_order():
            order_id = order_id_entry.get()
            if not order_id:
                messagebox.showwarning("Input Error", "Order ID is required for updating an order.")
                return
            
            customer_name = customer_name_entry.get()
            book_id = book_id_entry.get()
            order_date = order_date_entry.get()

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE orders SET customer_name=%s, book_id=%s, order_date=%s WHERE order_id=%s",
                        (customer_name, book_id, order_date, order_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Order details updated successfully")
            clear_fields()

        def delete_order():
            order_id = order_id_entry.get()
            if not order_id:
                messagebox.showwarning("Input Error", "Order ID is required for deleting an order.")
                return

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM orders WHERE order_id=%s", (order_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Order deleted successfully")
            clear_fields()

        def view_order():
            order_id = order_id_entry.get()
            if not order_id:
                messagebox.showwarning("Input Error", "Order ID is required for viewing order details.")
                return

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT customer_name, book_id, order_date FROM orders WHERE order_id=%s", (order_id,))

            result = cursor.fetchone()

            if result:
                customer_name_entry.delete(0, tk.END)
                customer_name_entry.insert(0, result[0])

                book_id_entry.delete(0, tk.END)
                book_id_entry.insert(0, result[1])

                order_date_entry.delete(0, tk.END)
                order_date_entry.insert(0, result[2])

            else:
                messagebox.showinfo("Not Found", "Order ID not found in the database.")
            conn.close()
             # Function to read all orders and display in Treeview
        def read_all_orders():
            read_window = tk.Toplevel(order_window)
            read_window.title("All Orders")

            # Create a Treeview to display the order details
            columns = ('Order ID', 'Customer Name', 'Book ID', 'Order Date')
            tree = ttk.Treeview(read_window, columns=columns, show='headings')

            # Define column headings
            for col in columns:
                tree.heading(col, text=col)

            tree.grid(row=0, column=0, padx=10, pady=10)

            # Scrollbar for the Treeview
            scrollbar = ttk.Scrollbar(read_window, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.grid(row=0, column=1, sticky='ns')

            # Fetch data from the database
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT order_id, customer_name, book_id, order_date FROM orders")
            result = cursor.fetchall()

            # Insert data into the Treeview
            for row in result:
                tree.insert('', tk.END, values=row)

            conn.close()

        #Buttons
        tk.Button(order_window, text="Place Order", command=lambda: insert_order(customer_name_entry.get(), book_id_entry.get(), order_date_entry.get()), bg='green', fg='white').grid(row=5, column=0, padx=5, pady=10, columnspan=2, sticky='ew')
        tk.Button(order_window, text="View Order", command=view_order, bg='orange', fg='white').grid(row=5, column=2, padx=5, pady=10)
        tk.Button(order_window, text="Update Order", command=update_order, bg='yellow', fg='black').grid(row=5, column=3, padx=5, pady=10)
        tk.Button(order_window, text="Delete Order", command=delete_order, bg='red', fg='white').grid(row=5, column=4, padx=5, pady=10)
        tk.Button(order_window, text="Clear", command=clear_fields, bg='blue', fg='white').grid(row=5, column=5, padx=5, pady=10)
        
        read_all_orders_button = tk.Button(order_window, text="READ ALL ORDERS", command=read_all_orders, bg='lightgreen', fg='black')
        read_all_orders_button.grid(row=6, column=0, columnspan=6, pady=20)

        order_window.mainloop()


    # Buttons to open forms
    author_button = tk.Button(root, text="ENTER AUTHOR DETAILS", font=('Times New Roman', 12), command=open_author_form, bg='sandybrown', fg='white')
    author_button.place(relx=0.5, rely=0.3, relwidth=0.3, relheight=0.1)

    book_button = tk.Button(root, text="ENTER BOOK DETAILS", font=('Times New Roman', 12), command=open_book_form, bg='peachpuff', fg='black')
    book_button.place(relx=0.5, rely=0.45, relwidth=0.3, relheight=0.1)

    order_button = tk.Button(root, text="PLACE AN ORDER", font=('Times New Roman', 12), command=open_order_form, bg='peru', fg='white')
    order_button.place(relx=0.5, rely=0.6, relwidth=0.3, relheight=0.1)


    root.mainloop()


# Function to highlight current day in the calendar
def get_highlighted_calendar(year, month):
    now = datetime.now()
    cal = calendar.TextCalendar(calendar.SUNDAY)
    cal_str = cal.formatmonth(year, month)
    current_day = now.day
    if now.year == year and now.month == month:
        cal_str = cal_str.replace(f"{current_day:2d}", f"[{current_day:2d}]")
    return cal_str

# Tkinter GUI for login
login_window = tk.Tk()
login_window.title("Login")
login_window.state('zoomed')  # Maximize the window

# Set the background image for login window
bg_image_path = os.path.join(script_dir, 'images', 'test2.jpg')
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((1366, 768), Image.LANCZOS)  
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(login_window, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

title_label = tk.Label(login_window, text="Welcome to the Database of Wisdom Bookstore", font=('Georgia', 25), bg='chocolate')
title_label.pack()

info_label = tk.Label(login_window, text="Here you can enter, read, update and delete author, books and order details.\nPlease enter your username and password to continue.", font=('Garamond', 17), fg='black')
info_label.pack(pady=10) 

# Login frame
login_frame = tk.Frame(login_window, bg='white', bd=5)
login_frame.place(relwidth=0.4, relheight=0.4, relx=0.1, rely=0.3)

tk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=10, pady=10)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(login_frame, show='*')
password_entry.grid(row=1, column=1, padx=10, pady=10)

login_button = tk.Button(login_frame, text="Login", command=login, bg='mediumspringgreen')
login_button.grid(row=2, columnspan=2, pady=10)

# Digital clock
def update_clock():
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    login_window.after(1000, update_clock)

clock_label = tk.Label(login_window, font=('Helvetica', 20), bg='gold')
clock_label.place(relx=0.1, rely=0.75, relwidth=0.4, relheight=0.1)
update_clock()

# Calendar with highlighted current day
now = datetime.now()
highlighted_calendar = get_highlighted_calendar(now.year, now.month)
calendar_label = tk.Label(login_window, text=highlighted_calendar, font=('Courier', 20), bg='orange')
calendar_label.place(relx=0.6, rely=0.3, relwidth=0.3, relheight=0.55)

login_window.mainloop()



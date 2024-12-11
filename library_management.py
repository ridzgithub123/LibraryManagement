
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import csv
import os

# File paths for CSV data
BOOKS_FILE = "books.csv"
MOVIES_FILE = "movies.csv"
MEMBERS_FILE = "members.csv"
TRANSACTIONS_FILE = "transactions.csv"
USERS_FILE = "users.csv"

# Initialize data files if not present
def initialize_files():
    for file, headers in [
        (BOOKS_FILE, ["Book ID", "Title", "Author", "Available"]),
        (MEMBERS_FILE, ["Member ID", "First Name", "Last Name", "Contact Name", "Contact Address", "Aadhaar Card No", "Start Date", "End Date", "Membership Duration"]),
        (TRANSACTIONS_FILE, ["Transaction ID", "Book ID", "Member ID", "Date", "Type"]),
        (USERS_FILE, ["Username", "Password", "Role"]),
    ]:
        if not os.path.exists(file):
            with open(file, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)

# GUI Application class
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.current_role = None
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_screen()

        ttk.Label(self.root, text="Login", font=("Arial", 18)).pack(pady=20)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(form_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(form_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Login", command=self.handle_login).grid(row=2, column=0, pady=10)
        ttk.Button(form_frame, text="Register", command=self.show_register_screen).grid(row=2, column=1, pady=10)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Both fields are required")
            return

        with open(USERS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Username"] == username and row["Password"] == password:
                    self.current_role = row["Role"]
                    if self.current_role == "Admin":
                        self.show_admin_homepage()
                    elif self.current_role == "User":
                        self.show_user_homepage()
                    return

        messagebox.showerror("Error", "Invalid credentials")

    def show_register_screen(self):
        self.clear_screen()

        ttk.Label(self.root, text="Register", font=("Arial", 18)).pack(pady=20)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.reg_username_entry = ttk.Entry(form_frame)
        self.reg_username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.reg_password_entry = ttk.Entry(form_frame, show="*")
        self.reg_password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Role:").grid(row=2, column=0, padx=5, pady=5)
        self.reg_role_combo = ttk.Combobox(form_frame, values=["Admin", "User"], state="readonly")
        self.reg_role_combo.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Register", command=self.handle_register).grid(row=3, columnspan=2, pady=10)
        ttk.Button(form_frame, text="Back", command=self.show_login_screen).grid(row=4, columnspan=2, pady=10)

    def handle_register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        role = self.reg_role_combo.get()

        if not username or not password or not role:
            messagebox.showerror("Error", "All fields are required")
            return

        with open(USERS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Username"] == username:
                    messagebox.showerror("Error", "Username already exists")
                    return

        with open(USERS_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([username, password, role])

        messagebox.showinfo("Success", "Registration successful")
        self.show_login_screen()

    def show_admin_homepage(self):
        self.clear_screen()
        ttk.Label(self.root, text="Admin Homepage", font=("Arial", 18)).pack(pady=20)
        ttk.Button(self.root, text="Maintenance Menu", command=self.show_maintenance_menu).pack(pady=10)
        ttk.Button(self.root, text="Report Menu", command=self.show_report_menu).pack(pady=10)
        ttk.Button(self.root, text="Transaction Menu", command=self.show_transaction_menu).pack(pady=10)
        ttk.Button(self.root, text="Logout", command=self.show_login_screen).pack(pady=10)

    def show_user_homepage(self):
        self.clear_screen()
        ttk.Label(self.root, text="User Homepage", font=("Arial", 18)).pack(pady=20)
        ttk.Button(self.root, text="Report Menu", command=self.show_report_menu).pack(pady=10)
        ttk.Button(self.root, text="Transaction Menu", command=self.show_transaction_menu).pack(pady=10)
        ttk.Button(self.root, text="Logout", command=self.show_login_screen).pack(pady=10)

    def show_maintenance_menu(self):
        self.clear_screen()
        ttk.Label(self.root, text="Maintenance Menu", font=("Arial", 18)).pack(pady=20)
        ttk.Button(self.root, text="Membership Add", command=self.show_add_membership).pack(pady=10)
        ttk.Button(self.root, text="Membership Update", command=self.show_update_membership).pack(pady=10)
        ttk.Button(self.root, text="Books/Movies Add", command=self.show_add_books).pack(pady=10)
        ttk.Button(self.root, text="Books/Movies Update", command=self.show_update_books).pack(pady=10)
        ttk.Button(self.root, text="User Management Add", command=self.show_add_user).pack(pady=10)
        ttk.Button(self.root, text="User Management Update", command=self.show_update_user).pack(pady=10)
        ttk.Button(self.root, text="Log Out", command=self.show_login_screen).pack(pady=10)

    def show_report_menu(self):
        self.clear_screen()

        report_frame = ttk.Frame(self.root)
        report_frame.pack(pady=20)

        # Title
        ttk.Label(report_frame, text="Report Menu", font=("Arial", 18)).pack(pady=20)

        # Master List of Books
        ttk.Button(report_frame, text="Master List of Books", command=self.show_master_list_books).pack(anchor="w", padx=10, pady=5)

        # Master List of Movies
        ttk.Button(report_frame, text="Master List of Movies", command=self.show_master_list_movies).pack(anchor="w", padx=10, pady=5)

        # Master List of Memberships
        ttk.Button(report_frame, text="Master List of Memberships", command=self.show_master_list_memberships).pack(anchor="w", padx=10, pady=5)

        # Active Issues
        ttk.Button(report_frame, text="Active Issues", command=self.show_active_issues).pack(anchor="w", padx=10, pady=5)

        # Overdue Returns
        ttk.Button(report_frame, text="Overdue Returns", command=self.show_overdue_returns).pack(anchor="w", padx=10, pady=5)

        # Pending Issue Requests
        ttk.Button(report_frame, text="Pending Issue Requests", command=self.show_pending_issue_requests).pack(anchor="w", padx=10, pady=5)

        # Log Out button
        ttk.Button(report_frame, text="Log Out", command=self.show_login_screen).pack(pady=20)

    def show_master_list_books(self):
        self.clear_screen()

        # Table header
        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=20)

        columns = ["Serial No", "Name of Book", "Author Name", "Category", "Status", "Cost", "Procurement Date"]
        treeview = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=150)

        # Load data from books.csv and populate the table
        with open(BOOKS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                treeview.insert("", "end", values=[row["Serial No"], row["Name of Book"], row["Author Name"], row["Category"], row["Status"], row["Cost"], row["Procurement Date"]])

        treeview.pack()

        # Back and Logout buttons
        ttk.Button(self.root, text="Back", command=self.show_report_menu).pack(pady=10)
        ttk.Button(self.root, text="Log Out", command=self.show_login_screen).pack(pady=10)


    def show_master_list_movies(self):
        self.clear_screen()
        self.clear_screen()
        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=20)

        columns = ["Serial No", "Name of Movie", "Author Name", "Category", "Status", "Cost", "Procurement Date"]
        treeview = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=150)

        with open(BOOKS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                treeview.insert("", "end", values=[row["Serial No"], row["Name of Movie"], row["Author Name"], row["Category"], row["Status"], row["Cost"], row["Procurement Date"]])

        treeview.pack()
        ttk.Button(self.root, text="Back", command=self.show_report_menu).pack(pady=10)
        ttk.Button(self.root, text="Log Out", command=self.show_login_screen).pack(pady=10)
    

    def show_master_list_memberships(self):
        self.clear_screen()

        members_data = []
        with open(MEMBERS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                members_data.append(row)

        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=10)

        headers = ["Member ID", "First Name", "Last Name", "Start Date", "End Date", "Membership Duration"]
        for col, header in enumerate(headers):
            ttk.Label(table_frame, text=header, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=5, pady=5)

        for i, member in enumerate(members_data, start=1):
            ttk.Label(table_frame, text=member["Member ID"]).grid(row=i, column=0, padx=5, pady=5)
            ttk.Label(table_frame, text=member["First Name"]).grid(row=i, column=1, padx=5, pady=5)
            ttk.Label(table_frame, text=member["Last Name"]).grid(row=i, column=2, padx=5, pady=5)
            ttk.Label(table_frame, text=member["Start Date"]).grid(row=i, column=3, padx=5, pady=5)
            ttk.Label(table_frame, text=member["End Date"]).grid(row=i, column=4, padx=5, pady=5)
            ttk.Label(table_frame, text=member["Membership Duration"]).grid(row=i, column=5, padx=5, pady=5)

        ttk.Button(self.root, text="Back to Report Menu", command=self.show_report_menu).pack(pady=10)

    def show_active_issues(self):
        self.clear_screen()
        messagebox.showinfo("Info", "Active Issues report is under development.")

    def show_overdue_returns(self):
        self.clear_screen()
        messagebox.showinfo("Info", "Overdue Returns report is under development.")

    def show_pending_issue_requests(self):
        self.clear_screen()
        messagebox.showinfo("Info", "Pending Issue Requests report is under development.")


   
    def show_transaction_menu(self):
        self.clear_screen()

        ttk.Label(self.root, text="Transaction Menu", font=("Arial", 18)).pack(pady=20)

        # Creating clickable buttons for each option in the transaction menu
        ttk.Button(self.root, text="Is Book Available?", command=self.check_book_availability).pack(pady=10)
        ttk.Button(self.root, text="Issue Book", command=self.issue_book).pack(pady=10)
        ttk.Button(self.root, text="Return Book", command=self.return_book).pack(pady=10)
        ttk.Button(self.root, text="Pay Fine", command=self.pay_fine).pack(pady=10)
        ttk.Button(self.root, text="Log Out", command=self.show_login_screen).pack(pady=10)

    def check_book_availability(self):
        self.clear_screen()

        # Label for Book Availability
        ttk.Label(self.root, text="Check Book Availability", font=("Arial", 18)).pack(pady=20)

        # Create a frame for drop-downs and buttons
        frame = ttk.Frame(self.root)
        frame.pack(pady=20)

        # Book Name Drop-down
        ttk.Label(frame, text="Enter Book Name:").grid(row=0, column=0, padx=5, pady=5)
        self.book_name_combo = ttk.Combobox(frame, state="readonly")
        self.book_name_combo.grid(row=0, column=1, padx=5, pady=5)

        # Author Drop-down
        ttk.Label(frame, text="Enter Author:").grid(row=1, column=0, padx=5, pady=5)
        self.author_combo = ttk.Combobox(frame, state="readonly")
        self.author_combo.grid(row=1, column=1, padx=5, pady=5)

        # Load available books and authors
        self.load_books_and_authors()

        # Search Button
        ttk.Button(frame, text="Search", command=self.search_book_availability).grid(row=2, column=0, columnspan=2, pady=10)

        # Back and Logout buttons
        ttk.Button(self.root, text="Back", command=self.show_transaction_menu).pack(pady=10)
        ttk.Button(self.root, text="Log Out", command=self.show_login_screen).pack(pady=10)

    def load_books_and_authors(self):
        books = set()
        authors = set()

        # Read book data from books.csv
        with open(BOOKS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                books.add(row["Title"])  # Add book titles to the book name drop-down
                authors.add(row["Author"])  # Add authors to the author drop-down

        # Populate drop-down menus
        self.book_name_combo["values"] = sorted(books)
        self.author_combo["values"] = sorted(authors)

    def search_book_availability(self):
        book_name = self.book_name_combo.get()
        author_name = self.author_combo.get()

        if not book_name or not author_name:
            messagebox.showerror("Error", "Please select both book name and author.")
            return

        # Check if the book is available
        is_available = False
        with open(BOOKS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Title"] == book_name and row["Author"] == author_name:
                    is_available = row["Available"] == "Yes"

        if is_available:
            messagebox.showinfo("Availability", f"The book '{book_name}' by {author_name} is available.")
        else:
            messagebox.showinfo("Availability", f"The book '{book_name}' by {author_name} is not available.")

    def issue_book(self):
        self.clear_screen()

        # Label for Book Issue
        ttk.Label(self.root, text="Book Issue", font=("Arial", 18)).pack(pady=20)

        # Create a frame for the input fields
        frame = ttk.Frame(self.root)
        frame.pack(pady=20)

        # Book Name Drop-down
        ttk.Label(frame, text="Enter Book Name:").grid(row=0, column=0, padx=5, pady=5)
        self.book_name_combo = ttk.Combobox(frame, state="readonly")
        self.book_name_combo.grid(row=0, column=1, padx=5, pady=5)

        # Author Text Box
        ttk.Label(frame, text="Enter Author:").grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = ttk.Entry(frame)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        # Load available books in the drop-down
        self.load_books_for_issue()

        # Issue Date Calendar
        ttk.Label(frame, text="Issue Date:").grid(row=2, column=0, padx=5, pady=5)
        self.issue_date = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.issue_date.grid(row=2, column=1, padx=5, pady=5)

        # Return Date Calendar
        ttk.Label(frame, text="Return Date:").grid(row=3, column=0, padx=5, pady=5)
        self.return_date = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.return_date.grid(row=3, column=1, padx=5, pady=5)

        # Remarks Text Area (Non-mandatory)
        ttk.Label(frame, text="Remarks:").grid(row=4, column=0, padx=5, pady=5)
        self.remarks_text = tk.Text(frame, height=4, width=30)
        self.remarks_text.grid(row=4, column=1, padx=5, pady=5)

        # Cancel and Confirm buttons
        ttk.Button(frame, text="Cancel", command=self.show_transaction_menu).grid(row=5, column=0, pady=10)
        ttk.Button(frame, text="Confirm", command=self.confirm_issue).grid(row=5, column=1, pady=10)

        # Logout Button
        ttk.Button(self.root, text="Log Out", command=self.show_login_screen).pack(pady=10)

    def load_books_for_issue(self):
        books = set()

        # Read books from books.csv
        with open(BOOKS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Available"] == "Yes":  # Only show available books
                    books.add(row["Title"])

        # Populate the Book Name drop-down with available books
        self.book_name_combo["values"] = sorted(books)

    def confirm_issue(self):
        book_name = self.book_name_combo.get()
        author = self.author_entry.get()
        issue_date = self.issue_date.get_date()
        return_date = self.return_date.get_date()
        remarks = self.remarks_text.get("1.0", "end-1c")

        if not book_name or not author or not issue_date or not return_date:
            messagebox.showerror("Error", "All fields except remarks are required.")
            return

        # Issue book functionality
        with open(TRANSACTIONS_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            # Writing the transaction details to the transactions.csv
            writer.writerow([self.generate_transaction_id(), book_name, author, issue_date, return_date, remarks])

        # Update book availability (mark as unavailable)
        self.update_book_availability(book_name)

        messagebox.showinfo("Success", f"Book '{book_name}' issued successfully!")

        # Return to the transaction menu after the successful issue
        self.show_transaction_menu()

    def update_book_availability(self, book_name):
        # Read and update book availability
        books = []

        with open(BOOKS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Title"] == book_name:
                    row["Available"] = "No"  # Mark book as unavailable
                books.append(row)

        # Save the updated book data back to the CSV
        with open(BOOKS_FILE, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Book ID", "Title", "Author", "Available"])
            writer.writeheader()
            writer.writerows(books)

    def generate_transaction_id(self):
        # Generate a unique transaction ID (this could be an incremental number or a UUID)
        with open(TRANSACTIONS_FILE, mode="r") as f:
            reader = csv.reader(f)
            rows = list(reader)
            transaction_id = len(rows) + 1  # Use the row count as a transaction ID
        return transaction_id

    def return_book(self):
        self.clear_screen()

        # Label for Book Return
        ttk.Label(self.root, text="Return Book", font=("Arial", 18)).pack(pady=20)

        # Create a frame for the input fields
        frame = ttk.Frame(self.root)
        frame.pack(pady=20)

        # Book Name Drop-down
        ttk.Label(frame, text="Enter Book Name:").grid(row=0, column=0, padx=5, pady=5)
        self.book_name_combo = ttk.Combobox(frame, state="readonly")
        self.book_name_combo.grid(row=0, column=1, padx=5, pady=5)

        # Load issued books into the drop-down
        self.load_issued_books()

        # Author Text Area (Non-mandatory)
        ttk.Label(frame, text="Enter Author:").grid(row=1, column=0, padx=5, pady=5)
        self.author_text = tk.Text(frame, height=4, width=30, wrap="word")
        self.author_text.grid(row=1, column=1, padx=5, pady=5)
        self.author_text.config(state="disabled")  # Make it non-editable

        # Serial No Drop-down (Mandatory)
        ttk.Label(frame, text="Serial No:").grid(row=2, column=0, padx=5, pady=5)
        self.serial_no_combo = ttk.Combobox(frame, state="readonly")
        self.serial_no_combo.grid(row=2, column=1, padx=5, pady=5)

        # Issue Date Text Box (Non-mandatory)
        ttk.Label(frame, text="Issue Date:").grid(row=3, column=0, padx=5, pady=5)
        self.issue_date_entry = ttk.Entry(frame)
        self.issue_date_entry.grid(row=3, column=1, padx=5, pady=5)

        # Return Date Calendar
        ttk.Label(frame, text="Return Date:").grid(row=4, column=0, padx=5, pady=5)
        self.return_date = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.return_date.grid(row=4, column=1, padx=5, pady=5)

        # Remarks Text Area (Non-mandatory)
        ttk.Label(frame, text="Remarks:").grid(row=5, column=0, padx=5, pady=5)
        self.remarks_text = tk.Text(frame, height=4, width=30)
        self.remarks_text.grid(row=5, column=1, padx=5, pady=5)

        # Cancel and Confirm buttons
        ttk.Button(frame, text="Cancel", command=self.show_transaction_menu).grid(row=6, column=0, pady=10)
        ttk.Button(frame, text="Confirm", command=self.confirm_return).grid(row=6, column=1, pady=10)

        # Logout Button
        ttk.Button(self.root, text="Log Out", command=self.show_login_screen).pack(pady=10)

    def load_issued_books(self):
        # Load issued books into the drop-down
        issued_books = set()

        with open(TRANSACTIONS_FILE, mode="r") as f:
            reader = csv.reader(f)
            for row in reader:
                issued_books.add((row[1], row[2], row[0]))  # (Book Name, Author, Transaction ID)

        books = sorted(set([book[0] for book in issued_books]))
        self.book_name_combo["values"] = books

    def load_serial_numbers(self, book_name):
        # Load the serial numbers for the selected book name
        serial_numbers = []

        with open(TRANSACTIONS_FILE, mode="r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] == book_name:  # Filter by selected book name
                    serial_numbers.append(row[0])  # Transaction ID as Serial No

        self.serial_no_combo["values"] = serial_numbers

    def confirm_return(self):
        book_name = self.book_name_combo.get()
        serial_no = self.serial_no_combo.get()
        return_date = self.return_date.get_date()
        remarks = self.remarks_text.get("1.0", "end-1c")

        if not book_name or not serial_no or not return_date:
            messagebox.showerror("Error", "Book Name, Serial No, and Return Date are mandatory.")
            return

        # Find the issue details for the selected serial number
        issue_date = ""
        author = ""
        with open(TRANSACTIONS_FILE, mode="r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == serial_no:  # Match by Serial No (Transaction ID)
                    issue_date = row[3]
                    author = row[2]

        # Update the book availability (mark as available)
        self.update_book_availability(book_name)

        # Update the return transaction in the transactions.csv
        with open(TRANSACTIONS_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([serial_no, book_name, author, issue_date, return_date, remarks])

        messagebox.showinfo("Success", f"Book '{book_name}' returned successfully!")

        # Return to the transaction menu after the successful return
        self.show_transaction_menu()

    def update_book_availability(self, book_name):
        # Read and update book availability
        books = []

        with open(BOOKS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Title"] == book_name:
                    row["Available"] = "Yes"  # Mark book as available
                books.append(row)

        # Save the updated book data back to the CSV
        with open(BOOKS_FILE, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Book ID", "Title", "Author", "Available"])
            writer.writeheader()
            writer.writerows(books)

    def pay_fine(self):
        self.clear_screen()

        # Label for Pay Fine
        ttk.Label(self.root, text="Pay Fine", font=("Arial", 18)).pack(pady=20)

        # Create a frame for the input fields
        frame = ttk.Frame(self.root)
        frame.pack(pady=20)

        # Book Name Text Box
        ttk.Label(frame, text="Enter Book Name:").grid(row=0, column=0, padx=5, pady=5)
        self.book_name_entry = ttk.Entry(frame)
        self.book_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Author Text Box
        ttk.Label(frame, text="Enter Author:").grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = ttk.Entry(frame)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        # Serial No Text Box
        ttk.Label(frame, text="Enter Serial No:").grid(row=2, column=0, padx=5, pady=5)
        self.serial_no_entry = ttk.Entry(frame)
        self.serial_no_entry.grid(row=2, column=1, padx=5, pady=5)

        # Issue Date Calendar
        ttk.Label(frame, text="Issue Date:").grid(row=3, column=0, padx=5, pady=5)
        self.issue_date = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.issue_date.grid(row=3, column=1, padx=5, pady=5)

        # Return Date Calendar
        ttk.Label(frame, text="Return Date:").grid(row=4, column=0, padx=5, pady=5)
        self.return_date = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.return_date.grid(row=4, column=1, padx=5, pady=5)

        # Actual Return Date Calendar
        ttk.Label(frame, text="Actual Return Date:").grid(row=5, column=0, padx=5, pady=5)
        self.actual_return_date = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.actual_return_date.grid(row=5, column=1, padx=5, pady=5)

        # Fine Calculated Text Box (Default 0)
        ttk.Label(frame, text="Fine Calculated:").grid(row=6, column=0, padx=5, pady=5)
        self.fine_calculated_entry = ttk.Entry(frame)
        self.fine_calculated_entry.grid(row=6, column=1, padx=5, pady=5)
        self.fine_calculated_entry.insert(0, "0")  # Default value is 0

        # Fine Paid Checkbox (Default unchecked)
        ttk.Label(frame, text="Fine Paid:").grid(row=7, column=0, padx=5, pady=5)
        self.fine_paid_var = tk.BooleanVar(value=False)
        self.fine_paid_checkbox = ttk.Checkbutton(frame, variable=self.fine_paid_var)
        self.fine_paid_checkbox.grid(row=7, column=1, padx=5, pady=5)

        # Remarks Text Area (Non-mandatory)
        ttk.Label(frame, text="Remarks:").grid(row=8, column=0, padx=5, pady=5)
        self.remarks_text = tk.Text(frame, height=4, width=30)
        self.remarks_text.grid(row=8, column=1, padx=5, pady=5)

        # Cancel and Confirm buttons
        ttk.Button(frame, text="Cancel", command=self.show_transaction_menu).grid(row=9, column=0, pady=10)
        ttk.Button(frame, text="Confirm", command=self.confirm_fine_payment).grid(row=9, column=1, pady=10)

        # Logout Button
        ttk.Button(self.root, text="Log Out", command=self.show_login_screen).pack(pady=10)

    def confirm_fine_payment(self):
        # Get data from inputs
        book_name = self.book_name_entry.get()
        author = self.author_entry.get()
        serial_no = self.serial_no_entry.get()
        issue_date = self.issue_date.get_date()
        return_date = self.return_date.get_date()
        actual_return_date = self.actual_return_date.get_date()
        fine_calculated = self.fine_calculated_entry.get()
        fine_paid = self.fine_paid_var.get()
        remarks = self.remarks_text.get("1.0", "end-1c")

        # Validate mandatory fields
        if not book_name or not author or not serial_no or not issue_date or not return_date or not actual_return_date:
            messagebox.showerror("Error", "All fields except Remarks are mandatory.")
            return

        try:
            fine_calculated = float(fine_calculated)
        except ValueError:
            messagebox.showerror("Error", "Invalid value for Fine Calculated.")
            return

        # Handle the fine payment status
        fine_status = "Paid" if fine_paid else "Unpaid"

        # Log the fine payment details
        with open(FINE_TRANSACTIONS_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([serial_no, book_name, author, issue_date, return_date, actual_return_date, fine_calculated, fine_status, remarks])

        # Display success message
        messagebox.showinfo("Success", f"Fine for book '{book_name}' processed successfully!")

        # Return to transaction menu after the successful fine payment
        self.show_transaction_menu()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

      

    def show_add_membership(self):
        self.clear_screen()
        ttk.Label(self.root, text="Add Membership", font=("Arial", 18)).pack(pady=20)
        # Fields for adding membership (not included in this snippet for brevity)
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
        first_name_entry = ttk.Entry(form_frame)
        first_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
        last_name_entry = ttk.Entry(form_frame)
        last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Contact Name:").grid(row=2, column=0, padx=5, pady=5)
        contact_name_entry = ttk.Entry(form_frame)
        contact_name_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Contact Address:").grid(row=3, column=0, padx=5, pady=5)
        contact_address_entry = ttk.Entry(form_frame)
        contact_address_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Aadhaar Card No:").grid(row=4, column=0, padx=5, pady=5)
        aadhaar_entry = ttk.Entry(form_frame)
        aadhaar_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Start Date:").grid(row=5, column=0, padx=5, pady=5)
        start_date_entry = DateEntry(form_frame, date_pattern='y-mm-dd')
        start_date_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="End Date:").grid(row=6, column=0, padx=5, pady=5)
        end_date_entry = DateEntry(form_frame, date_pattern='y-mm-dd')
        end_date_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Membership Duration:").grid(row=7, column=0, padx=5, pady=5)
        membership_var = tk.StringVar()
        ttk.Radiobutton(form_frame, text="Six Months", variable=membership_var, value="6 Months").grid(row=7, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="One Year", variable=membership_var, value="1 Year").grid(row=8, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="Two Years", variable=membership_var, value="2 Years").grid(row=9, column=1, padx=5, pady=5, sticky="w")

        def confirm_membership():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            contact_name = contact_name_entry.get()
            contact_address = contact_address_entry.get()
            aadhaar = aadhaar_entry.get()
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()
            membership_duration = membership_var.get()

            if not all([first_name, last_name, contact_name, contact_address, aadhaar, start_date, end_date, membership_duration]):
                messagebox.showerror("Error", "All fields are required")
                return

            with open(MEMBERS_FILE, mode="a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["M" + str(sum(1 for _ in open(MEMBERS_FILE)) + 1), first_name, last_name, contact_name, contact_address, aadhaar, start_date, end_date, membership_duration])

            messagebox.showinfo("Success", "Membership added successfully")
            self.show_maintenance_menu()

        ttk.Button(form_frame, text="Confirm", command=confirm_membership).grid(row=10, column=0, pady=10)
        ttk.Button(form_frame, text="Cancel", command=self.show_maintenance_menu).grid(row=10, column=1, pady=10)

        

    def show_update_membership(self):
        self.clear_screen()
        ttk.Label(self.root, text="Update Membership", font=("Arial", 18)).pack(pady=20)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Membership Number :").grid(row=0, column=0, padx=5, pady=5)
        membership_id_entry = ttk.Entry(form_frame)
        membership_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Start Date:").grid(row=1, column=0, padx=5, pady=5)
        start_date_entry = DateEntry(form_frame, date_pattern='y-mm-dd')
        start_date_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="End Date:").grid(row=2, column=0, padx=5, pady=5)
        end_date_entry = DateEntry(form_frame, date_pattern='y-mm-dd')
        end_date_entry.grid(row=2, column=1, padx=5, pady=5)

        membership_duration_var = tk.StringVar()
        ttk.Radiobutton(form_frame, text="Six Months", variable=membership_duration_var, value="6 Months").grid(row=3, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="One Year", variable=membership_duration_var, value="1 Year").grid(row=4, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="Two Years", variable=membership_duration_var, value="2 Years").grid(row=5, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(form_frame, text="Membership Type :").grid(row=6, column=0, padx=5, pady=5)

        membership_type_var = tk.StringVar()
        ttk.Radiobutton(form_frame, text="Book", variable=membership_type_var, value="Book").grid(row=7, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="Movie", variable=membership_type_var, value="Movie").grid(row=8, column=1, padx=5, pady=5, sticky="w")

        def confirm_update_membership():
            membership_id = membership_id_entry.get()
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()
            membership_duration = membership_duration_var.get()
            membership_type = membership_type_var.get()

            if not all([membership_id, start_date, end_date, membership_duration, membership_type]):
                messagebox.showerror("Error", "All fields are required")
                return

            # Implement membership update logic here
            # For this example, we're simply printing the data
            messagebox.showinfo("Success", f"Membership {membership_id} updated successfully")

            self.show_maintenance_menu()

        ttk.Button(form_frame, text="Confirm", command=confirm_update_membership).grid(row=9, column=0, pady=10)
        ttk.Button(form_frame, text="Cancel", command=self.show_maintenance_menu).grid(row=9, column=1, pady=10)


#######################################################################################        

    def show_add_books(self):
        self.clear_screen()
        ttk.Label(self.root, text="Add Book/Movie", font=("Arial", 18)).pack(pady=20)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Book/Movie Name:").grid(row=0, column=0, padx=5, pady=5)
        book_movie_name_entry = ttk.Entry(form_frame)
        book_movie_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Quantity/Copies:").grid(row=1, column=0, padx=5, pady=5)
        quantity_entry = ttk.Entry(form_frame)
        quantity_entry.insert(0, "1")  # Default to 1
        quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Date of Procurement:").grid(row=2, column=0, padx=5, pady=5)
        procurement_date_entry = DateEntry(form_frame, date_pattern='y-mm-dd')
        procurement_date_entry.grid(row=2, column=1, padx=5, pady=5)

        type_var = tk.StringVar()
        ttk.Radiobutton(form_frame, text="Book", variable=type_var, value="Book").grid(row=3, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="Movie", variable=type_var, value="Movie").grid(row=4, column=1, padx=5, pady=5, sticky="w")

        def confirm_add_book_movie():
            name = book_movie_name_entry.get()
            quantity = quantity_entry.get()
            procurement_date = procurement_date_entry.get()
            type_value = type_var.get()

            if not all([name, quantity, procurement_date, type_value]):
                messagebox.showerror("Error", "All fields are required")
                return

            with open(BOOKS_FILE, mode="a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([str(sum(1 for _ in open(BOOKS_FILE)) + 1), name, type_value, quantity])

            messagebox.showinfo("Success", "Book/Movie added successfully")
            self.show_maintenance_menu()

        ttk.Button(form_frame, text="Confirm", command=confirm_add_book_movie).grid(row=5, column=0, pady=10)
        ttk.Button(form_frame, text="Cancel", command=self.show_maintenance_menu).grid(row=5, column=1, pady=10)




#######################################################################################        

    def show_update_books(self):
        self.clear_screen()

        ttk.Label(self.root, text="Update Books/Movies", font=("Arial", 18)).pack(pady=20)

        # Frame for the form
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

       

        # Radio buttons for Book or Movie
        media_type_var = tk.StringVar()
        ttk.Radiobutton(form_frame, text="Book", variable=media_type_var, value="Book").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="Movie", variable=media_type_var, value="Movie").grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Dropdown for Book/Movie Name
        ttk.Label(form_frame, text="Book/Movie Name:").grid(row=3, column=0, padx=5, pady=5)
        media_name_combobox = ttk.Combobox(form_frame, state="readonly")
        media_name_combobox.grid(row=3, column=1, padx=5, pady=5)

        # Populate media_name_combobox with data from CSV (Books/Movies)
        with open(BOOKS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            media_names = [row["Title"] for row in reader]
        media_name_combobox["values"] = media_names

        # Status dropdown (for Book or Movie)
        ttk.Label(form_frame, text="Status:").grid(row=4, column=0, padx=5, pady=5)
        status_combobox = ttk.Combobox(form_frame, state="readonly", values=["Available", "Checked Out", "Damaged"])
        status_combobox.grid(row=4, column=1, padx=5, pady=5)

        # Date of Procurement calendar
        ttk.Label(form_frame, text="Date of Procurement:").grid(row=5, column=0, padx=5, pady=5)
        procurement_date_entry = DateEntry(form_frame, date_pattern='y-mm-dd')
        procurement_date_entry.grid(row=5, column=1, padx=5, pady=5)

        # Submit button
        def confirm_update_book():
            media_type = media_type_var.get()
            media_name = media_name_combobox.get()
            status = status_combobox.get()
            procurement_date = procurement_date_entry.get()

            if not all([media_type, media_name, status, procurement_date]):
                messagebox.showerror("Error", "All fields are required")
                return

            # Update the relevant CSV file (Books or Movies)
            file = BOOKS_FILE if media_type == "Book" else MOVIES_FILE
            updated = False

            # Update logic
            temp_rows = []
            with open(file, mode="r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["Title"] == media_name:
                        row["Status"] = status
                        row["Procurement Date"] = procurement_date
                        updated = True
                    temp_rows.append(row)

            # If updated, write changes back to the file
            if updated:
                with open(file, mode="w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=["Title", "Author", "Status", "Procurement Date"])
                    writer.writeheader()
                    writer.writerows(temp_rows)

                messagebox.showinfo("Success", f"{media_type} {media_name} updated successfully")
                self.show_maintenance_menu()  # Go back to Maintenance Menu
            else:
                messagebox.showerror("Error", f"{media_name} not found")

        ttk.Button(form_frame, text="Confirm", command=confirm_update_book).grid(row=6, column=0, pady=10)
        ttk.Button(form_frame, text="Cancel", command=self.show_maintenance_menu).grid(row=6, column=1, pady=10)


 
##########################################################################################################


    def show_add_user(self):
        self.clear_screen()

        ttk.Label(self.root, text="User Management", font=("Arial", 18)).pack(pady=20)

        # Frame for the form
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        # Radio buttons for New User or Existing User
        user_type_var = tk.StringVar()
        ttk.Radiobutton(form_frame, text="New User", variable=user_type_var, value="New User").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="Existing User", variable=user_type_var, value="Existing User").grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Name entry field
        ttk.Label(form_frame, text="Name:").grid(row=3, column=0, padx=5, pady=5)
        user_name_entry = ttk.Entry(form_frame)
        user_name_entry.grid(row=3, column=1, padx=5, pady=5)

        # Admin checkbox (for New or Existing User)
        ttk.Label(form_frame, text="Admin:").grid(row=4, column=0, padx=5, pady=5)
        admin_checkbox = ttk.Checkbutton(form_frame)
        admin_checkbox.grid(row=4, column=1, padx=5, pady=5)

        # Active checkbox (for New or Existing User)
        ttk.Label(form_frame, text="Active:").grid(row=5, column=0, padx=5, pady=5)
        active_checkbox = ttk.Checkbutton(form_frame)
        active_checkbox.grid(row=5, column=1, padx=5, pady=5)

        # Submit button
        def confirm_add_user():
            # Get values from the form
            user_type = user_type_var.get()
            user_name = user_name_entry.get()
            is_admin = admin_checkbox.instate(["selected"])
            is_active = active_checkbox.instate(["selected"])

            # Debug: Print the values for verification
            print(f"User Type: {user_type}")
            print(f"User Name: {user_name}")
            print(f"Admin: {is_admin}")
            print(f"Active: {is_active}")

            # Validate fields
            if not user_name:
                messagebox.showerror("Error", "Name field is required")
                return

            # Logic for adding new user or updating existing user
            if user_type == "New User":
                # Add new user logic
                self.add_new_user(user_name, is_admin, is_active)
            elif user_type == "Existing User":
                # Update existing user logic
                self.update_existing_user(user_name, is_admin, is_active)

        def add_new_user(user_name, is_admin, is_active):
            # Example logic for adding a new user
            with open(USERS_FILE, mode="a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([user_name, "Password", "Email", "Phone", "Date", "Admin" if is_admin else "User", "Active" if is_active else "Inactive"])

            messagebox.showinfo("Success", f"New user {user_name} added successfully")
            self.show_maintenance_menu()  # Go back to Maintenance Menu

        def update_existing_user(user_name, is_admin, is_active):
            # Update the user data in the file
            updated = False
            temp_rows = []
            with open(USERS_FILE, mode="r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == user_name:
                        row[5] = "Admin" if is_admin else "User"
                        row[6] = "Active" if is_active else "Inactive"
                        updated = True
                    temp_rows.append(row)

            if updated:
                with open(USERS_FILE, mode="w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerows(temp_rows)
                messagebox.showinfo("Success", f"User {user_name} updated successfully")
            else:
                messagebox.showerror("Error", f"User {user_name} not found")

            self.show_maintenance_menu()  # Go back to Maintenance Menu

        # Ensure confirm button calls confirm_add_user() correctly
        confirm_button = ttk.Button(form_frame, text="Confirm", command=confirm_add_user)
        confirm_button.grid(row=6, column=0, pady=10)

        cancel_button = ttk.Button(form_frame, text="Cancel", command=self.show_maintenance_menu)
        cancel_button.grid(row=6, column=1, pady=10)

    def home_button_action(self):
        if self.current_role == "Admin":
            self.show_admin_homepage()
        else:
            self.show_user_homepage()

########################################################################################################

    
    def show_update_user(self):
        self.clear_screen()

        ttk.Label(self.root, text="User Management", font=("Arial", 18)).pack(pady=20)

        # Frame for the form
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        # Radio buttons for New User or Existing User
        user_type_var = tk.StringVar(value="New User")
        ttk.Radiobutton(form_frame, text="New User", variable=user_type_var, value="New User").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="Existing User", variable=user_type_var, value="Existing User").grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Name entry field
        ttk.Label(form_frame, text="Name:").grid(row=3, column=0, padx=5, pady=5)
        user_name_entry = ttk.Entry(form_frame)
        user_name_entry.grid(row=3, column=1, padx=5, pady=5)

        # Admin checkbox (for New or Existing User)
        ttk.Label(form_frame, text="Admin:").grid(row=4, column=0, padx=5, pady=5)
        admin_checkbox = ttk.Checkbutton(form_frame)
        admin_checkbox.grid(row=4, column=1, padx=5, pady=5)

        # Active checkbox (for New or Existing User)
        ttk.Label(form_frame, text="Active:").grid(row=5, column=0, padx=5, pady=5)
        active_checkbox = ttk.Checkbutton(form_frame)
        active_checkbox.grid(row=5, column=1, padx=5, pady=5)

        # Submit button
        def confirm_update_user():
            # Get values from the form
            user_type = user_type_var.get()
            user_name = user_name_entry.get()
            is_admin = admin_checkbox.instate(["selected"])
            is_active = active_checkbox.instate(["selected"])

            # Validate fields
            if not user_name:
                messagebox.showerror("Error", "Name field is required")
                return

            # Logic for adding new user or updating existing user
            if user_type == "New User":
                # Add new user logic
                self.add_new_user(user_name, is_admin, is_active)
            elif user_type == "Existing User":
                # Update existing user logic
                self.update_existing_user(user_name, is_admin, is_active)

        def add_new_user(user_name, is_admin, is_active):
            # Example logic for adding a new user
            with open('users.csv', mode="a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([user_name, "Password", "Email", "Phone", "Date", "Admin" if is_admin else "User", "Active" if is_active else "Inactive"])

            messagebox.showinfo("Success", f"New user {user_name} added successfully")
            self.show_maintenance_menu()  # Go back to Maintenance Menu

        def update_existing_user(user_name, is_admin, is_active):
            # Update the user data in the file
            updated = False
            temp_rows = []
            with open('users.csv', mode="r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == user_name:
                        row[5] = "Admin" if is_admin else "User"
                        row[6] = "Active" if is_active else "Inactive"
                        updated = True
                    temp_rows.append(row)

            if updated:
                with open('users.csv', mode="w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerows(temp_rows)
                messagebox.showinfo("Success", f"User {user_name} updated successfully")
            else:
                messagebox.showerror("Error", f"User {user_name} not found")

            self.show_maintenance_menu()  # Go back to Maintenance Menu

        confirm_button = ttk.Button(form_frame, text="Confirm", command=confirm_update_user)
        confirm_button.grid(row=6, column=0, pady=10)

        cancel_button = ttk.Button(form_frame, text="Cancel", command=self.show_maintenance_menu)
        cancel_button.grid(row=6, column=1, pady=10)


    

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Initialize files and add sample user data
initialize_files()
if os.stat(USERS_FILE).st_size == 0:  # Add sample users if the file is empty
    with open(USERS_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["admin", "admin123", "Admin"])
        writer.writerow(["user", "user123", "User"])

# Run the application
root = tk.Tk()
app = LibraryApp(root)
root.mainloop()



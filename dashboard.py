import tkinter as tk
from tkinter import ttk, messagebox
from database import add_student, get_all_students, delete_student, add_attendance, add_fee, add_notice, get_notices
from config import APP_TITLE
from style import apply_professional_theme


class DashboardWindow(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title(f"{APP_TITLE} - Dashboard")
        self.geometry("980x640")
        self.resizable(False, False)
        apply_professional_theme(self)
        self._build_ui()
        self.refresh_students()
        self.refresh_notices()

    def _build_ui(self):
        header = ttk.Frame(self, style="Card.TFrame", padding=18)
        header.pack(fill="x", padx=18, pady=(18, 10))
        ttk.Label(header, text=f"Welcome, {self.username}", style="Header.TLabel").pack(anchor="w")
        ttk.Label(header, text="Manage students, attendance, fees, and notices from one place.", style="Body.TLabel").pack(anchor="w", pady=(4, 0))

        summary = ttk.Frame(self, style="Panel.TFrame", padding=10)
        summary.pack(fill="x", padx=18, pady=(0, 10))
        ttk.Label(summary, text="Quick overview", style="Header.TLabel").pack(anchor="w")
        ttk.Label(summary, text="Add students, keep records updated, and publish notices instantly.", style="Body.TLabel").pack(anchor="w", pady=(4, 0))

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 18))

        student_frame = ttk.Frame(notebook, padding=12)
        attendance_frame = ttk.Frame(notebook, padding=12)
        fees_frame = ttk.Frame(notebook, padding=12)
        notices_frame = ttk.Frame(notebook, padding=12)

        notebook.add(student_frame, text="Students")
        notebook.add(attendance_frame, text="Attendance")
        notebook.add(fees_frame, text="Fees")
        notebook.add(notices_frame, text="Notices")

        self._build_student_tab(student_frame)
        self._build_attendance_tab(attendance_frame)
        self._build_fees_tab(fees_frame)
        self._build_notices_tab(notices_frame)

    def _build_student_tab(self, parent):
        form = ttk.Frame(parent, style="Panel.TFrame", padding=12)
        form.grid(row=0, column=0, sticky="n", padx=(0, 18), pady=(0, 10))

        ttk.Label(form, text="Add Student", style="Header.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
        ttk.Label(form, text="Name").grid(row=1, column=0, sticky="w", pady=3)
        self.name_entry = ttk.Entry(form, width=28)
        self.name_entry.grid(row=1, column=1, pady=3)
        ttk.Label(form, text="Class").grid(row=2, column=0, sticky="w", pady=3)
        self.class_entry = ttk.Entry(form, width=28)
        self.class_entry.grid(row=2, column=1, pady=3)
        ttk.Label(form, text="Course").grid(row=3, column=0, sticky="w", pady=3)
        self.course_entry = ttk.Entry(form, width=28)
        self.course_entry.grid(row=3, column=1, pady=3)
        ttk.Label(form, text="Phone").grid(row=4, column=0, sticky="w", pady=3)
        self.phone_entry = ttk.Entry(form, width=28)
        self.phone_entry.grid(row=4, column=1, pady=3)
        ttk.Button(form, text="Add Student", style="Accent.TButton", command=self.add_student).grid(row=5, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        tree_frame = ttk.Frame(parent, style="Panel.TFrame", padding=8)
        tree_frame.grid(row=0, column=1, sticky="nsew")
        self.student_tree = ttk.Treeview(tree_frame, columns=("id", "name", "class", "course", "phone"), show="headings", height=12)
        self.student_tree.heading("id", text="ID")
        self.student_tree.heading("name", text="Name")
        self.student_tree.heading("class", text="Class")
        self.student_tree.heading("course", text="Course")
        self.student_tree.heading("phone", text="Phone")
        self.student_tree.column("id", width=50, anchor="center")
        self.student_tree.column("name", width=140)
        self.student_tree.column("class", width=90)
        self.student_tree.column("course", width=120)
        self.student_tree.column("phone", width=120)
        self.student_tree.grid(row=0, column=0, sticky="nsew")
        ttk.Button(tree_frame, text="Delete Selected", style="Secondary.TButton", command=self.delete_selected_student).grid(row=1, column=0, sticky="w", pady=(8, 0))

    def _build_attendance_tab(self, parent):
        card = ttk.Frame(parent, style="Panel.TFrame", padding=16)
        card.pack(fill="x", padx=8, pady=8)
        ttk.Label(card, text="Mark Attendance", style="Header.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(card, text="Student ID").pack(anchor="w")
        self.attendance_student_id = ttk.Entry(card, width=30)
        self.attendance_student_id.pack(fill="x", pady=(4, 8))
        ttk.Label(card, text="Date (YYYY-MM-DD)").pack(anchor="w")
        self.attendance_date = ttk.Entry(card, width=30)
        self.attendance_date.pack(fill="x", pady=(4, 8))
        ttk.Label(card, text="Status (Present/Absent)").pack(anchor="w")
        self.attendance_status = ttk.Entry(card, width=30)
        self.attendance_status.pack(fill="x", pady=(4, 12))
        ttk.Button(card, text="Save Attendance", style="Accent.TButton", command=self.save_attendance).pack(fill="x")

    def _build_fees_tab(self, parent):
        card = ttk.Frame(parent, style="Panel.TFrame", padding=16)
        card.pack(fill="x", padx=8, pady=8)
        ttk.Label(card, text="Fee Entry", style="Header.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(card, text="Student ID").pack(anchor="w")
        self.fee_student_id = ttk.Entry(card, width=30)
        self.fee_student_id.pack(fill="x", pady=(4, 8))
        ttk.Label(card, text="Amount").pack(anchor="w")
        self.fee_amount = ttk.Entry(card, width=30)
        self.fee_amount.pack(fill="x", pady=(4, 8))
        ttk.Label(card, text="Paid On").pack(anchor="w")
        self.fee_date = ttk.Entry(card, width=30)
        self.fee_date.pack(fill="x", pady=(4, 12))
        ttk.Button(card, text="Save Fee", style="Accent.TButton", command=self.save_fee).pack(fill="x")

    def _build_notices_tab(self, parent):
        card = ttk.Frame(parent, style="Panel.TFrame", padding=16)
        card.pack(fill="x", padx=8, pady=8)
        ttk.Label(card, text="Publish Notice", style="Header.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(card, text="Title").pack(anchor="w")
        self.notice_title = ttk.Entry(card, width=40)
        self.notice_title.pack(fill="x", pady=(4, 8))
        ttk.Label(card, text="Message").pack(anchor="w")
        self.notice_message = ttk.Entry(card, width=40)
        self.notice_message.pack(fill="x", pady=(4, 12))
        ttk.Button(card, text="Publish Notice", style="Accent.TButton", command=self.publish_notice).pack(fill="x")
        self.notice_list = tk.Listbox(card, height=8, width=70, bg="#ffffff", bd=1, relief="solid")
        self.notice_list.pack(pady=(12, 0), fill="x")

    def add_student(self):
        name = self.name_entry.get().strip()
        class_name = self.class_entry.get().strip()
        course = self.course_entry.get().strip()
        phone = self.phone_entry.get().strip()
        if not all([name, class_name, course, phone]):
            messagebox.showerror("Error", "All student fields are required")
            return
        add_student(name, class_name, course, phone)
        self.refresh_students()
        messagebox.showinfo("Success", "Student added successfully")

    def save_attendance(self):
        try:
            student_id = int(self.attendance_student_id.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid student ID")
            return
        add_attendance(student_id, self.attendance_date.get(), self.attendance_status.get())
        messagebox.showinfo("Success", "Attendance recorded")

    def save_fee(self):
        try:
            student_id = int(self.fee_student_id.get())
            amount = float(self.fee_amount.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid fee details")
            return
        add_fee(student_id, amount, self.fee_date.get())
        messagebox.showinfo("Success", "Fee recorded")

    def publish_notice(self):
        title = self.notice_title.get().strip()
        message = self.notice_message.get().strip()
        if not title or not message:
            messagebox.showerror("Error", "Title and message are required")
            return
        add_notice(title, message)
        self.refresh_notices()
        messagebox.showinfo("Success", "Notice published")

    def refresh_students(self):
        for row in self.student_tree.get_children():
            self.student_tree.delete(row)
        for student in get_all_students():
            self.student_tree.insert("", tk.END, values=student)

    def refresh_notices(self):
        self.notice_list.delete(0, tk.END)
        for title, message in get_notices():
            self.notice_list.insert(tk.END, f"{title}: {message}")

    def delete_selected_student(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a student first")
            return
        student_id = self.student_tree.item(selected[0], "values")[0]
        delete_student(student_id)
        self.refresh_students()
        messagebox.showinfo("Success", "Student deleted")

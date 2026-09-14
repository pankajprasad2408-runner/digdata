import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from config import APP_TITLE
from database import (
    add_attendance,
    add_fee,
    add_notice,
    add_performance,
    add_student,
    delete_student,
    get_all_students,
    get_attendance_records,
    get_dashboard_stats,
    get_fee_records,
    get_notices,
    get_performance,
    get_student_options,
)
from style import apply_professional_theme


class DashboardWindow(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title(f"{APP_TITLE} - Teacher Dashboard")
        self.geometry("1120x760")
        self.minsize(980, 680)
        apply_professional_theme(self)
        self.student_by_display = {}
        self._build_ui()
        self.refresh_all()

    def _build_ui(self):
        header = ttk.Frame(self, style="Card.TFrame", padding=(22, 18))
        header.pack(fill="x", padx=18, pady=(18, 12))
        left = ttk.Frame(header, style="Card.TFrame")
        left.pack(side="left", fill="x", expand=True)
        ttk.Label(left, text="Teacher workspace", style="Eyebrow.TLabel").pack(anchor="w")
        ttk.Label(left, text=f"Good to see you, {self.username}", style="Title.TLabel").pack(anchor="w", pady=(3, 2))
        ttk.Label(left, text="Track progress, payments, and classroom activity in one place.", style="SubTitle.TLabel").pack(anchor="w")
        ttk.Button(header, text="Refresh data", style="Secondary.TButton", command=self.refresh_all).pack(side="right", anchor="n")

        self.stats_frame = ttk.Frame(self, style="TFrame")
        self.stats_frame.pack(fill="x", padx=18, pady=(0, 12))
        self.stat_values = {}
        metrics = (("students", "Active students"), ("courses", "Courses"), ("attendance_rate", "Attendance rate"), ("fees", "Fees collected"), ("average_performance", "Average score"))
        for key, title in metrics:
            card = ttk.Frame(self.stats_frame, style="Metric.TFrame", padding=(14, 12))
            card.pack(side="left", fill="both", expand=True, padx=(0, 8))
            ttk.Label(card, text=title, style="MetricLabel.TLabel").pack(anchor="w")
            value = ttk.Label(card, text="0", style="MetricValue.TLabel")
            value.pack(anchor="w", pady=(5, 0))
            self.stat_values[key] = value

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        tabs = [("Students", self._build_students_tab), ("Attendance", self._build_attendance_tab), ("Fees", self._build_fees_tab), ("Performance", self._build_performance_tab), ("Notices", self._build_notices_tab)]
        for title, builder in tabs:
            tab = ttk.Frame(self.notebook, padding=14)
            self.notebook.add(tab, text=title)
            builder(tab)

    def _build_students_tab(self, parent):
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=1)
        form = ttk.Frame(parent, style="Panel.TFrame", padding=16)
        form.grid(row=0, column=0, sticky="ns", padx=(0, 14))
        ttk.Label(form, text="Register student", style="Section.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 12))
        self.name_entry = self._labeled_entry(form, "Full name", 1)
        self.class_entry = self._labeled_entry(form, "Class / batch", 3)
        self.course_entry = self._labeled_entry(form, "Course", 5)
        self.phone_entry = self._labeled_entry(form, "Phone", 7)
        ttk.Button(form, text="Add student", style="Accent.TButton", command=self.add_student).grid(row=9, column=0, sticky="ew", pady=(12, 0))

        table = ttk.Frame(parent, style="Panel.TFrame", padding=10)
        table.grid(row=0, column=1, sticky="nsew")
        table.columnconfigure(0, weight=1)
        table.rowconfigure(0, weight=1)
        self.student_tree = ttk.Treeview(table, columns=("id", "name", "class", "course", "phone"), show="headings")
        for column, heading, width in (("id", "ID", 50), ("name", "Name", 180), ("class", "Class / batch", 120), ("course", "Course", 160), ("phone", "Phone", 140)):
            self.student_tree.heading(column, text=heading)
            self.student_tree.column(column, width=width, anchor="center" if column == "id" else "w")
        self.student_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(table, orient="vertical", command=self.student_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.student_tree.configure(yscrollcommand=scrollbar.set)
        ttk.Button(table, text="Delete selected student", style="Secondary.TButton", command=self.delete_selected_student).grid(row=1, column=0, sticky="w", pady=(10, 0))

    def _build_attendance_tab(self, parent):
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=1)
        card = self._form_card(parent, "Record attendance", "Choose a student and record today's classroom status.")
        card.grid(row=0, column=0, sticky="ns", padx=(0, 14))
        self.attendance_student = self._student_picker(card, "Student", 2)
        self.attendance_date = self._labeled_entry(card, "Date (YYYY-MM-DD)", 4, date.today().isoformat())
        ttk.Label(card, text="Status").grid(row=6, column=0, sticky="w", pady=(10, 4))
        self.attendance_status = ttk.Combobox(card, values=("Present", "Absent", "Late"), state="readonly", width=28)
        self.attendance_status.set("Present")
        self.attendance_status.grid(row=7, column=0, sticky="ew")
        ttk.Button(card, text="Save attendance", style="Accent.TButton", command=self.save_attendance).grid(row=8, column=0, sticky="ew", pady=(16, 0))
        self.attendance_summary = ttk.Label(card, text="No attendance recorded yet", style="Body.TLabel", wraplength=300)
        self.attendance_summary.grid(row=9, column=0, sticky="w", pady=(18, 0))

        table = self._history_table(parent, ("id", "student", "date", "status"), (("id", "ID", 50), ("student", "Student", 190), ("date", "Date", 120), ("status", "Status", 100)))
        table.grid(row=0, column=1, sticky="nsew")
        self.attendance_tree = table.tree

    def _build_fees_tab(self, parent):
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=1)
        card = self._form_card(parent, "Record fee payment", "Keep a clear payment trail for every student.")
        card.grid(row=0, column=0, sticky="ns", padx=(0, 14))
        self.fee_student = self._student_picker(card, "Student", 2)
        self.fee_amount = self._labeled_entry(card, "Amount", 4)
        self.fee_date = self._labeled_entry(card, "Paid on (YYYY-MM-DD)", 6, date.today().isoformat())
        ttk.Button(card, text="Save payment", style="Accent.TButton", command=self.save_fee).grid(row=8, column=0, sticky="ew", pady=(16, 0))
        self.fee_summary = ttk.Label(card, text="No payments recorded yet", style="Body.TLabel", wraplength=300)
        self.fee_summary.grid(row=9, column=0, sticky="w", pady=(18, 0))

        table = self._history_table(parent, ("id", "student", "amount", "date"), (("id", "ID", 50), ("student", "Student", 190), ("amount", "Amount", 110), ("date", "Paid on", 120)))
        table.grid(row=0, column=1, sticky="nsew")
        self.fee_tree = table.tree

    def _build_performance_tab(self, parent):
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=1)
        form = self._form_card(parent, "Add assessment", "Record scores to monitor each learner's progress.")
        form.grid(row=0, column=0, sticky="ns", padx=(0, 14))
        self.performance_student = self._student_picker(form, "Student", 2)
        self.performance_subject = self._labeled_entry(form, "Subject", 4)
        self.performance_score = self._labeled_entry(form, "Score", 6)
        self.performance_max_score = self._labeled_entry(form, "Maximum score", 8, "100")
        self.performance_date = self._labeled_entry(form, "Assessed on", 10, date.today().isoformat())
        ttk.Button(form, text="Save assessment", style="Accent.TButton", command=self.save_performance).grid(row=12, column=0, sticky="ew", pady=(16, 0))

        table = ttk.Frame(parent, style="Panel.TFrame", padding=10)
        table.grid(row=0, column=1, sticky="nsew")
        table.columnconfigure(0, weight=1)
        table.rowconfigure(0, weight=1)
        self.performance_tree = ttk.Treeview(table, columns=("id", "student", "subject", "score", "max", "date"), show="headings")
        for column, heading, width in (("id", "ID", 45), ("student", "Student", 180), ("subject", "Subject", 130), ("score", "Score", 75), ("max", "Out of", 75), ("date", "Date", 110)):
            self.performance_tree.heading(column, text=heading)
            self.performance_tree.column(column, width=width, anchor="center" if column in ("id", "score", "max") else "w")
        self.performance_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(table, orient="vertical", command=self.performance_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.performance_tree.configure(yscrollcommand=scrollbar.set)
        self.performance_summary = ttk.Label(form, text="No assessments recorded yet", style="Body.TLabel", wraplength=300)
        self.performance_summary.grid(row=13, column=0, sticky="w", pady=(18, 0))

    def _build_notices_tab(self, parent):
        card = self._form_card(parent, "Publish notice", "Share important updates with the coaching center team.")
        card.pack(fill="both", expand=True)
        self.notice_title = self._labeled_entry(card, "Title", 2)
        self.notice_message = self._labeled_entry(card, "Message", 4)
        ttk.Button(card, text="Publish notice", style="Accent.TButton", command=self.publish_notice).grid(row=6, column=0, sticky="ew", pady=(16, 0))
        self.notice_list = tk.Listbox(card, height=12, bg="#ffffff", fg="#172033", bd=0, highlightthickness=1, highlightcolor="#cbd5e1", font=("Segoe UI", 10))
        self.notice_list.grid(row=7, column=0, sticky="ew", pady=(18, 0))

    def _form_card(self, parent, title, description):
        card = ttk.Frame(parent, style="Panel.TFrame", padding=20)
        card.grid_columnconfigure(0, weight=1)
        card.configure(width=360, height=500)
        ttk.Label(card, text=title, style="Section.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(card, text=description, style="Body.TLabel", wraplength=310).grid(row=1, column=0, sticky="w", pady=(4, 14))
        return card

    def _student_picker(self, parent, label, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=(8, 4))
        picker = ttk.Combobox(parent, state="readonly", width=30)
        picker.grid(row=row + 1, column=0, sticky="ew")
        return picker

    def _history_table(self, parent, columns, headings):
        table = ttk.Frame(parent, style="Panel.TFrame", padding=10)
        table.columnconfigure(0, weight=1)
        table.rowconfigure(0, weight=1)
        table.tree = ttk.Treeview(table, columns=columns, show="headings")
        for column, heading, width in headings:
            table.tree.heading(column, text=heading)
            table.tree.column(column, width=width, anchor="center" if column == "id" else "w")
        table.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(table, orient="vertical", command=table.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        table.tree.configure(yscrollcommand=scrollbar.set)
        return table

    def _labeled_entry(self, parent, label, row, value=""):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=(8, 4))
        entry = ttk.Entry(parent, width=30)
        entry.grid(row=row + 1, column=0, sticky="ew")
        if value:
            entry.insert(0, value)
        return entry

    def add_student(self):
        values = [entry.get().strip() for entry in (self.name_entry, self.class_entry, self.course_entry, self.phone_entry)]
        if not all(values):
            messagebox.showerror("Missing details", "Complete all student fields before saving.")
            return
        add_student(*values)
        self._clear_entries(self.name_entry, self.class_entry, self.course_entry, self.phone_entry)
        self.refresh_all()
        messagebox.showinfo("Student added", "The student is now in the register.")

    def save_attendance(self):
        student_id = self._selected_student_id(self.attendance_student)
        if student_id is None:
            messagebox.showerror("Select a student", "Choose a student before recording attendance.")
            return
        if not self.attendance_date.get().strip():
            messagebox.showerror("Missing date", "Enter the attendance date.")
            return
        add_attendance(student_id, self.attendance_date.get().strip(), self.attendance_status.get().strip())
        self.refresh_all()
        messagebox.showinfo("Attendance saved", "Attendance has been recorded.")

    def save_fee(self):
        student_id = self._selected_student_id(self.fee_student)
        if student_id is None:
            messagebox.showerror("Select a student", "Choose a student before recording a payment.")
            return
        try:
            amount = float(self.fee_amount.get().strip())
        except ValueError:
            messagebox.showerror("Invalid payment", "Enter a numeric student ID and amount.")
            return
        if amount <= 0 or not self.fee_date.get().strip():
            messagebox.showerror("Invalid payment", "Amount must be greater than zero and a date is required.")
            return
        add_fee(student_id, amount, self.fee_date.get().strip())
        self.refresh_all()
        messagebox.showinfo("Payment saved", "The fee payment has been recorded.")

    def save_performance(self):
        student_id = self._selected_student_id(self.performance_student)
        if student_id is None:
            messagebox.showerror("Select a student", "Choose a student before recording a score.")
            return
        try:
            score = float(self.performance_score.get().strip())
            max_score = float(self.performance_max_score.get().strip())
        except ValueError:
            messagebox.showerror("Invalid score", "Enter numeric student ID, score, and maximum score.")
            return
        subject = self.performance_subject.get().strip()
        assessed_on = self.performance_date.get().strip()
        if not subject or not assessed_on or max_score <= 0 or score < 0 or score > max_score:
            messagebox.showerror("Invalid score", "Check the subject, date, and score range.")
            return
        add_performance(student_id, subject, score, max_score, assessed_on)
        self.refresh_all()
        messagebox.showinfo("Assessment saved", "The performance record has been added.")

    def publish_notice(self):
        title = self.notice_title.get().strip()
        message = self.notice_message.get().strip()
        if not title or not message:
            messagebox.showerror("Missing notice", "Enter both a title and a message.")
            return
        add_notice(title, message)
        self.notice_title.delete(0, tk.END)
        self.notice_message.delete(0, tk.END)
        self.refresh_notices()
        messagebox.showinfo("Notice published", "The notice is now visible in the notice board.")

    def refresh_all(self):
        self.refresh_student_selectors()
        self.refresh_students()
        self.refresh_attendance()
        self.refresh_fees()
        self.refresh_performance()
        self.refresh_notices()
        stats = get_dashboard_stats()
        self.stat_values["students"].configure(text=str(stats["students"]))
        self.stat_values["courses"].configure(text=str(stats["courses"]))
        self.stat_values["attendance_rate"].configure(text=f"{stats['attendance_rate']:.1f}%")
        self.stat_values["fees"].configure(text=f"{stats['fees']:,.2f}")
        self.stat_values["average_performance"].configure(text=f"{stats['average_performance']:.1f}%")

    def refresh_student_selectors(self):
        self.student_by_display = {}
        values = []
        for student_id, name, class_name, course in get_student_options():
            display = f"{student_id} - {name} ({course})"
            self.student_by_display[display] = student_id
            values.append(display)
        for picker in (self.attendance_student, self.fee_student, self.performance_student):
            current = picker.get()
            picker["values"] = values
            if current in values:
                picker.set(current)
            elif values:
                picker.current(0)
            else:
                picker.set("")

    def refresh_attendance(self):
        records = get_attendance_records()
        for row in self.attendance_tree.get_children():
            self.attendance_tree.delete(row)
        for record in records:
            self.attendance_tree.insert("", tk.END, values=record)
        present = sum(record[3].lower() == "present" for record in records)
        rate = (present * 100 / len(records)) if records else 0
        self.attendance_summary.configure(text=f"{len(records)} records | {present} present | Overall rate: {rate:.1f}%")

    def refresh_fees(self):
        records = get_fee_records()
        for row in self.fee_tree.get_children():
            self.fee_tree.delete(row)
        for record in records:
            self.fee_tree.insert("", tk.END, values=(record[0], record[1], f"{record[2]:,.2f}", record[3]))
        total = sum(record[2] for record in records)
        self.fee_summary.configure(text=f"{len(records)} payments | Total collected: {total:,.2f}")

    def refresh_students(self):
        for row in self.student_tree.get_children():
            self.student_tree.delete(row)
        for student in get_all_students():
            self.student_tree.insert("", tk.END, values=student)

    def refresh_performance(self):
        records = get_performance()
        for row in self.performance_tree.get_children():
            self.performance_tree.delete(row)
        for performance in records:
            self.performance_tree.insert("", tk.END, values=performance)
        if records:
            average = sum((record[3] * 100 / record[4]) for record in records if record[4]) / len(records)
            self.performance_summary.configure(text=f"{len(records)} assessments | Overall average: {average:.1f}%")
        else:
            self.performance_summary.configure(text="No assessments recorded yet")

    def refresh_notices(self):
        self.notice_list.delete(0, tk.END)
        for title, message in get_notices():
            self.notice_list.insert(tk.END, f"{title}: {message}")

    def delete_selected_student(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select a student before deleting.")
            return
        if not messagebox.askyesno("Delete student", "Delete the selected student from the register?"):
            return
        student_id = self.student_tree.item(selected[0], "values")[0]
        delete_student(student_id)
        self.refresh_all()

    def _selected_student_id(self, picker):
        return self.student_by_display.get(picker.get())

    @staticmethod
    def _clear_entries(*entries):
        for entry in entries:
            entry.delete(0, tk.END)

import tkinter as tk
from tkinter import messagebox, ttk
from database import authenticate_user, initialize_database, register_user
from config import APP_TITLE
from style import apply_professional_theme


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("420x420")
        self.resizable(False, False)
        apply_professional_theme(self)
        self._build_ui()

    def _build_ui(self):
        main_frame = ttk.Frame(self, padding=24)
        main_frame.pack(fill="both", expand=True)

        card = ttk.Frame(main_frame, style="Card.TFrame", padding=24)
        card.pack(fill="both", expand=True)

        self.title_label = ttk.Label(card, text="Welcome Back", style="Title.TLabel")
        self.title_label.pack(anchor="w", pady=(0, 4))
        self.subtitle_label = ttk.Label(card, text="Sign in to manage your coaching center smoothly.", style="SubTitle.TLabel")
        self.subtitle_label.pack(anchor="w", pady=(0, 16))

        ttk.Label(card, text="Username").pack(anchor="w")
        self.username_entry = ttk.Entry(card, width=30)
        self.username_entry.pack(fill="x", pady=(4, 10))

        ttk.Label(card, text="Password").pack(anchor="w")
        self.password_entry = ttk.Entry(card, width=30, show="*")
        self.password_entry.pack(fill="x", pady=(4, 14))

        self.action_button = ttk.Button(card, text="Login", style="Accent.TButton", command=self.handle_login)
        self.action_button.pack(fill="x")

        self.switch_button = ttk.Button(card, text="Create New Account", style="Secondary.TButton", command=self.toggle_mode)
        self.switch_button.pack(fill="x", pady=(10, 0))

        self.mode = "login"
        self.username_entry.focus_set()
        self.bind("<Return>", self.handle_login)

    def toggle_mode(self):
        if self.mode == "login":
            self.mode = "signup"
            self.title_label.configure(text="Create Account")
            self.subtitle_label.configure(text="Register a new account for the coaching center.")
            self.action_button.configure(text="Sign Up")
            self.switch_button.configure(text="Back to Login")
        else:
            self.mode = "login"
            self.title_label.configure(text="Welcome Back")
            self.subtitle_label.configure(text="Sign in to manage your coaching center smoothly.")
            self.action_button.configure(text="Login")
            self.switch_button.configure(text="Create New Account")
        self.clear_fields()

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.username_entry.focus_set()

    def handle_login(self, event=None):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return "break"

        if self.mode == "signup":
            if register_user(username, password, role="student"):
                messagebox.showinfo("Success", "Account created successfully. You can now log in.")
                self.toggle_mode()
            else:
                messagebox.showerror("Error", "Username already exists or the input is invalid.")
            return "break"

        if authenticate_user(username, password):
            self.clear_fields()
            self.destroy()
            from dashboard import DashboardWindow
            dashboard = DashboardWindow(username=username)
            dashboard.protocol("WM_DELETE_WINDOW", dashboard.destroy)
            dashboard.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password")
        return "break"


def main():
    initialize_database()
    app = LoginWindow()
    app.mainloop()

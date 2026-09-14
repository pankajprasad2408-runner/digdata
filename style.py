import tkinter as tk
from tkinter import ttk


def apply_professional_theme(root):
    style = ttk.Style(root)
    available_themes = style.theme_names()
    if "clam" in available_themes:
        style.theme_use("clam")
    elif "alt" in available_themes:
        style.theme_use("alt")

    root.configure(bg="#f4f7fb")
    style.configure("TFrame", background="#f4f7fb")
    style.configure("Card.TFrame", background="#ffffff")
    style.configure("Panel.TFrame", background="#ffffff")
    style.configure("Header.TLabel", background="#f4f7fb", foreground="#1d4ed8", font=("Segoe UI", 15, "bold"))
    style.configure("Title.TLabel", background="#ffffff", foreground="#111827", font=("Segoe UI", 20, "bold"))
    style.configure("SubTitle.TLabel", background="#ffffff", foreground="#475569", font=("Segoe UI", 11))
    style.configure("Eyebrow.TLabel", background="#ffffff", foreground="#2563eb", font=("Segoe UI", 9, "bold"))
    style.configure("Section.TLabel", background="#ffffff", foreground="#111827", font=("Segoe UI", 14, "bold"))
    style.configure("Metric.TFrame", background="#ffffff", relief="solid", borderwidth=1)
    style.configure("MetricLabel.TLabel", background="#ffffff", foreground="#64748b", font=("Segoe UI", 9, "bold"))
    style.configure("MetricValue.TLabel", background="#ffffff", foreground="#0f172a", font=("Segoe UI", 18, "bold"))
    style.configure("Body.TLabel", background="#f4f7fb", foreground="#475569", font=("Segoe UI", 10))
    style.configure("Accent.TButton", background="#2563eb", foreground="#ffffff", padding=(12, 8))
    style.map("Accent.TButton", background=[("active", "#1d4ed8")], foreground=[("active", "#ffffff")])
    style.configure("Secondary.TButton", background="#e2e8f0", foreground="#0f172a", padding=(10, 6))
    style.map("Secondary.TButton", background=[("active", "#cbd5e1")], foreground=[("active", "#0f172a")])
    style.configure("TLabel", background="#f4f7fb", foreground="#334155", font=("Segoe UI", 10))
    style.configure("TEntry", fieldbackground="#ffffff", foreground="#0f172a")
    style.configure("TNotebook", background="#f4f7fb")
    style.configure("TNotebook.Tab", padding=(12, 8), font=("Segoe UI", 10, "bold"))
    style.map("TNotebook.Tab", background=[("selected", "#ffffff")], foreground=[("selected", "#1d4ed8")])
    style.configure("Treeview", rowheight=28, fieldbackground="#ffffff", background="#ffffff")
    style.configure("Treeview.Heading", background="#e2e8f0", foreground="#0f172a", font=("Segoe UI", 10, "bold"))
    style.map("Treeview.Heading", background=[("active", "#cbd5e1")])

"""
LishePro - Professional Nutrition Portal
Developer/Nutritionist Application
Kenya MOH-Aligned Nutrition Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from common_utils import (
    MOH_AGE_BRACKETS, CONDITIONS, CONSENT_TEXT,
    ROLE_DEVELOPER, hash_password
)
from backend_manager import ServerBackend

class LisheProApp(tk.Tk):
    """
    LishePro - Professional Nutrition Portal
    For Nutritionists and Healthcare Professionals
    """
    
    def __init__(self):
        super().__init__()
        self.title("LishePro - Professional Nutrition Portal")
        self.geometry("1000x700")
        self.configure(bg="#F0F2F5")
        self.minsize(900, 600)
        
        self.server = ServerBackend()
        self.current_user_id = None
        self.user_info = {}

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.show_login_screen()

    def configure_styles(self):
        # Professional Color Palette
        self.PRIMARY = "#1A237E"       # Deep Indigo
        self.PRIMARY_LIGHT = "#3949AB"
        self.SECONDARY = "#00897B"     # Teal
        self.ACCENT = "#304FFE"        # Blue Accent
        self.BG = "#F0F2F5"            # Light Gray
        self.SIDEBAR_BG = "#1A237E"
        self.CARD = "#FFFFFF"
        self.TEXT = "#212121"
        self.TEXT_LIGHT = "#757575"
        self.SUCCESS = "#43A047"
        self.WARNING = "#FB8C00"
        self.ERROR = "#E53935"
        
        self.style.configure("TFrame", background=self.BG)
        self.style.configure("Sidebar.TFrame", background=self.SIDEBAR_BG)
        self.style.configure("Card.TFrame", background=self.CARD)
        
        self.style.configure("TLabel", background=self.BG, foreground=self.TEXT, font=("Segoe UI", 11))
        self.style.configure("Card.TLabel", background=self.CARD, foreground=self.TEXT, font=("Segoe UI", 11))
        self.style.configure("Sidebar.TLabel", background=self.SIDEBAR_BG, foreground="white", font=("Segoe UI", 11))
        
        self.style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"), foreground=self.PRIMARY, background=self.BG)
        self.style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground=self.PRIMARY, background=self.BG)
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 13, "bold"), foreground=self.TEXT, background=self.CARD)
        
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"), background=self.PRIMARY, foreground="white", padding=12)
        self.style.map("TButton", background=[('active', self.PRIMARY_LIGHT)])
        
        self.style.configure("Secondary.TButton", background=self.SECONDARY)
        self.style.map("Secondary.TButton", background=[('active', "#00695C")])

    def clear_window(self):
        for w in self.winfo_children():
            w.destroy()

    # ==================== LOGIN SCREEN ====================
    
    def show_login_screen(self):
        self.clear_window()
        
        # Center Container
        container = tk.Frame(self, bg=self.BG)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo
        tk.Label(container, text="🩺", font=("Segoe UI Emoji", 64), bg=self.BG).pack()
        tk.Label(container, text="LishePro", font=("Segoe UI", 28, "bold"), 
                 bg=self.BG, fg=self.PRIMARY).pack()
        tk.Label(container, text="Professional Nutrition Portal", font=("Segoe UI", 12), 
                 bg=self.BG, fg=self.TEXT_LIGHT).pack(pady=(0, 30))
        
        # Login Card
        card = tk.Frame(container, bg=self.CARD, padx=40, pady=30)
        card.pack()
        
        tk.Label(card, text="Sign In", font=("Segoe UI", 16, "bold"), 
                 bg=self.CARD, fg=self.PRIMARY).pack(pady=(0, 20))
        
        # Email
        tk.Label(card, text="Email", font=("Segoe UI", 10), bg=self.CARD, fg=self.TEXT_LIGHT).pack(anchor="w")
        self.login_email = ttk.Entry(card, width=35, font=("Segoe UI", 11))
        self.login_email.pack(pady=(0, 15), ipady=8)
        
        # Password
        tk.Label(card, text="Password", font=("Segoe UI", 10), bg=self.CARD, fg=self.TEXT_LIGHT).pack(anchor="w")
        self.login_password = ttk.Entry(card, width=35, show="●", font=("Segoe UI", 11))
        self.login_password.pack(pady=(0, 20), ipady=8)
        
        # Sign In Button
        tk.Button(card, text="Sign In", font=("Segoe UI", 11, "bold"),
                  bg=self.PRIMARY, fg="white", width=30, pady=10, relief="flat",
                  command=self.do_login).pack(pady=10)
        
        tk.Label(card, text="Contact admin for account access", font=("Segoe UI", 9),
                 bg=self.CARD, fg=self.TEXT_LIGHT).pack(pady=(10, 0))

    def do_login(self):
        email = self.login_email.get().strip()
        password = self.login_password.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter credentials")
            return
        
        resp = self.server.login(email, password)
        if resp["status"] == "success":
            if resp["role"] != ROLE_DEVELOPER:
                messagebox.showerror("Access Denied", "This portal is for nutrition professionals only.")
                return
            
            self.current_user_id = resp["user_id"]
            self.user_info = {"email": email}
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", resp.get("message", "Invalid credentials"))

    # ==================== MAIN DASHBOARD ====================
    
    def show_dashboard(self):
        self.clear_window()
        
        # Main Layout: Sidebar + Content
        main_container = tk.Frame(self, bg=self.BG)
        main_container.pack(fill="both", expand=True)
        
        # Sidebar
        sidebar = tk.Frame(main_container, bg=self.SIDEBAR_BG, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Sidebar Header
        tk.Label(sidebar, text="🩺 LishePro", font=("Segoe UI", 16, "bold"),
                 bg=self.SIDEBAR_BG, fg="white").pack(pady=30)
        
        # Navigation
        self.current_section = tk.StringVar(value="dashboard")
        
        nav_items = [
            ("📊 Dashboard", "dashboard"),
            ("👥 Users", "clients"),
            ("❓ Questions", "questions"),
            ("📈 Reports", "reports"),
            ("⚙️ Settings", "settings")
        ]
        
        for text, section in nav_items:
            btn = tk.Button(sidebar, text=text, font=("Segoe UI", 11),
                            bg=self.SIDEBAR_BG, fg="white", bd=0, anchor="w",
                            padx=20, pady=12, activebackground=self.PRIMARY_LIGHT,
                            command=lambda s=section: self.navigate_to(s))
            btn.pack(fill="x")
        
        # User Info at Bottom
        user_frame = tk.Frame(sidebar, bg=self.SIDEBAR_BG)
        user_frame.pack(side="bottom", fill="x", pady=20)
        
        tk.Label(user_frame, text=f"👤 {self.user_info.get('email', 'User')[:20]}",
                 font=("Segoe UI", 9), bg=self.SIDEBAR_BG, fg="white").pack(pady=5)
        
        tk.Button(user_frame, text="Sign Out", font=("Segoe UI", 9),
                  bg=self.PRIMARY_LIGHT, fg="white", bd=0, pady=5,
                  command=self.sign_out).pack(fill="x", padx=20)
        
        # Content Area
        self.content_area = tk.Frame(main_container, bg=self.BG)
        self.content_area.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        self.show_dashboard_section()

    def navigate_to(self, section):
        self.current_section.set(section)
        
        # Clear content
        for w in self.content_area.winfo_children():
            w.destroy()
        
        if section == "dashboard":
            self.show_dashboard_section()
        elif section == "clients":
            self.show_clients_section()
        elif section == "questions":
            self.show_questions_section()
        elif section == "reports":
            self.show_reports_section()
        elif section == "settings":
            self.show_settings_section()

    def show_dashboard_section(self):
        # Header
        tk.Label(self.content_area, text="Dashboard", font=("Segoe UI", 22, "bold"),
                 bg=self.BG, fg=self.PRIMARY).pack(anchor="w", pady=(0, 20))
        
        # Stats Cards
        stats_frame = tk.Frame(self.content_area, bg=self.BG)
        stats_frame.pack(fill="x", pady=(0, 30))
        
        # Get Stats
        stats = self.server.get_dashboard_stats()
        
        stat_data = [
            ("Total Users", stats.get("total_clients", 0), self.SECONDARY, "👥"),
            ("Active Today", stats.get("active_today", 0), self.SUCCESS, "✓"),
            ("Pending Questions", stats.get("pending_questions", 0), self.WARNING, "❓"),
            ("Diet Plans Generated", stats.get("diet_plans", 0), self.ACCENT, "🥗")
        ]
        
        for title, value, color, icon in stat_data:
            card = tk.Frame(stats_frame, bg=self.CARD, padx=20, pady=20, width=180)
            card.pack(side="left", padx=(0, 15))
            card.pack_propagate(False)
            card.configure(height=120)
            
            # Color Strip
            tk.Frame(card, bg=color, height=4).pack(fill="x", pady=(0, 10))
            
            tk.Label(card, text=icon + " " + title, font=("Segoe UI", 10),
                     bg=self.CARD, fg=self.TEXT_LIGHT).pack(anchor="w")
            tk.Label(card, text=str(value), font=("Segoe UI", 28, "bold"),
                     bg=self.CARD, fg=color).pack(anchor="w")
        
        # Recent Activity
        activity_frame = tk.Frame(self.content_area, bg=self.CARD, padx=20, pady=20)
        activity_frame.pack(fill="both", expand=True)
        
        tk.Label(activity_frame, text="📋 Recent Activity", font=("Segoe UI", 14, "bold"),
                 bg=self.CARD, fg=self.PRIMARY).pack(anchor="w", pady=(0, 15))
        
        # Sample activities
        activities = [
            ("New user registered", "2 minutes ago", self.SUCCESS),
            ("Diet plan generated", "15 minutes ago", self.ACCENT),
            ("Question answered", "1 hour ago", self.SECONDARY),
            ("User completed assessment", "2 hours ago", self.SUCCESS)
        ]
        
        for text, time, color in activities:
            row = tk.Frame(activity_frame, bg=self.CARD)
            row.pack(fill="x", pady=8)
            
            tk.Frame(row, bg=color, width=4, height=20).pack(side="left", padx=(0, 15))
            tk.Label(row, text=text, font=("Segoe UI", 11), bg=self.CARD).pack(side="left")
            tk.Label(row, text=time, font=("Segoe UI", 9), bg=self.CARD, fg=self.TEXT_LIGHT).pack(side="right")

    def show_clients_section(self):
        tk.Label(self.content_area, text="User Management", font=("Segoe UI", 22, "bold"),
                 bg=self.BG, fg=self.PRIMARY).pack(anchor="w", pady=(0, 20))
        
        # Search Bar
        search_frame = tk.Frame(self.content_area, bg=self.BG)
        search_frame.pack(fill="x", pady=(0, 20))
        
        tk.Entry(search_frame, font=("Segoe UI", 11), width=40).pack(side="left", ipady=8)
        tk.Button(search_frame, text="🔍 Search", font=("Segoe UI", 10),
                  bg=self.PRIMARY, fg="white", relief="flat", padx=15).pack(side="left", padx=10)
        
        # Client List
        list_frame = tk.Frame(self.content_area, bg=self.CARD, padx=20, pady=20)
        list_frame.pack(fill="both", expand=True)
        
        # Column Headers
        header = tk.Frame(list_frame, bg="#E8EAF6")
        header.pack(fill="x", pady=(0, 10))
        
        headers = ["Name/Email", "Age Bracket", "Status", "Last Active", "Actions"]
        widths = [200, 120, 120, 120, 100]
        
        for h, w in zip(headers, widths):
            tk.Label(header, text=h, font=("Segoe UI", 10, "bold"), bg="#E8EAF6",
                     width=w//8, anchor="w").pack(side="left", padx=10, pady=8)
        
        # Sample Data
        clients = [
            ("jane@example.com", "20-59y", "Normal", "Today"),
            ("john@example.com", "60+y", "Overweight", "Yesterday"),
            ("mary@example.com", "pregnant", "Underweight", "3 days ago")
        ]
        
        for email, age, status, last in clients:
            row = tk.Frame(list_frame, bg=self.CARD)
            row.pack(fill="x", pady=5)
            
            tk.Label(row, text=email, font=("Segoe UI", 10), bg=self.CARD, width=25, anchor="w").pack(side="left", padx=10)
            tk.Label(row, text=MOH_AGE_BRACKETS.get(age, age), font=("Segoe UI", 10), bg=self.CARD, width=15, anchor="w").pack(side="left", padx=10)
            
            status_color = self.SUCCESS if status == "Normal" else self.WARNING
            tk.Label(row, text=status, font=("Segoe UI", 10), bg=self.CARD, fg=status_color, width=15, anchor="w").pack(side="left", padx=10)
            
            tk.Label(row, text=last, font=("Segoe UI", 10), bg=self.CARD, fg=self.TEXT_LIGHT, width=15, anchor="w").pack(side="left", padx=10)
            
            tk.Button(row, text="View", font=("Segoe UI", 9), bg=self.ACCENT, fg="white", 
                      relief="flat", padx=10).pack(side="left", padx=10)

    def show_questions_section(self):
        tk.Label(self.content_area, text="User Questions", font=("Segoe UI", 22, "bold"),
                 bg=self.BG, fg=self.PRIMARY).pack(anchor="w", pady=(0, 20))
        
        # Tabs
        tab_frame = tk.Frame(self.content_area, bg=self.BG)
        tab_frame.pack(fill="x", pady=(0, 20))
        
        tk.Button(tab_frame, text="Pending (3)", font=("Segoe UI", 10, "bold"),
                  bg=self.WARNING, fg="white", relief="flat", padx=15, pady=8).pack(side="left", padx=(0, 10))
        tk.Button(tab_frame, text="Answered", font=("Segoe UI", 10),
                  bg=self.CARD, fg=self.TEXT, relief="solid", bd=1, padx=15, pady=8).pack(side="left")
        
        # Questions List
        questions_frame = tk.Frame(self.content_area, bg=self.CARD, padx=20, pady=20)
        questions_frame.pack(fill="both", expand=True)
        
        # Sample Questions
        questions = self.server.get_pending_questions()
        
        if not questions:
            tk.Label(questions_frame, text="No pending questions", font=("Segoe UI", 12),
                     bg=self.CARD, fg=self.TEXT_LIGHT).pack(pady=30)
        else:
            for q in questions[:5]:
                self.create_question_card(questions_frame, q)

    def create_question_card(self, parent, question):
        card = tk.Frame(parent, bg="#FAFAFA", padx=15, pady=15)
        card.pack(fill="x", pady=8)
        
        # Header
        header = tk.Frame(card, bg="#FAFAFA")
        header.pack(fill="x")
        
        tk.Label(header, text=f"👤 User #{question.get('user_id', 'Unknown')}", 
                 font=("Segoe UI", 10, "bold"), bg="#FAFAFA", fg=self.PRIMARY).pack(side="left")
        tk.Label(header, text=question.get('timestamp', 'Recently'), 
                 font=("Segoe UI", 9), bg="#FAFAFA", fg=self.TEXT_LIGHT).pack(side="right")
        
        # Question Text
        tk.Label(card, text=question.get('message', 'No message'), 
                 font=("Segoe UI", 11), bg="#FAFAFA", wraplength=600, justify="left").pack(anchor="w", pady=10)
        
        # Response Area
        response_frame = tk.Frame(card, bg="#FAFAFA")
        response_frame.pack(fill="x", pady=(5, 0))
        
        response_entry = tk.Entry(response_frame, font=("Segoe UI", 10), width=60)
        response_entry.pack(side="left", ipady=6)
        
        def send_response():
            resp_text = response_entry.get()
            if resp_text:
                self.server.answer_question(question.get('id'), resp_text)
                messagebox.showinfo("Sent", "Response sent successfully!")
                self.navigate_to("questions")
        
        tk.Button(response_frame, text="Send Response", font=("Segoe UI", 10, "bold"),
                  bg=self.SECONDARY, fg="white", relief="flat", padx=15,
                  command=send_response).pack(side="left", padx=10)

    def show_reports_section(self):
        tk.Label(self.content_area, text="Reports & Analytics", font=("Segoe UI", 22, "bold"),
                 bg=self.BG, fg=self.PRIMARY).pack(anchor="w", pady=(0, 20))
        
        # Report Cards
        reports_frame = tk.Frame(self.content_area, bg=self.BG)
        reports_frame.pack(fill="x", pady=20)
        
        report_types = [
            ("📊 User Statistics", "Overview of all registered users"),
            ("🥗 Diet Plan Analysis", "Most recommended foods and patterns"),
            ("📈 Health Trends", "Nutritional status distribution"),
            ("📋 Activity Report", "User engagement metrics")
        ]
        
        for title, desc in report_types:
            card = tk.Frame(reports_frame, bg=self.CARD, padx=20, pady=20)
            card.pack(fill="x", pady=8)
            
            tk.Label(card, text=title, font=("Segoe UI", 12, "bold"), 
                     bg=self.CARD, fg=self.PRIMARY).pack(anchor="w")
            tk.Label(card, text=desc, font=("Segoe UI", 10), 
                     bg=self.CARD, fg=self.TEXT_LIGHT).pack(anchor="w", pady=(5, 10))
            tk.Button(card, text="Generate Report", font=("Segoe UI", 10),
                      bg=self.ACCENT, fg="white", relief="flat", padx=15).pack(anchor="w")

    def show_settings_section(self):
        tk.Label(self.content_area, text="Settings", font=("Segoe UI", 22, "bold"),
                 bg=self.BG, fg=self.PRIMARY).pack(anchor="w", pady=(0, 20))
        
        # Settings Card
        card = tk.Frame(self.content_area, bg=self.CARD, padx=30, pady=30)
        card.pack(fill="x")
        
        tk.Label(card, text="Account Settings", font=("Segoe UI", 14, "bold"),
                 bg=self.CARD, fg=self.PRIMARY).pack(anchor="w", pady=(0, 20))
        
        # Email
        tk.Label(card, text="Email", font=("Segoe UI", 10), bg=self.CARD, fg=self.TEXT_LIGHT).pack(anchor="w")
        email_entry = ttk.Entry(card, width=40, font=("Segoe UI", 11))
        email_entry.insert(0, self.user_info.get('email', ''))
        email_entry.pack(anchor="w", pady=(0, 15), ipady=5)
        
        # Change Password
        tk.Label(card, text="New Password (leave blank to keep current)", 
                 font=("Segoe UI", 10), bg=self.CARD, fg=self.TEXT_LIGHT).pack(anchor="w")
        ttk.Entry(card, width=40, show="●", font=("Segoe UI", 11)).pack(anchor="w", pady=(0, 20), ipady=5)
        
        tk.Button(card, text="Save Changes", font=("Segoe UI", 11, "bold"),
                  bg=self.PRIMARY, fg="white", relief="flat", padx=20, pady=10).pack(anchor="w")

    def sign_out(self):
        self.current_user_id = None
        self.user_info = {}
        self.show_login_screen()


if __name__ == "__main__":
    app = LisheProApp()
    app.mainloop()

"""
LisheBora - Your Nutrition Partner
Mobile-Ready Client Application
Kenya MOH-Aligned Nutrition Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime
from common_utils import (
    MOH_AGE_BRACKETS, KENYAN_FOOD_DB, CONDITIONS, HEALTH_TIPS, CONSENT_TEXT,
    calculate_bmi, calculate_age_years, get_age_bracket_from_age,
    get_comprehensive_status, generate_diet_plan, 
    analyze_intake, ROLE_CLIENT
)
from backend_manager import ClientLocalManager, ServerBackend

class LisheBoraApp(tk.Tk):
    """
    LisheBora - Your Personal Nutrition Partner
    A client-centered nutrition management application
    """
    
    def __init__(self):
        super().__init__()
        self.title("LisheBora - Your Nutrition Partner")
        self.geometry("420x900")
        self.configure(bg="#FAFAFA")
        self.resizable(True, True)
        
        self.local_manager = ClientLocalManager()
        self.server = ServerBackend()
        
        # User State
        self.current_user_id = None
        self.user_profile = {}
        self.generated_plan = {}
        self.today_log = []

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.show_welcome_screen()

    def configure_styles(self):
        # Premium Color Palette
        self.PRIMARY = "#1B5E20"      # Deep Forest Green
        self.PRIMARY_LIGHT = "#4CAF50" # Light Green
        self.SECONDARY = "#FF6D00"    # Vibrant Orange
        self.BG = "#FAFAFA"           # Off-White
        self.CARD = "#FFFFFF"         # Pure White
        self.TEXT = "#212121"         # Near Black
        self.TEXT_LIGHT = "#757575"   # Gray
        self.ACCENT = "#E8F5E9"       # Light Green Tint
        self.WARNING = "#FFA000"      # Amber
        self.ERROR = "#D32F2F"        # Red
        self.SUCCESS = "#388E3C"      # Green
        
        self.style.configure("TFrame", background=self.BG)
        self.style.configure("Card.TFrame", background=self.CARD)
        
        self.style.configure("TLabel", background=self.BG, foreground=self.TEXT, font=("Segoe UI", 11))
        self.style.configure("Card.TLabel", background=self.CARD, foreground=self.TEXT, font=("Segoe UI", 11))
        
        self.style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"), foreground=self.PRIMARY, background=self.BG)
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground=self.PRIMARY, background=self.BG)
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 13, "bold"), foreground=self.TEXT, background=self.CARD)
        
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"), background=self.PRIMARY, foreground="white", padding=12)
        self.style.map("TButton", background=[('active', self.PRIMARY_LIGHT)])
        
        self.style.configure("Secondary.TButton", background=self.SECONDARY)
        self.style.map("Secondary.TButton", background=[('active', "#E65100")])
        
        self.style.configure("Outline.TButton", background=self.CARD, foreground=self.PRIMARY)
        
        self.style.configure("TEntry", font=("Segoe UI", 11), padding=8)
        self.style.configure("TCombobox", font=("Segoe UI", 11), padding=5)

    def clear_window(self):
        for w in self.winfo_children():
            w.destroy()

    # ==================== WELCOME / AUTH SCREENS ====================
    
    def show_welcome_screen(self):
        self.clear_window()
        
        frame = ttk.Frame(self, padding=30)
        frame.pack(fill="both", expand=True)
        
        # Logo Area
        logo_frame = ttk.Frame(frame)
        logo_frame.pack(pady=(60, 30))
        
        # Using text-based logo with food emoji
        tk.Label(logo_frame, text="🥗", font=("Segoe UI Emoji", 64), bg=self.BG).pack()
        ttk.Label(logo_frame, text="LisheBora", style="Title.TLabel").pack()
        ttk.Label(logo_frame, text="Your Nutrition Partner", font=("Segoe UI", 12, "italic"), foreground=self.TEXT_LIGHT).pack(pady=(5, 0))
        
        # Tagline
        ttk.Label(frame, text="Personalized nutrition guidance\naligned with Kenya MOH standards", 
                  font=("Segoe UI", 11), foreground=self.TEXT_LIGHT, justify="center").pack(pady=20)
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=40)
        
        ttk.Button(btn_frame, text="Sign In", command=self.show_login_screen).pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Create Account", command=self.show_register_screen, style="Secondary.TButton").pack(fill="x", pady=5)
        
        # Footer
        ttk.Label(frame, text="© 2024 LisheBora Kenya", font=("Segoe UI", 9), foreground=self.TEXT_LIGHT).pack(side="bottom", pady=20)

    def show_login_screen(self):
        self.clear_window()
        
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)
        
        # Back Button
        tk.Button(frame, text="← Back", font=("Segoe UI", 10), bg=self.BG, fg=self.PRIMARY, 
                  bd=0, command=self.show_welcome_screen).pack(anchor="w")
        
        # Header
        ttk.Label(frame, text="Welcome Back", style="Title.TLabel").pack(pady=(30, 5))
        ttk.Label(frame, text="Sign in to continue", foreground=self.TEXT_LIGHT).pack(pady=(0, 30))
        
        # Form
        form = ttk.Frame(frame, style="Card.TFrame", padding=20)
        form.pack(fill="x")
        
        ttk.Label(form, text="📧  Email or Phone", style="Card.TLabel").pack(anchor="w")
        self.login_email = ttk.Entry(form, font=("Segoe UI", 12))
        self.login_email.pack(fill="x", pady=(5, 15), ipady=8)
        
        ttk.Label(form, text="🔒  Password", style="Card.TLabel").pack(anchor="w")
        self.login_password = ttk.Entry(form, show="●", font=("Segoe UI", 12))
        self.login_password.pack(fill="x", pady=(5, 20), ipady=8)
        
        ttk.Button(form, text="Sign In Securely", command=self.do_login).pack(fill="x", pady=10)

    def show_register_screen(self):
        self.clear_window()
        
        # Scrollable Frame
        canvas = tk.Canvas(self, bg=self.BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas, padding=25)
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=400)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Back Button
        tk.Button(scroll_frame, text="← Back", font=("Segoe UI", 10), bg=self.BG, fg=self.PRIMARY, 
                  bd=0, command=self.show_welcome_screen).pack(anchor="w")
        
        # Header
        ttk.Label(scroll_frame, text="Create Account", style="Title.TLabel").pack(pady=(20, 5))
        ttk.Label(scroll_frame, text="Join LisheBora today", foreground=self.TEXT_LIGHT).pack(pady=(0, 20))
        
        # Form Card
        form = ttk.Frame(scroll_frame, style="Card.TFrame", padding=20)
        form.pack(fill="x")
        
        # Personal Info Section
        ttk.Label(form, text="👤  Personal Information", style="SubHeader.TLabel").pack(anchor="w", pady=(0, 10))
        
        ttk.Label(form, text="Full Name", style="Card.TLabel").pack(anchor="w")
        self.reg_name = ttk.Entry(form)
        self.reg_name.pack(fill="x", pady=(2, 10), ipady=5)
        
        ttk.Label(form, text="Email Address", style="Card.TLabel").pack(anchor="w")
        self.reg_email = ttk.Entry(form)
        self.reg_email.pack(fill="x", pady=(2, 10), ipady=5)
        
        ttk.Label(form, text="Phone Number", style="Card.TLabel").pack(anchor="w")
        self.reg_phone = ttk.Entry(form)
        self.reg_phone.pack(fill="x", pady=(2, 10), ipady=5)
        
        ttk.Label(form, text="Date of Birth (YYYY-MM-DD)", style="Card.TLabel").pack(anchor="w")
        self.reg_dob = ttk.Entry(form)
        self.reg_dob.insert(0, "1990-01-01")
        self.reg_dob.pack(fill="x", pady=(2, 10), ipady=5)
        
        ttk.Label(form, text="Gender", style="Card.TLabel").pack(anchor="w")
        self.reg_gender = ttk.Combobox(form, values=["Female", "Male"], state="readonly")
        self.reg_gender.set("Female")
        self.reg_gender.pack(fill="x", pady=(2, 10))
        
        # Security Section
        ttk.Label(form, text="🔐  Security", style="SubHeader.TLabel").pack(anchor="w", pady=(15, 10))
        
        ttk.Label(form, text="Password", style="Card.TLabel").pack(anchor="w")
        self.reg_password = ttk.Entry(form, show="●")
        self.reg_password.pack(fill="x", pady=(2, 10), ipady=5)
        
        ttk.Label(form, text="Confirm Password", style="Card.TLabel").pack(anchor="w")
        self.reg_confirm = ttk.Entry(form, show="●")
        self.reg_confirm.pack(fill="x", pady=(2, 15), ipady=5)
        
        ttk.Button(form, text="Create Account", command=self.do_register).pack(fill="x", pady=10)

    def do_login(self):
        email = self.login_email.get().strip()
        password = self.login_password.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter your credentials")
            return
            
        resp = self.server.login(email, password)
        if resp["status"] == "success":
            if resp["role"] != ROLE_CLIENT:
                messagebox.showerror("Access Denied", "Please use the professional portal for nutritionist access.")
                return
            
            self.current_user_id = resp["user_id"]
            self.user_profile = {
                "age_bracket": resp.get("age_bracket", "20-59y"),
                "dob": resp.get("dob"),
                "gender": resp.get("gender", "Female")
            }
            
            if not resp.get("consent_given"):
                self.show_consent_screen()
            else:
                self.show_main_dashboard()
        else:
            messagebox.showerror("Login Failed", resp.get("message", "Invalid credentials"))

    def do_register(self):
        if self.reg_password.get() != self.reg_confirm.get():
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        dob = self.reg_dob.get()
        age = calculate_age_years(dob)
        if age is None:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return
        
        age_bracket = get_age_bracket_from_age(age)
        
        resp = self.server.register_user(
            self.reg_email.get().strip(),
            self.reg_phone.get().strip(),
            self.reg_password.get(),
            ROLE_CLIENT,
            age_bracket
        )
        
        if resp["status"] == "success":
            messagebox.showinfo("Success", "Account created successfully!\nPlease sign in.")
            self.show_login_screen()
        else:
            messagebox.showerror("Registration Failed", resp.get("message", "Could not create account"))

    # ==================== CONSENT SCREEN ====================
    
    def show_consent_screen(self):
        self.clear_window()
        
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="📋", font=("Segoe UI Emoji", 48)).pack(pady=(20, 10))
        ttk.Label(frame, text="Informed Consent", style="Header.TLabel").pack()
        
        # Consent Text in Scrollable Area
        text_frame = tk.Frame(frame, bg=self.CARD, padx=15, pady=15)
        text_frame.pack(fill="both", expand=True, pady=20)
        
        text_widget = tk.Text(text_frame, wrap="word", font=("Segoe UI", 10), 
                              bg=self.CARD, fg=self.TEXT, relief="flat", height=15)
        text_widget.insert("1.0", CONSENT_TEXT)
        text_widget.config(state="disabled")
        text_widget.pack(fill="both", expand=True)
        
        # Consent Toggle
        self.consent_var = tk.IntVar(value=0)
        consent_frame = ttk.Frame(frame)
        consent_frame.pack(fill="x", pady=15)
        
        chk = ttk.Checkbutton(consent_frame, text="I have read and agree to the terms above", 
                              variable=self.consent_var, command=self.toggle_consent_button)
        chk.pack()
        
        self.consent_btn = ttk.Button(frame, text="Continue", state="disabled", command=self.grant_consent)
        self.consent_btn.pack(fill="x", pady=10)

    def toggle_consent_button(self):
        if self.consent_var.get():
            self.consent_btn.config(state="normal")
        else:
            self.consent_btn.config(state="disabled")

    def grant_consent(self):
        self.server.set_consent(self.current_user_id)
        self.show_main_dashboard()

    # ==================== MAIN DASHBOARD ====================
    
    def show_main_dashboard(self):
        self.clear_window()
        
        # Tab Navigation
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.tab_home = ttk.Frame(notebook)
        self.tab_diet = ttk.Frame(notebook)
        self.tab_log = ttk.Frame(notebook)
        self.tab_chat = ttk.Frame(notebook)
        self.tab_profile = ttk.Frame(notebook)

        # Using emoji icons for tabs
        notebook.add(self.tab_home, text="🏠 Home")
        notebook.add(self.tab_diet, text="🥗 My Diet")
        notebook.add(self.tab_log, text="📝 Log")
        notebook.add(self.tab_chat, text="💬 Support")
        notebook.add(self.tab_profile, text="👤 Profile")

        self.build_home_tab()
        self.build_diet_tab()
        self.build_log_tab()
        self.build_chat_tab()
        self.build_profile_tab()

    def build_home_tab(self):
        # Scrollable
        canvas = tk.Canvas(self.tab_home, bg=self.BG, highlightthickness=0)
        ys = ttk.Scrollbar(self.tab_home, orient="vertical", command=canvas.yview)
        frame = ttk.Frame(canvas, padding=20)
        
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw", width=400)
        canvas.configure(yscrollcommand=ys.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        ys.pack(side="right", fill="y")

        # Welcome Banner with Health Tip
        banner = tk.Frame(frame, bg=self.ACCENT, padx=15, pady=15)
        banner.pack(fill="x", pady=(0, 20))
        
        tip = random.choice(HEALTH_TIPS)
        tk.Label(banner, text="🌿 Welcome!", font=("Segoe UI", 16, "bold"), 
                 bg=self.ACCENT, fg=self.PRIMARY).pack(anchor="w")
        tk.Label(banner, text=tip, font=("Segoe UI", 10, "italic"), 
                 bg=self.ACCENT, fg=self.TEXT, wraplength=340, justify="left").pack(anchor="w", pady=(8, 0))

        # Health Assessment Card
        card = tk.Frame(frame, bg=self.CARD, padx=20, pady=20)
        card.pack(fill="x", pady=10)
        
        tk.Label(card, text="📊 Health Assessment", font=("Segoe UI", 14, "bold"), 
                 bg=self.CARD, fg=self.PRIMARY).pack(anchor="w", pady=(0, 15))
        
        # Anthropometric Inputs
        input_frame = tk.Frame(card, bg=self.CARD)
        input_frame.pack(fill="x")
        
        # Row 1: Weight & Height
        row1 = tk.Frame(input_frame, bg=self.CARD)
        row1.pack(fill="x", pady=5)
        
        tk.Label(row1, text="⚖️ Weight (kg)", bg=self.CARD, font=("Segoe UI", 10)).pack(side="left")
        self.weight_var = tk.DoubleVar()
        tk.Entry(row1, textvariable=self.weight_var, width=8, font=("Segoe UI", 11)).pack(side="left", padx=10)
        
        tk.Label(row1, text="📏 Height (cm)", bg=self.CARD, font=("Segoe UI", 10)).pack(side="left", padx=(20, 0))
        self.height_var = tk.DoubleVar()
        tk.Entry(row1, textvariable=self.height_var, width=8, font=("Segoe UI", 11)).pack(side="left", padx=10)
        
        # Row 2: MUAC
        row2 = tk.Frame(input_frame, bg=self.CARD)
        row2.pack(fill="x", pady=10)
        
        tk.Label(row2, text="💪 MUAC (mm)", bg=self.CARD, font=("Segoe UI", 10)).pack(side="left")
        self.muac_var = tk.DoubleVar()
        tk.Entry(row2, textvariable=self.muac_var, width=8, font=("Segoe UI", 11)).pack(side="left", padx=10)
        
        tk.Label(row2, text="Mid-Upper Arm Circumference", bg=self.CARD, 
                 fg=self.TEXT_LIGHT, font=("Segoe UI", 9, "italic")).pack(side="left", padx=10)
        
        # Condition
        cond_frame = tk.Frame(card, bg=self.CARD)
        cond_frame.pack(fill="x", pady=10)
        
        tk.Label(cond_frame, text="🩺 Health Condition", bg=self.CARD, font=("Segoe UI", 10)).pack(anchor="w")
        self.condition_var = tk.StringVar(value="None")
        ttk.Combobox(cond_frame, textvariable=self.condition_var, values=CONDITIONS, 
                     state="readonly", font=("Segoe UI", 10)).pack(fill="x", pady=5)
        
        # Status Display
        self.status_frame = tk.Frame(card, bg="#E3F2FD", padx=15, pady=15)
        self.status_frame.pack(fill="x", pady=15)
        
        self.status_label = tk.Label(self.status_frame, text="Complete assessment to view your status", 
                                      bg="#E3F2FD", fg=self.TEXT, font=("Segoe UI", 11))
        self.status_label.pack()
        
        # Calculate Button
        tk.Button(card, text="✓ Calculate My Status", font=("Segoe UI", 11, "bold"),
                  bg=self.PRIMARY, fg="white", pady=10, relief="flat",
                  command=self.calculate_status).pack(fill="x")
        
        self.sync_label = tk.Label(frame, text="", bg=self.BG, fg=self.TEXT_LIGHT, font=("Segoe UI", 9))
        self.sync_label.pack(pady=5)

    def calculate_status(self):
        weight = self.weight_var.get()
        height = self.height_var.get()
        muac = self.muac_var.get()
        age_bracket = self.user_profile.get("age_bracket", "20-59y")
        
        if not weight or not height:
            messagebox.showerror("Incomplete", "Please enter weight and height")
            return
        
        result = get_comprehensive_status(weight, height, muac if muac else None, age_bracket)
        
        # Update status display
        self.user_profile['status'] = result['priority_status']
        self.user_profile['bmi'] = result['bmi']
        
        status_text = f"BMI: {result['bmi']} | {result['bmi_status']}\n"
        if muac:
            status_text += f"MUAC: {result['muac_status']}\n"
        status_text += f"\n{result['action']}"
        
        # Color code based on status
        if "SAM" in result['priority_status'] or "Severe" in result['priority_status']:
            self.status_frame.configure(bg="#FFEBEE")
            self.status_label.configure(bg="#FFEBEE", fg=self.ERROR)
        elif "MAM" in result['priority_status'] or "Moderate" in result['priority_status'] or "Overweight" in result['priority_status']:
            self.status_frame.configure(bg="#FFF8E1")
            self.status_label.configure(bg="#FFF8E1", fg=self.WARNING)
        else:
            self.status_frame.configure(bg="#E8F5E9")
            self.status_label.configure(bg="#E8F5E9", fg=self.SUCCESS)
        
        self.status_label.configure(text=status_text)
        
        # Sync
        self.sync_label.configure(text="✓ Data saved", fg=self.SUCCESS)
        try:
            self.local_manager.sync_with_server(self.current_user_id)
        except:
            self.sync_label.configure(text="Offline - will sync later", fg=self.WARNING)

    def build_diet_tab(self):
        frame = ttk.Frame(self.tab_diet, padding=20)
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="🥗 My Diet Plan", style="Header.TLabel").pack(pady=(0, 10))
        ttk.Label(frame, text="Personalized meal suggestions based on your profile", 
                  foreground=self.TEXT_LIGHT).pack(pady=(0, 20))
        
        ttk.Button(frame, text="Generate My Plan", command=self.generate_plan).pack(fill="x", pady=(0, 15))
        
        # Scrollable Results
        container = ttk.Frame(frame)
        container.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(container, bg=self.BG, highlightthickness=0)
        ys = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.diet_scroll = ttk.Frame(canvas)
        
        self.diet_scroll.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.diet_scroll, anchor="nw", width=380)
        canvas.configure(yscrollcommand=ys.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        ys.pack(side="right", fill="y")
        
        ttk.Label(self.diet_scroll, text="Tap 'Generate' to create your personalized plan", 
                  foreground=self.TEXT_LIGHT).pack(pady=30)

    def generate_plan(self):
        status = self.user_profile.get('status', 'Normal')
        cond = self.condition_var.get() if hasattr(self, 'condition_var') else "None"
        age_bracket = self.user_profile.get('age_bracket', '20-59y')
        
        self.generated_plan = generate_diet_plan(cond, age_bracket, status)
        self.render_diet_plan()

    def render_diet_plan(self):
        for w in self.diet_scroll.winfo_children():
            w.destroy()
        
        meals_order = ["Breakfast", "Snack (10am)", "Lunch", "Snack (4pm)", "Supper"]
        icons = {"Breakfast": "☕", "Snack (10am)": "🍎", "Lunch": "🍛", "Snack (4pm)": "🥤", "Supper": "🍲"}
        
        for meal in meals_order:
            if meal in self.generated_plan:
                data = self.generated_plan[meal]
                
                card = tk.Frame(self.diet_scroll, bg=self.CARD, padx=15, pady=15)
                card.pack(fill="x", pady=8)
                
                # Header
                header = tk.Frame(card, bg=self.CARD)
                header.pack(fill="x")
                
                tk.Label(header, text=icons.get(meal, "🍽️"), font=("Segoe UI Emoji", 20), 
                         bg=self.CARD).pack(side="left", padx=(0, 10))
                
                title_frame = tk.Frame(header, bg=self.CARD)
                title_frame.pack(side="left", fill="x", expand=True)
                
                tk.Label(title_frame, text=meal, font=("Segoe UI", 12, "bold"), 
                         bg=self.CARD, fg=self.PRIMARY).pack(anchor="w")
                tk.Label(title_frame, text=data['goal'], font=("Segoe UI", 9), 
                         bg=self.CARD, fg=self.TEXT_LIGHT).pack(anchor="w")
                
                # Main Option
                tk.Label(card, text=data['main'], font=("Segoe UI", 11), 
                         bg=self.CARD, wraplength=320, justify="left").pack(anchor="w", pady=(10, 5))
                
                # Substitutes
                if data.get('subs'):
                    tk.Label(card, text="Alternatives:", font=("Segoe UI", 9, "bold"), 
                             bg=self.CARD, fg=self.TEXT_LIGHT).pack(anchor="w", pady=(5, 2))
                    for sub in data['subs'][:2]:  # Show max 2
                        tk.Label(card, text=f"• {sub}", font=("Segoe UI", 9), 
                                 bg=self.CARD, fg=self.TEXT_LIGHT, wraplength=300).pack(anchor="w")

    def build_log_tab(self):
        frame = ttk.Frame(self.tab_log, padding=20)
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="📝 Food Diary", style="Header.TLabel").pack(pady=(0, 5))
        ttk.Label(frame, text="Track what you eat daily", foreground=self.TEXT_LIGHT).pack(pady=(0, 20))
        
        # Meal Buttons
        btn_frame = tk.Frame(frame, bg=self.BG)
        btn_frame.pack(fill="x", pady=10)
        
        meals = [("🍳 Breakfast", "Breakfast"), ("🍛 Lunch", "Lunch"), 
                 ("🍲 Supper", "Supper"), ("🍎 Snack", "Snack")]
        
        for text, meal in meals:
            tk.Button(btn_frame, text=text, font=("Segoe UI", 9), bg=self.CARD, fg=self.PRIMARY,
                      relief="solid", bd=1, padx=8, pady=6,
                      command=lambda m=meal: self.open_meal_logger(m)).pack(side="left", padx=3)
        
        # Log Display
        tk.Label(frame, text="Today's Log:", font=("Segoe UI", 11, "bold"), 
                 bg=self.BG, fg=self.TEXT).pack(anchor="w", pady=(20, 5))
        
        self.log_display = tk.Text(frame, height=8, font=("Segoe UI", 10), 
                                    relief="solid", bd=1, state="disabled")
        self.log_display.pack(fill="x", pady=5)
        
        # Analyze Button
        tk.Button(frame, text="📊 Analyze My Diet", font=("Segoe UI", 11, "bold"),
                  bg=self.SECONDARY, fg="white", pady=10, relief="flat",
                  command=self.analyze_diet).pack(fill="x", pady=15)

    def open_meal_logger(self, meal_name):
        if not self.generated_plan:
            messagebox.showinfo("Generate Plan First", "Please generate a diet plan in 'My Diet' tab first.")
            return

        # Prepare options
        main_opt = None
        subs = []
        
        if meal_name == "Snack":
            if "Snack (10am)" in self.generated_plan:
                subs.append(self.generated_plan["Snack (10am)"]['main'])
            if "Snack (4pm)" in self.generated_plan:
                subs.append(self.generated_plan["Snack (4pm)"]['main'])
            main_opt = subs[0] if subs else "Healthy Snack"
        else:
            if meal_name in self.generated_plan:
                d = self.generated_plan[meal_name]
                main_opt = d['main']
                subs = d.get('subs', [])

        # Popup
        top = tk.Toplevel(self)
        top.title(f"Log {meal_name}")
        top.geometry("380x450")
        top.configure(bg=self.BG)
        
        tk.Label(top, text=f"What did you have for {meal_name}?", 
                 font=("Segoe UI", 14, "bold"), bg=self.BG, fg=self.PRIMARY).pack(pady=20)
        
        def add_option_row(text, is_main=False):
            row = tk.Frame(top, bg=self.CARD, padx=15, pady=12)
            row.pack(fill="x", pady=5, padx=15)
            
            lbl = tk.Label(row, text=text, bg=self.CARD, font=("Segoe UI", 10), 
                           wraplength=240, justify="left")
            lbl.pack(side="left", fill="x", expand=True)
            
            def select():
                self.add_to_log(text, extra.get())
                top.destroy()
            
            tk.Button(row, text="SELECT", font=("Segoe UI", 9, "bold"), 
                      bg=self.PRIMARY, fg="white", relief="flat", padx=12,
                      command=select).pack(side="right")
        
        if main_opt:
            tk.Label(top, text="Recommended:", font=("Segoe UI", 10, "bold"), 
                     bg=self.BG, fg=self.TEXT_LIGHT).pack(anchor="w", padx=15)
            add_option_row(main_opt, True)
        
        if subs:
            tk.Label(top, text="Alternatives:", font=("Segoe UI", 10, "bold"), 
                     bg=self.BG, fg=self.TEXT_LIGHT).pack(anchor="w", padx=15, pady=(15, 0))
            for s in subs[:2]:
                add_option_row(s)
        
        tk.Label(top, text="Additional items:", font=("Segoe UI", 10), 
                 bg=self.BG).pack(anchor="w", padx=15, pady=(20, 5))
        extra = ttk.Entry(top)
        extra.pack(fill="x", padx=15, pady=5)
        
        def add_custom():
            if extra.get():
                self.add_to_log("Custom", extra.get())
                top.destroy()
        
        tk.Button(top, text="Add Custom Item Only", font=("Segoe UI", 10),
                  bg=self.CARD, fg=self.PRIMARY, relief="solid", bd=1,
                  command=add_custom).pack(pady=15)

    def add_to_log(self, main_item, extra):
        final = main_item
        if extra:
            if main_item == "Custom":
                final = extra
            else:
                final += f" + {extra}"
        
        if final and final != "Custom":
            self.today_log.append(final)
            self.update_log_display()

    def update_log_display(self):
        self.log_display.config(state="normal")
        self.log_display.delete("1.0", tk.END)
        for item in self.today_log:
            self.log_display.insert(tk.END, f"• {item}\n")
        self.log_display.config(state="disabled")

    def analyze_diet(self):
        if not self.today_log:
            messagebox.showinfo("Empty Log", "Please log some meals first.")
            return
        
        full_text = " ".join(self.today_log)
        cond = self.condition_var.get() if hasattr(self, 'condition_var') else "None"
        analysis, rec = analyze_intake(full_text, cond)
        
        top = tk.Toplevel(self)
        top.title("Diet Analysis")
        top.geometry("380x400")
        top.configure(bg=self.ACCENT)
        
        tk.Label(top, text="📊 Your Analysis", font=("Segoe UI", 16, "bold"), 
                 bg=self.ACCENT, fg=self.PRIMARY).pack(pady=20)
        
        tk.Label(top, text=analysis, font=("Segoe UI", 11), bg=self.ACCENT, 
                 justify="left").pack(pady=10, padx=20)
        
        tk.Label(top, text="💡 Recommendation", font=("Segoe UI", 13, "bold"), 
                 bg=self.ACCENT, fg=self.SECONDARY).pack(pady=(20, 10))
        
        tk.Label(top, text=rec, font=("Segoe UI", 11), bg=self.ACCENT, 
                 wraplength=340, justify="center").pack(pady=10, padx=20)
        
        self.local_manager.save_log(self.current_user_id, full_text, rec)

    def build_chat_tab(self):
        frame = ttk.Frame(self.tab_chat, padding=15)
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="💬 Nutrition Support", style="Header.TLabel").pack(pady=(0, 5))
        ttk.Label(frame, text="Get guidance from our nutrition team", 
                  foreground=self.TEXT_LIGHT).pack(pady=(0, 15))
        
        # Chat Area
        canvas = tk.Canvas(frame, bg=self.CARD, highlightthickness=0)
        ys = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        self.chat_inner = tk.Frame(canvas, bg=self.CARD)
        
        self.chat_inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.chat_inner, anchor="nw", width=370)
        canvas.configure(yscrollcommand=ys.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        ys.pack(side="right", fill="y")
        
        # Input
        input_frame = tk.Frame(frame, bg=self.BG)
        input_frame.pack(fill="x", pady=(15, 0))
        
        self.chat_input = ttk.Entry(input_frame, font=("Segoe UI", 11))
        self.chat_input.pack(side="left", fill="x", expand=True, ipady=8)
        
        tk.Button(input_frame, text="Send", font=("Segoe UI", 10, "bold"),
                  bg=self.PRIMARY, fg="white", relief="flat", padx=15,
                  command=self.send_message).pack(side="right", padx=(10, 0))

    def send_message(self):
        msg = self.chat_input.get().strip()
        if not msg:
            return
        
        self.add_chat_bubble(msg, "user")
        self.chat_input.delete(0, tk.END)
        
        self.after(500, lambda: self.add_chat_bubble(
            "Thank you for your message. A nutrition professional will respond shortly.", "system"))

    def add_chat_bubble(self, text, sender):
        bg = self.PRIMARY if sender == "user" else "#EEEEEE"
        fg = "white" if sender == "user" else self.TEXT
        side = "right" if sender == "user" else "left"
        
        bubble_frame = tk.Frame(self.chat_inner, bg=self.CARD)
        bubble_frame.pack(fill="x", pady=5)
        
        bubble = tk.Label(bubble_frame, text=text, bg=bg, fg=fg, 
                          font=("Segoe UI", 10), wraplength=250, justify="left",
                          padx=12, pady=8)
        bubble.pack(side=side, padx=10)

    def build_profile_tab(self):
        frame = ttk.Frame(self.tab_profile, padding=20)
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="👤 My Profile", style="Header.TLabel").pack(pady=(0, 20))
        
        # Profile Card
        card = tk.Frame(frame, bg=self.CARD, padx=20, pady=20)
        card.pack(fill="x")
        
        tk.Label(card, text="Age Bracket:", font=("Segoe UI", 10), bg=self.CARD, fg=self.TEXT_LIGHT).pack(anchor="w")
        tk.Label(card, text=MOH_AGE_BRACKETS.get(self.user_profile.get('age_bracket', '20-59y'), 'Adult'), 
                 font=("Segoe UI", 12, "bold"), bg=self.CARD, fg=self.TEXT).pack(anchor="w", pady=(0, 15))
        
        tk.Label(card, text="Current Status:", font=("Segoe UI", 10), bg=self.CARD, fg=self.TEXT_LIGHT).pack(anchor="w")
        tk.Label(card, text=self.user_profile.get('status', 'Not Assessed Yet'), 
                 font=("Segoe UI", 12, "bold"), bg=self.CARD, fg=self.PRIMARY).pack(anchor="w")
        
        # Sign Out
        tk.Button(frame, text="Sign Out", font=("Segoe UI", 11),
                  bg=self.CARD, fg=self.ERROR, relief="solid", bd=1, pady=10,
                  command=self.sign_out).pack(fill="x", pady=(30, 0))

    def sign_out(self):
        self.current_user_id = None
        self.user_profile = {}
        self.generated_plan = {}
        self.today_log = []
        self.show_welcome_screen()


if __name__ == "__main__":
    app = LisheBoraApp()
    app.mainloop()

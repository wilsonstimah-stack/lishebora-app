"""
LisheBora Mobile - Android Application
Built with Kivy for cross-platform mobile deployment
Kenya MOH-Aligned Nutrition Management System

To build for Android:
1. Install buildozer: pip install buildozer
2. Initialize: buildozer init
3. Build: buildozer android debug
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
import random

# Set window size for development (ignored on Android)
Window.size = (400, 700)

# ==================== THEME COLORS ====================
class Theme:
    PRIMARY = get_color_from_hex("#1B5E20")
    PRIMARY_LIGHT = get_color_from_hex("#4CAF50")
    SECONDARY = get_color_from_hex("#FF6D00")
    BG = get_color_from_hex("#FAFAFA")
    CARD = get_color_from_hex("#FFFFFF")
    TEXT = get_color_from_hex("#212121")
    TEXT_LIGHT = get_color_from_hex("#757575")
    ACCENT = get_color_from_hex("#E8F5E9")
    SUCCESS = get_color_from_hex("#388E3C")
    WARNING = get_color_from_hex("#FFA000")
    ERROR = get_color_from_hex("#D32F2F")

# ==================== DATA ====================
MOH_AGE_BRACKETS = [
    "0-6m", "6-23m", "2-5y", "5-9y", "10-14y", 
    "15-19y", "20-59y", "60+y", "pregnant", "lactating"
]

CONDITIONS = [
    "None", "Diabetes", "Hypertension", "Pregnancy", "Anemia", 
    "Gout", "Kidney Disease", "Ulcers", "Lactose Intolerance"
]

HEALTH_TIPS = [
    "Nutrition Fact: Avocado is rich in healthy fats that support heart health.",
    "Nutrition Fact: Drinking 8 glasses of water daily improves digestion.",
    "Nutrition Fact: Traditional vegetables like Managu are packed with Iron.",
    "Nutrition Fact: Reducing salt helps manage blood pressure effectively.",
    "Nutrition Fact: Sweet Potatoes (Ngwaci) are excellent for Vitamin A."
]

KENYAN_FOODS = {
    "starch": ["Ugali", "Chapati", "Rice", "Sweet Potatoes", "Arrowroots", "Matoke"],
    "protein": ["Beans", "Eggs", "Omena", "Chicken", "Beef", "Milk", "Fish"],
    "veg": ["Sukuma Wiki", "Spinach", "Managu", "Terere", "Cabbage"],
    "fruit": ["Mango", "Avocado", "Orange", "Banana", "Pawpaw"]
}

CONSENT_TEXT = """
INFORMED CONSENT FOR NUTRITION SERVICES

This application collects health information to provide personalized nutrition guidance aligned with Kenya Ministry of Health guidelines.

Your data will be:
• Used solely for nutrition assessment
• Kept confidential and protected
• Anonymized for research purposes

By proceeding, you confirm that you understand and consent to these terms.
"""

# ==================== CUSTOM WIDGETS ====================

class CardBox(BoxLayout):
    """White card with rounded corners"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(15)
        self.spacing = dp(10)
        with self.canvas.before:
            Color(*Theme.CARD)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class PrimaryButton(Button):
    """Green primary button"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = Theme.PRIMARY
        self.background_normal = ''
        self.color = (1, 1, 1, 1)
        self.font_size = sp(14)
        self.bold = True
        self.size_hint_y = None
        self.height = dp(50)

class SecondaryButton(Button):
    """Orange secondary button"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = Theme.SECONDARY
        self.background_normal = ''
        self.color = (1, 1, 1, 1)
        self.font_size = sp(14)
        self.bold = True
        self.size_hint_y = None
        self.height = dp(50)

class StyledInput(TextInput):
    """Styled text input"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.font_size = sp(14)
        self.padding = [dp(15), dp(12)]
        self.background_color = (0.95, 0.95, 0.95, 1)
        self.size_hint_y = None
        self.height = dp(50)

# ==================== SCREENS ====================

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))
        
        with layout.canvas.before:
            Color(*Theme.BG)
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self.update_bg, size=self.update_bg)
        self.layout = layout
        
        # Spacer
        layout.add_widget(BoxLayout(size_hint_y=0.2))
        
        # Logo
        logo_label = Label(
            text="🥗",
            font_size=sp(80),
            size_hint_y=None,
            height=dp(100)
        )
        layout.add_widget(logo_label)
        
        # Title
        title = Label(
            text="LisheBora",
            font_size=sp(32),
            bold=True,
            color=Theme.PRIMARY,
            size_hint_y=None,
            height=dp(50)
        )
        layout.add_widget(title)
        
        # Subtitle
        subtitle = Label(
            text="Your Nutrition Partner",
            font_size=sp(14),
            color=Theme.TEXT_LIGHT,
            size_hint_y=None,
            height=dp(30)
        )
        layout.add_widget(subtitle)
        
        # Spacer
        layout.add_widget(BoxLayout(size_hint_y=0.2))
        
        # Buttons
        sign_in_btn = PrimaryButton(text="Sign In")
        sign_in_btn.bind(on_press=self.go_to_login)
        layout.add_widget(sign_in_btn)
        
        create_btn = SecondaryButton(text="Create Account")
        create_btn.bind(on_press=self.go_to_register)
        layout.add_widget(create_btn)
        
        # Footer
        footer = Label(
            text="Kenya MOH Aligned",
            font_size=sp(10),
            color=Theme.TEXT_LIGHT,
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(footer)
        
        self.add_widget(layout)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.layout.pos
        self.bg_rect.size = self.layout.size
    
    def go_to_login(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'login'
    
    def go_to_register(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'register'


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=dp(25), spacing=dp(15))
        
        with layout.canvas.before:
            Color(*Theme.BG)
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self.update_bg, size=self.update_bg)
        self.layout = layout
        
        # Back Button
        back_btn = Button(
            text="← Back",
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            background_color=(0, 0, 0, 0),
            color=Theme.PRIMARY
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        # Title
        layout.add_widget(Label(
            text="Welcome Back",
            font_size=sp(24),
            bold=True,
            color=Theme.PRIMARY,
            size_hint_y=None,
            height=dp(50)
        ))
        
        layout.add_widget(BoxLayout(size_hint_y=0.1))
        
        # Form Card
        card = CardBox()
        
        card.add_widget(Label(
            text="Email or Phone",
            font_size=sp(12),
            color=Theme.TEXT_LIGHT,
            size_hint_y=None,
            height=dp(25),
            halign='left'
        ))
        
        self.email_input = StyledInput(hint_text="Enter your email")
        card.add_widget(self.email_input)
        
        card.add_widget(Label(
            text="Password",
            font_size=sp(12),
            color=Theme.TEXT_LIGHT,
            size_hint_y=None,
            height=dp(25),
            halign='left'
        ))
        
        self.password_input = StyledInput(hint_text="Enter password", password=True)
        card.add_widget(self.password_input)
        
        card.add_widget(BoxLayout(size_hint_y=None, height=dp(20)))
        
        login_btn = PrimaryButton(text="Sign In Securely")
        login_btn.bind(on_press=self.do_login)
        card.add_widget(login_btn)
        
        layout.add_widget(card)
        layout.add_widget(BoxLayout())  # Spacer
        
        self.add_widget(layout)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.layout.pos
        self.bg_rect.size = self.layout.size
    
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'welcome'
    
    def do_login(self, instance):
        # Simulate login
        email = self.email_input.text
        password = self.password_input.text
        
        if email and password:
            # Store user info in app
            app = App.get_running_app()
            app.current_user = {"email": email}
            
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'consent'
        else:
            self.show_error("Please enter credentials")
    
    def show_error(self, message):
        popup = Popup(
            title="Error",
            content=Label(text=message),
            size_hint=(0.8, 0.3)
        )
        popup.open()


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', padding=dp(25), spacing=dp(10), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        with layout.canvas.before:
            Color(*Theme.BG)
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self.update_bg, size=self.update_bg)
        self.layout = layout
        
        # Back Button
        back_btn = Button(
            text="← Back",
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            background_color=(0, 0, 0, 0),
            color=Theme.PRIMARY
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        # Title
        layout.add_widget(Label(
            text="Create Account",
            font_size=sp(24),
            bold=True,
            color=Theme.PRIMARY,
            size_hint_y=None,
            height=dp(50)
        ))
        
        # Form
        card = CardBox()
        
        fields = [
            ("Full Name", "name"),
            ("Email", "email"),
            ("Phone", "phone"),
            ("Date of Birth (YYYY-MM-DD)", "dob")
        ]
        
        self.inputs = {}
        
        for label_text, field_name in fields:
            card.add_widget(Label(
                text=label_text,
                font_size=sp(12),
                color=Theme.TEXT_LIGHT,
                size_hint_y=None,
                height=dp(25),
                halign='left'
            ))
            inp = StyledInput()
            self.inputs[field_name] = inp
            card.add_widget(inp)
        
        # Gender
        card.add_widget(Label(
            text="Gender",
            font_size=sp(12),
            color=Theme.TEXT_LIGHT,
            size_hint_y=None,
            height=dp(25)
        ))
        self.gender_spinner = Spinner(
            text="Select Gender",
            values=["Female", "Male"],
            size_hint_y=None,
            height=dp(50)
        )
        card.add_widget(self.gender_spinner)
        
        # Password
        card.add_widget(Label(
            text="Password",
            font_size=sp(12),
            color=Theme.TEXT_LIGHT,
            size_hint_y=None,
            height=dp(25)
        ))
        self.password_input = StyledInput(password=True)
        card.add_widget(self.password_input)
        
        card.add_widget(BoxLayout(size_hint_y=None, height=dp(15)))
        
        register_btn = PrimaryButton(text="Create Account")
        register_btn.bind(on_press=self.do_register)
        card.add_widget(register_btn)
        
        layout.add_widget(card)
        layout.add_widget(BoxLayout(size_hint_y=None, height=dp(50)))
        
        scroll.add_widget(layout)
        self.add_widget(scroll)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.layout.pos
        self.bg_rect.size = self.layout.size
    
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'welcome'
    
    def do_register(self, instance):
        # Simulate registration
        app = App.get_running_app()
        app.current_user = {"email": self.inputs['email'].text}
        
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'consent'


class ConsentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        with layout.canvas.before:
            Color(*Theme.BG)
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self.update_bg, size=self.update_bg)
        self.layout = layout
        
        # Icon
        layout.add_widget(Label(
            text="📋",
            font_size=sp(50),
            size_hint_y=None,
            height=dp(70)
        ))
        
        # Title
        layout.add_widget(Label(
            text="Informed Consent",
            font_size=sp(20),
            bold=True,
            color=Theme.PRIMARY,
            size_hint_y=None,
            height=dp(40)
        ))
        
        # Consent Text Card
        scroll = ScrollView(size_hint_y=0.5)
        card = CardBox()
        consent_label = Label(
            text=CONSENT_TEXT,
            font_size=sp(12),
            color=Theme.TEXT,
            size_hint_y=None,
            text_size=(dp(320), None),
            halign='left',
            valign='top'
        )
        consent_label.bind(texture_size=consent_label.setter('size'))
        card.add_widget(consent_label)
        scroll.add_widget(card)
        layout.add_widget(scroll)
        
        # Checkbox
        check_layout = BoxLayout(size_hint_y=None, height=dp(50))
        self.consent_check = CheckBox(size_hint_x=None, width=dp(50))
        self.consent_check.bind(active=self.on_check)
        check_layout.add_widget(self.consent_check)
        check_layout.add_widget(Label(
            text="I agree to the terms above",
            font_size=sp(12),
            color=Theme.TEXT
        ))
        layout.add_widget(check_layout)
        
        # Continue Button
        self.continue_btn = PrimaryButton(text="Continue", disabled=True)
        self.continue_btn.bind(on_press=self.go_to_home)
        layout.add_widget(self.continue_btn)
        
        self.add_widget(layout)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.layout.pos
        self.bg_rect.size = self.layout.size
    
    def on_check(self, checkbox, value):
        self.continue_btn.disabled = not value
    
    def go_to_home(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'home'


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical')
        
        with main_layout.canvas.before:
            Color(*Theme.BG)
            self.bg_rect = Rectangle(pos=main_layout.pos, size=main_layout.size)
        main_layout.bind(pos=self.update_bg, size=self.update_bg)
        self.main_layout = main_layout
        
        # Content Area
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # Health Tip Banner
        tip = random.choice(HEALTH_TIPS)
        tip_card = CardBox()
        tip_card.size_hint_y = None
        tip_card.height = dp(100)
        
        with tip_card.canvas.before:
            Color(*Theme.ACCENT)
        
        tip_card.add_widget(Label(
            text="🌿 " + tip,
            font_size=sp(12),
            color=Theme.PRIMARY,
            text_size=(dp(320), None),
            halign='left'
        ))
        content.add_widget(tip_card)
        
        # Assessment Card
        assess_card = CardBox()
        assess_card.size_hint_y = None
        assess_card.height = dp(350)
        
        assess_card.add_widget(Label(
            text="📊 Health Assessment",
            font_size=sp(16),
            bold=True,
            color=Theme.PRIMARY,
            size_hint_y=None,
            height=dp(40)
        ))
        
        # Weight
        row1 = BoxLayout(size_hint_y=None, height=dp(50))
        row1.add_widget(Label(text="Weight (kg):", font_size=sp(12), color=Theme.TEXT))
        self.weight_input = StyledInput(hint_text="e.g. 65")
        row1.add_widget(self.weight_input)
        assess_card.add_widget(row1)
        
        # Height
        row2 = BoxLayout(size_hint_y=None, height=dp(50))
        row2.add_widget(Label(text="Height (cm):", font_size=sp(12), color=Theme.TEXT))
        self.height_input = StyledInput(hint_text="e.g. 170")
        row2.add_widget(self.height_input)
        assess_card.add_widget(row2)
        
        # MUAC
        row3 = BoxLayout(size_hint_y=None, height=dp(50))
        row3.add_widget(Label(text="MUAC (mm):", font_size=sp(12), color=Theme.TEXT))
        self.muac_input = StyledInput(hint_text="e.g. 250")
        row3.add_widget(self.muac_input)
        assess_card.add_widget(row3)
        
        # Status Display
        self.status_label = Label(
            text="Complete assessment to view status",
            font_size=sp(12),
            color=Theme.TEXT_LIGHT,
            size_hint_y=None,
            height=dp(40)
        )
        assess_card.add_widget(self.status_label)
        
        # Calculate Button
        calc_btn = PrimaryButton(text="✓ Calculate Status")
        calc_btn.bind(on_press=self.calculate_status)
        assess_card.add_widget(calc_btn)
        
        content.add_widget(assess_card)
        
        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        
        # Bottom Navigation
        nav = BoxLayout(size_hint_y=None, height=dp(60))
        with nav.canvas.before:
            Color(*Theme.CARD)
            self.nav_rect = Rectangle(pos=nav.pos, size=nav.size)
        nav.bind(pos=self.update_nav, size=self.update_nav)
        
        nav_items = [
            ("🏠", "home"),
            ("🥗", "diet"),
            ("📝", "log"),
            ("💬", "chat")
        ]
        
        for icon, screen in nav_items:
            btn = Button(
                text=icon,
                font_size=sp(24),
                background_color=(0, 0, 0, 0),
                color=Theme.PRIMARY if screen == "home" else Theme.TEXT_LIGHT
            )
            btn.bind(on_press=lambda x, s=screen: self.navigate(s))
            nav.add_widget(btn)
        
        main_layout.add_widget(nav)
        self.add_widget(main_layout)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.main_layout.pos
        self.bg_rect.size = self.main_layout.size
    
    def update_nav(self, *args):
        pass
    
    def calculate_status(self, instance):
        try:
            weight = float(self.weight_input.text)
            height = float(self.height_input.text)
            bmi = round(weight / ((height/100) ** 2), 1)
            
            if bmi < 18.5:
                status = "Underweight"
            elif bmi < 25:
                status = "Normal"
            elif bmi < 30:
                status = "Overweight"
            else:
                status = "Obese"
            
            self.status_label.text = f"BMI: {bmi} | Status: {status}"
            self.status_label.color = Theme.SUCCESS if status == "Normal" else Theme.WARNING
            
            # Store in app
            app = App.get_running_app()
            app.user_status = status
            
        except:
            self.status_label.text = "Please enter valid numbers"
            self.status_label.color = Theme.ERROR
    
    def navigate(self, screen):
        if screen != "home":
            self.manager.current = screen


class DietScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical')
        
        with main_layout.canvas.before:
            Color(*Theme.BG)
            self.bg_rect = Rectangle(pos=main_layout.pos, size=main_layout.size)
        main_layout.bind(pos=self.update_bg, size=self.update_bg)
        self.main_layout = main_layout
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(60), padding=dp(15))
        header.add_widget(Label(
            text="🥗 My Diet Plan",
            font_size=sp(18),
            bold=True,
            color=Theme.PRIMARY
        ))
        main_layout.add_widget(header)
        
        # Generate Button
        gen_btn = PrimaryButton(text="Generate My Plan")
        gen_btn.size_hint_x = 0.9
        gen_btn.pos_hint = {'center_x': 0.5}
        gen_btn.bind(on_press=self.generate_plan)
        main_layout.add_widget(gen_btn)
        
        # Plan Display
        self.scroll = ScrollView()
        self.plan_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15), size_hint_y=None)
        self.plan_layout.bind(minimum_height=self.plan_layout.setter('height'))
        
        self.plan_layout.add_widget(Label(
            text="Tap 'Generate' to create your plan",
            font_size=sp(12),
            color=Theme.TEXT_LIGHT,
            size_hint_y=None,
            height=dp(50)
        ))
        
        self.scroll.add_widget(self.plan_layout)
        main_layout.add_widget(self.scroll)
        
        # Bottom Nav
        nav = self.create_nav("diet")
        main_layout.add_widget(nav)
        
        self.add_widget(main_layout)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.main_layout.pos
        self.bg_rect.size = self.main_layout.size
    
    def create_nav(self, current):
        nav = BoxLayout(size_hint_y=None, height=dp(60))
        with nav.canvas.before:
            Color(*Theme.CARD)
            Rectangle(pos=nav.pos, size=nav.size)
        
        for icon, screen in [("🏠", "home"), ("🥗", "diet"), ("📝", "log"), ("💬", "chat")]:
            btn = Button(
                text=icon,
                font_size=sp(24),
                background_color=(0, 0, 0, 0),
                color=Theme.PRIMARY if screen == current else Theme.TEXT_LIGHT
            )
            btn.bind(on_press=lambda x, s=screen: self.navigate(s))
            nav.add_widget(btn)
        return nav
    
    def navigate(self, screen):
        self.manager.current = screen
    
    def generate_plan(self, instance):
        self.plan_layout.clear_widgets()
        
        meals = [
            ("☕ Breakfast", "Energy Start"),
            ("🍎 Snack (10am)", "Vitamin Boost"),
            ("🍛 Lunch", "Balanced Meal"),
            ("🥤 Snack (4pm)", "Sustain Energy"),
            ("🍲 Supper", "Recovery")
        ]
        
        for meal_name, goal in meals:
            card = CardBox()
            card.size_hint_y = None
            card.height = dp(100)
            
            # Header
            card.add_widget(Label(
                text=meal_name,
                font_size=sp(14),
                bold=True,
                color=Theme.PRIMARY,
                size_hint_y=None,
                height=dp(25),
                halign='left'
            ))
            
            # Random meal
            starch = random.choice(KENYAN_FOODS['starch'])
            protein = random.choice(KENYAN_FOODS['protein'])
            veg = random.choice(KENYAN_FOODS['veg'])
            
            card.add_widget(Label(
                text=f"{starch} + {protein} + {veg}",
                font_size=sp(12),
                color=Theme.TEXT,
                size_hint_y=None,
                height=dp(25)
            ))
            
            card.add_widget(Label(
                text=f"Goal: {goal}",
                font_size=sp(10),
                color=Theme.TEXT_LIGHT,
                size_hint_y=None,
                height=dp(20)
            ))
            
            self.plan_layout.add_widget(card)


class LogScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical')
        
        with main_layout.canvas.before:
            Color(*Theme.BG)
            self.bg_rect = Rectangle()
        main_layout.bind(pos=self.update_bg, size=self.update_bg)
        self.main_layout = main_layout
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(60), padding=dp(15))
        header.add_widget(Label(
            text="📝 Food Diary",
            font_size=sp(18),
            bold=True,
            color=Theme.PRIMARY
        ))
        main_layout.add_widget(header)
        
        # Meal Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), padding=dp(10), spacing=dp(5))
        for meal in ["Breakfast", "Lunch", "Supper"]:
            btn = Button(
                text=meal,
                font_size=sp(11),
                background_color=Theme.CARD,
                color=Theme.PRIMARY
            )
            btn_layout.add_widget(btn)
        main_layout.add_widget(btn_layout)
        
        # Log Display
        card = CardBox()
        card.add_widget(Label(
            text="Your logged meals will appear here",
            font_size=sp(12),
            color=Theme.TEXT_LIGHT
        ))
        main_layout.add_widget(card)
        
        # Analyze Button
        analyze_btn = SecondaryButton(text="📊 Analyze My Diet")
        analyze_btn.size_hint_x = 0.9
        analyze_btn.pos_hint = {'center_x': 0.5}
        main_layout.add_widget(analyze_btn)
        
        main_layout.add_widget(BoxLayout())  # Spacer
        
        # Nav
        nav = self.create_nav("log")
        main_layout.add_widget(nav)
        
        self.add_widget(main_layout)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.main_layout.pos
        self.bg_rect.size = self.main_layout.size
    
    def create_nav(self, current):
        nav = BoxLayout(size_hint_y=None, height=dp(60))
        with nav.canvas.before:
            Color(*Theme.CARD)
            Rectangle(pos=nav.pos, size=nav.size)
        
        for icon, screen in [("🏠", "home"), ("🥗", "diet"), ("📝", "log"), ("💬", "chat")]:
            btn = Button(
                text=icon,
                font_size=sp(24),
                background_color=(0, 0, 0, 0),
                color=Theme.PRIMARY if screen == current else Theme.TEXT_LIGHT
            )
            btn.bind(on_press=lambda x, s=screen: self.navigate(s))
            nav.add_widget(btn)
        return nav
    
    def navigate(self, screen):
        self.manager.current = screen


class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical')
        
        with main_layout.canvas.before:
            Color(*Theme.BG)
            self.bg_rect = Rectangle()
        main_layout.bind(pos=self.update_bg, size=self.update_bg)
        self.main_layout = main_layout
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(60), padding=dp(15))
        header.add_widget(Label(
            text="💬 Nutrition Support",
            font_size=sp(18),
            bold=True,
            color=Theme.PRIMARY
        ))
        main_layout.add_widget(header)
        
        # Chat Area
        self.chat_scroll = ScrollView()
        self.chat_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15), size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.chat_scroll.add_widget(self.chat_layout)
        main_layout.add_widget(self.chat_scroll)
        
        # Input Area
        input_layout = BoxLayout(size_hint_y=None, height=dp(60), padding=dp(10), spacing=dp(10))
        with input_layout.canvas.before:
            Color(*Theme.CARD)
            Rectangle(pos=input_layout.pos, size=input_layout.size)
        
        self.chat_input = StyledInput(hint_text="Type a message...")
        input_layout.add_widget(self.chat_input)
        
        send_btn = PrimaryButton(text="Send")
        send_btn.size_hint_x = None
        send_btn.width = dp(80)
        send_btn.bind(on_press=self.send_message)
        input_layout.add_widget(send_btn)
        
        main_layout.add_widget(input_layout)
        
        # Nav
        nav = self.create_nav("chat")
        main_layout.add_widget(nav)
        
        self.add_widget(main_layout)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.main_layout.pos
        self.bg_rect.size = self.main_layout.size
    
    def create_nav(self, current):
        nav = BoxLayout(size_hint_y=None, height=dp(60))
        with nav.canvas.before:
            Color(*Theme.CARD)
            Rectangle(pos=nav.pos, size=nav.size)
        
        for icon, screen in [("🏠", "home"), ("🥗", "diet"), ("📝", "log"), ("💬", "chat")]:
            btn = Button(
                text=icon,
                font_size=sp(24),
                background_color=(0, 0, 0, 0),
                color=Theme.PRIMARY if screen == current else Theme.TEXT_LIGHT
            )
            btn.bind(on_press=lambda x, s=screen: self.navigate(s))
            nav.add_widget(btn)
        return nav
    
    def navigate(self, screen):
        self.manager.current = screen
    
    def send_message(self, instance):
        msg = self.chat_input.text.strip()
        if not msg:
            return
        
        # User message
        user_bubble = Label(
            text=msg,
            font_size=sp(12),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(40),
            halign='right'
        )
        with user_bubble.canvas.before:
            Color(*Theme.PRIMARY)
            RoundedRectangle(pos=user_bubble.pos, size=user_bubble.size, radius=[dp(10)])
        
        self.chat_layout.add_widget(user_bubble)
        self.chat_input.text = ""
        
        # Auto response
        Clock.schedule_once(lambda dt: self.add_response(), 0.5)
    
    def add_response(self):
        response = Label(
            text="Thank you! A nutritionist will respond shortly.",
            font_size=sp(12),
            color=Theme.TEXT,
            size_hint_y=None,
            height=dp(40)
        )
        self.chat_layout.add_widget(response)


# ==================== MAIN APP ====================

class LisheBoraApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = None
        self.user_status = None
    
    def build(self):
        self.title = "LisheBora"
        
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(ConsentScreen(name='consent'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(DietScreen(name='diet'))
        sm.add_widget(LogScreen(name='log'))
        sm.add_widget(ChatScreen(name='chat'))
        
        return sm


if __name__ == '__main__':
    LisheBoraApp().run()

"""
LishePro Mobile - Professional Nutrition Portal
Android Application for Nutritionists
Built with Kivy for cross-platform mobile deployment
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

# Set window size for development
Window.size = (400, 700)

# ==================== THEME ====================
class Theme:
    PRIMARY = get_color_from_hex("#1A237E")
    PRIMARY_LIGHT = get_color_from_hex("#3949AB")
    SECONDARY = get_color_from_hex("#00897B")
    ACCENT = get_color_from_hex("#304FFE")
    BG = get_color_from_hex("#F0F2F5")
    SIDEBAR = get_color_from_hex("#1A237E")
    CARD = get_color_from_hex("#FFFFFF")
    TEXT = get_color_from_hex("#212121")
    TEXT_LIGHT = get_color_from_hex("#757575")
    SUCCESS = get_color_from_hex("#43A047")
    WARNING = get_color_from_hex("#FB8C00")
    ERROR = get_color_from_hex("#E53935")

# ==================== CUSTOM WIDGETS ====================

class CardBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(15)
        self.spacing = dp(10)
        with self.canvas.before:
            Color(*Theme.CARD)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class PrimaryButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = Theme.PRIMARY
        self.background_normal = ''
        self.color = (1, 1, 1, 1)
        self.font_size = sp(14)
        self.bold = True
        self.size_hint_y = None
        self.height = dp(50)

class StyledInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.font_size = sp(14)
        self.padding = [dp(15), dp(12)]
        self.background_color = (0.95, 0.95, 0.95, 1)
        self.size_hint_y = None
        self.height = dp(50)

# ==================== SCREENS ====================

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))
        
        with layout.canvas.before:
            Color(*Theme.BG)
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self.update_bg, size=self.update_bg)
        self.layout = layout
        
        # Spacer
        layout.add_widget(BoxLayout(size_hint_y=0.15))
        
        # Logo
        layout.add_widget(Label(
            text="🩺",
            font_size=sp(64),
            size_hint_y=None,
            height=dp(80)
        ))
        
        layout.add_widget(Label(
            text="LishePro",
            font_size=sp(28),
            bold=True,
            color=Theme.PRIMARY,
            size_hint_y=None,
            height=dp(40)
        ))
        
        layout.add_widget(Label(
            text="Professional Nutrition Portal",
            font_size=sp(12),
            color=Theme.TEXT_LIGHT,
            size_hint_y=None,
            height=dp(30)
        ))
        
        layout.add_widget(BoxLayout(size_hint_y=0.1))
        
        # Login Card
        card = CardBox()
        
        card.add_widget(Label(
            text="Email",
            font_size=sp(11),
            color=Theme.TEXT_LIGHT,
            size_hint_y=None,
            height=dp(25),
            halign='left'
        ))
        
        self.email_input = StyledInput(hint_text="Enter email")
        card.add_widget(self.email_input)
        
        card.add_widget(Label(
            text="Password",
            font_size=sp(11),
            color=Theme.TEXT_LIGHT,
            size_hint_y=None,
            height=dp(25)
        ))
        
        self.password_input = StyledInput(hint_text="Enter password", password=True)
        card.add_widget(self.password_input)
        
        card.add_widget(BoxLayout(size_hint_y=None, height=dp(15)))
        
        login_btn = PrimaryButton(text="Sign In")
        login_btn.bind(on_press=self.do_login)
        card.add_widget(login_btn)
        
        layout.add_widget(card)
        layout.add_widget(BoxLayout())  # Spacer
        
        self.add_widget(layout)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.layout.pos
        self.bg_rect.size = self.layout.size
    
    def do_login(self, instance):
        email = self.email_input.text
        password = self.password_input.text
        
        if email and password:
            app = App.get_running_app()
            app.current_user = {"email": email}
            self.manager.current = 'dashboard'
        else:
            popup = Popup(
                title="Error",
                content=Label(text="Please enter credentials"),
                size_hint=(0.8, 0.3)
            )
            popup.open()


class DashboardScreen(Screen):
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
        with header.canvas.before:
            Color(*Theme.PRIMARY)
            Rectangle(pos=header.pos, size=header.size)
        
        header.add_widget(Label(
            text="🩺 LishePro Dashboard",
            font_size=sp(16),
            bold=True,
            color=(1, 1, 1, 1)
        ))
        main_layout.add_widget(header)
        
        # Content
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # Stats Grid
        stats_box = BoxLayout(size_hint_y=None, height=dp(120), spacing=dp(10))
        
        stats = [
            ("👥", "Users", "45"),
            ("❓", "Pending", "3"),
            ("🥗", "Plans", "128")
        ]
        
        for icon, label, value in stats:
            card = CardBox()
            card.add_widget(Label(text=icon, font_size=sp(28), size_hint_y=None, height=dp(40)))
            card.add_widget(Label(text=value, font_size=sp(24), bold=True, color=Theme.PRIMARY, size_hint_y=None, height=dp(30)))
            card.add_widget(Label(text=label, font_size=sp(10), color=Theme.TEXT_LIGHT, size_hint_y=None, height=dp(20)))
            stats_box.add_widget(card)
        
        content.add_widget(stats_box)
        
        # Recent Activity
        activity_card = CardBox()
        activity_card.size_hint_y = None
        activity_card.height = dp(200)
        
        activity_card.add_widget(Label(
            text="📋 Recent Activity",
            font_size=sp(14),
            bold=True,
            color=Theme.PRIMARY,
            size_hint_y=None,
            height=dp(35)
        ))
        
        activities = [
            "New user registered - 5 min ago",
            "Diet plan generated - 15 min ago",
            "Question answered - 1 hour ago"
        ]
        
        for activity in activities:
            activity_card.add_widget(Label(
                text="• " + activity,
                font_size=sp(11),
                color=Theme.TEXT,
                size_hint_y=None,
                height=dp(30),
                halign='left'
            ))
        
        content.add_widget(activity_card)
        
        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        
        # Bottom Navigation
        nav = BoxLayout(size_hint_y=None, height=dp(60))
        with nav.canvas.before:
            Color(*Theme.CARD)
            Rectangle(pos=nav.pos, size=nav.size)
        
        nav_items = [
            ("📊", "dashboard"),
            ("👥", "users"),
            ("❓", "questions"),
            ("⚙️", "settings")
        ]
        
        for icon, screen in nav_items:
            btn = Button(
                text=icon,
                font_size=sp(22),
                background_color=(0, 0, 0, 0),
                color=Theme.PRIMARY if screen == "dashboard" else Theme.TEXT_LIGHT
            )
            btn.bind(on_press=lambda x, s=screen: self.navigate(s))
            nav.add_widget(btn)
        
        main_layout.add_widget(nav)
        self.add_widget(main_layout)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.main_layout.pos
        self.bg_rect.size = self.main_layout.size
    
    def navigate(self, screen):
        if screen != "dashboard":
            self.manager.current = screen


class UsersScreen(Screen):
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
        with header.canvas.before:
            Color(*Theme.PRIMARY)
            Rectangle(pos=header.pos, size=header.size)
        
        header.add_widget(Label(
            text="👥 User Management",
            font_size=sp(16),
            bold=True,
            color=(1, 1, 1, 1)
        ))
        main_layout.add_widget(header)
        
        # Search
        search_layout = BoxLayout(size_hint_y=None, height=dp(60), padding=dp(10), spacing=dp(10))
        search_input = StyledInput(hint_text="Search users...")
        search_layout.add_widget(search_input)
        main_layout.add_widget(search_layout)
        
        # User List
        scroll = ScrollView()
        users_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10), size_hint_y=None)
        users_layout.bind(minimum_height=users_layout.setter('height'))
        
        sample_users = [
            ("jane@example.com", "Adult", "Normal"),
            ("john@example.com", "Elderly", "Overweight"),
            ("mary@example.com", "Pregnant", "Underweight")
        ]
        
        for email, age, status in sample_users:
            card = CardBox()
            card.size_hint_y = None
            card.height = dp(80)
            
            info_layout = BoxLayout()
            
            left = BoxLayout(orientation='vertical')
            left.add_widget(Label(text=email, font_size=sp(12), bold=True, color=Theme.TEXT, halign='left'))
            left.add_widget(Label(text=f"{age} | {status}", font_size=sp(10), color=Theme.TEXT_LIGHT, halign='left'))
            info_layout.add_widget(left)
            
            view_btn = Button(
                text="View",
                size_hint=(None, None),
                size=(dp(60), dp(35)),
                background_color=Theme.ACCENT,
                color=(1, 1, 1, 1),
                font_size=sp(11)
            )
            info_layout.add_widget(view_btn)
            
            card.add_widget(info_layout)
            users_layout.add_widget(card)
        
        scroll.add_widget(users_layout)
        main_layout.add_widget(scroll)
        
        # Navigation
        nav = self.create_nav("users")
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
        
        for icon, screen in [("📊", "dashboard"), ("👥", "users"), ("❓", "questions"), ("⚙️", "settings")]:
            btn = Button(
                text=icon,
                font_size=sp(22),
                background_color=(0, 0, 0, 0),
                color=Theme.PRIMARY if screen == current else Theme.TEXT_LIGHT
            )
            btn.bind(on_press=lambda x, s=screen: self.navigate(s))
            nav.add_widget(btn)
        return nav
    
    def navigate(self, screen):
        self.manager.current = screen


class QuestionsScreen(Screen):
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
        with header.canvas.before:
            Color(*Theme.PRIMARY)
            Rectangle(pos=header.pos, size=header.size)
        
        header.add_widget(Label(
            text="❓ User Questions",
            font_size=sp(16),
            bold=True,
            color=(1, 1, 1, 1)
        ))
        main_layout.add_widget(header)
        
        # Questions List
        scroll = ScrollView()
        questions_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15), size_hint_y=None)
        questions_layout.bind(minimum_height=questions_layout.setter('height'))
        
        sample_questions = [
            ("User #12", "What foods are good for diabetes?"),
            ("User #8", "How can I gain weight healthily?"),
            ("User #15", "Is ugali good for pregnant women?")
        ]
        
        for user, question in sample_questions:
            card = CardBox()
            card.size_hint_y = None
            card.height = dp(150)
            
            card.add_widget(Label(
                text=f"👤 {user}",
                font_size=sp(11),
                bold=True,
                color=Theme.PRIMARY,
                size_hint_y=None,
                height=dp(25),
                halign='left'
            ))
            
            card.add_widget(Label(
                text=question,
                font_size=sp(12),
                color=Theme.TEXT,
                size_hint_y=None,
                height=dp(30),
                halign='left'
            ))
            
            response_layout = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(10))
            response_input = StyledInput(hint_text="Type response...")
            response_layout.add_widget(response_input)
            
            send_btn = Button(
                text="Send",
                size_hint_x=None,
                width=dp(60),
                background_color=Theme.SECONDARY,
                color=(1, 1, 1, 1),
                font_size=sp(11)
            )
            response_layout.add_widget(send_btn)
            
            card.add_widget(response_layout)
            questions_layout.add_widget(card)
        
        scroll.add_widget(questions_layout)
        main_layout.add_widget(scroll)
        
        # Navigation
        nav = self.create_nav("questions")
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
        
        for icon, screen in [("📊", "dashboard"), ("👥", "users"), ("❓", "questions"), ("⚙️", "settings")]:
            btn = Button(
                text=icon,
                font_size=sp(22),
                background_color=(0, 0, 0, 0),
                color=Theme.PRIMARY if screen == current else Theme.TEXT_LIGHT
            )
            btn.bind(on_press=lambda x, s=screen: self.navigate(s))
            nav.add_widget(btn)
        return nav
    
    def navigate(self, screen):
        self.manager.current = screen


class SettingsScreen(Screen):
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
        with header.canvas.before:
            Color(*Theme.PRIMARY)
            Rectangle(pos=header.pos, size=header.size)
        
        header.add_widget(Label(
            text="⚙️ Settings",
            font_size=sp(16),
            bold=True,
            color=(1, 1, 1, 1)
        ))
        main_layout.add_widget(header)
        
        # Settings Content
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Account Card
        card = CardBox()
        card.size_hint_y = None
        card.height = dp(200)
        
        card.add_widget(Label(
            text="Account Settings",
            font_size=sp(14),
            bold=True,
            color=Theme.PRIMARY,
            size_hint_y=None,
            height=dp(35)
        ))
        
        card.add_widget(Label(text="Email", font_size=sp(10), color=Theme.TEXT_LIGHT, size_hint_y=None, height=dp(20), halign='left'))
        card.add_widget(StyledInput(hint_text="your@email.com"))
        
        card.add_widget(Label(text="New Password", font_size=sp(10), color=Theme.TEXT_LIGHT, size_hint_y=None, height=dp(20), halign='left'))
        card.add_widget(StyledInput(hint_text="Leave blank to keep", password=True))
        
        content.add_widget(card)
        
        # Sign Out
        signout_btn = Button(
            text="Sign Out",
            size_hint_y=None,
            height=dp(50),
            background_color=Theme.ERROR,
            color=(1, 1, 1, 1),
            font_size=sp(14)
        )
        signout_btn.bind(on_press=self.sign_out)
        content.add_widget(signout_btn)
        
        content.add_widget(BoxLayout())  # Spacer
        
        main_layout.add_widget(content)
        
        # Navigation
        nav = self.create_nav("settings")
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
        
        for icon, screen in [("📊", "dashboard"), ("👥", "users"), ("❓", "questions"), ("⚙️", "settings")]:
            btn = Button(
                text=icon,
                font_size=sp(22),
                background_color=(0, 0, 0, 0),
                color=Theme.PRIMARY if screen == current else Theme.TEXT_LIGHT
            )
            btn.bind(on_press=lambda x, s=screen: self.navigate(s))
            nav.add_widget(btn)
        return nav
    
    def navigate(self, screen):
        self.manager.current = screen
    
    def sign_out(self, instance):
        self.manager.current = 'login'


# ==================== MAIN APP ====================

class LisheProApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = None
    
    def build(self):
        self.title = "LishePro"
        
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(UsersScreen(name='users'))
        sm.add_widget(QuestionsScreen(name='questions'))
        sm.add_widget(SettingsScreen(name='settings'))
        
        return sm


if __name__ == '__main__':
    LisheProApp().run()

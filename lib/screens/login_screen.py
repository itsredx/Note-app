# ── Imports ───────────────────────────────────────────────────────────
from typing import Optional

from pythra import (
    StatefulWidget,
    State,
    Column,
    Row,
    Key,
    Widget,
    Container,
    BoxDecoration,
    BorderSide,
    Text,
    Alignment,
    Colors,
    Center,
    ElevatedButton,
    SizedBox,
    MainAxisAlignment,
    CrossAxisAlignment,
    EdgeInsets,
    Icon,
    IconButton,
    Icons,
    ButtonStyle,
    BorderRadius,
    TextStyle,
    Image,
    AssetImage,
    ImageFit,
    PageRoute,
    NavigatorState,
    GestureDetector,
    Padding,
    TextField,
    TextEditingController,
    InputDecoration,
    Expanded,
    SingleChildScrollView,
)

try:
    from lib.utils.shared_prefernce import PythraPreferences
except ImportError:
    from utils.shared_prefernce import PythraPreferences


# ── Screen Widget ─────────────────────────────────────────────────────
class LoginScreen(StatefulWidget):
    """
    Modern authentication screen presenting a split two-pane layout:
    - Left: Welcome typography, credentials input, social authentication, and registration link.
    - Right: Soft sage-tinted hero showcase with meditation/productivity illustration,
            carousel pagination, and value proposition headline.
    """

    def __init__(
        self,
        key: Key,
        navigator: NavigatorState,
    ):
        self.navigator = navigator
        super().__init__(key=key)

    def createState(self):
        return LoginScreenState(self.navigator)


# ── State Implementation ──────────────────────────────────────────────
class LoginScreenState(State):
    def __init__(self, navigator: NavigatorState):
        super().__init__()
        self.navigator = navigator
        self.pref = PythraPreferences()

        # Input controllers
        self.username_controller = TextEditingController()
        self.password_controller = TextEditingController()

        # UI state
        self.show_password = False
        self.active_slide = 1  # 0, 1 (active in design), 2
        self.error_message: Optional[str] = None
        self.success_message: Optional[str] = None
        self.is_register_mode = False

        # Carousel slides data
        self.slides = [
            {
                "title": "Stay focused and mindful throughout your day",
                "brand": "with Note App",
            },
            {
                "title": "Make your work easier and organized",
                "brand": "with Note App",
            },
            {
                "title": "Capture ideas and notes at lightning speed",
                "brand": "with Note App",
            },
        ]

    # ── Event Handlers ────────────────────────────────────────────────
    def _toggle_password_visibility(self):
        self.show_password = not self.show_password
        self.setState()

    def _set_active_slide(self, index: int):
        self.active_slide = index
        self.setState()

    def _handle_login(self):
        username = (
            self.username_controller.text.strip()
            if hasattr(self.username_controller, "text")
            else ""
        )
        password = (
            self.password_controller.text.strip()
            if hasattr(self.password_controller, "text")
            else ""
        )

        if self.is_register_mode:
            if not username:
                self.error_message = "Please enter your username"
                self.success_message = None
                self.setState()
                return
            if not password:
                self.error_message = "Please enter your password"
                self.success_message = None
                self.setState()
                return

        # Sensible fallback for instant login if left blank
        username = username or "Ahmad"
        password = password or "password"

        print(f"🔑 [LoginScreen] Logging in as '{username}'...")
        self.pref.set("is_logged_in", True)
        self.pref.set("username", username)

        try:
            from screens.dashboard_screen import DashboardScreen
        except ImportError:
            from lib.screens.dashboard_screen import DashboardScreen

        dashboard_route = PageRoute(
            builder=lambda nav: DashboardScreen(
                navigator=nav,
                key=Key("dashboard_screen_root"),
            ),
            name="dashboard",
        )
        self.navigator.push(dashboard_route)

    def _handle_social_login(self, provider: str):
        username = f"{provider}User"
        print(f"🔑 [LoginScreen] Social login via {provider} as '{username}'...")
        self.pref.set("is_logged_in", True)
        self.pref.set("username", username)

        try:
            from screens.dashboard_screen import DashboardScreen
        except ImportError:
            from lib.screens.dashboard_screen import DashboardScreen

        dashboard_route = PageRoute(
            builder=lambda nav: DashboardScreen(
                navigator=nav,
                key=Key("dashboard_screen_root"),
            ),
            name="dashboard",
        )
        self.navigator.push(dashboard_route)

    def _handle_forgot_password(self):
        self.error_message = None
        self.success_message = "Password reset instructions sent to your email."
        self.setState()

    def _toggle_auth_mode(self):
        self.is_register_mode = not self.is_register_mode
        self.error_message = None
        self.success_message = None
        self.setState()

    # ── Left Form Component ───────────────────────────────────────────
    def _build_left_form(self) -> Widget:
        # Status / Feedback banner
        feedback_widget = None
        if self.error_message:
            feedback_widget = Container(
                key=Key("error_banner"),
                padding=EdgeInsets.symmetric(horizontal=14, vertical=10),
                decoration=BoxDecoration(
                    color=Colors.hex("#FEE2E2"),
                    borderRadius=BorderRadius.all(12),
                    border=BorderSide(color=Colors.hex("#FCA5A5"), width=1),
                ),
                child=Row(
                    crossAxisAlignment=CrossAxisAlignment.CENTER,
                    children=[
                        Icon(
                            Icons.error_outline_rounded,
                            size=16,
                            color=Colors.hex("#DC2626"),
                        ),
                        SizedBox(width=8),
                        Expanded(
                            child=Text(
                                self.error_message,
                                style=TextStyle(
                                    fontSize=12,
                                    color=Colors.hex("#DC2626"),
                                    fontFamily="sans-serif",
                                ),
                            )
                        ),
                    ],
                ),
            )
        elif self.success_message:
            feedback_widget = Container(
                key=Key("success_banner"),
                padding=EdgeInsets.symmetric(horizontal=14, vertical=10),
                decoration=BoxDecoration(
                    color=Colors.hex("#DCFCE7"),
                    borderRadius=BorderRadius.all(12),
                    border=BorderSide(color=Colors.hex("#86EFAC"), width=1),
                ),
                child=Row(
                    crossAxisAlignment=CrossAxisAlignment.CENTER,
                    children=[
                        Icon(
                            Icons.check_circle_outline_rounded,
                            size=16,
                            color=Colors.hex("#16A34A"),
                        ),
                        SizedBox(width=8),
                        Expanded(
                            child=Text(
                                self.success_message,
                                style=TextStyle(
                                    fontSize=12,
                                    color=Colors.hex("#16A34A"),
                                    fontFamily="sans-serif",
                                ),
                            )
                        ),
                    ],
                ),
            )

        form_column_children = [
            # Header Title
            Text(
                "Welcome back!" if not self.is_register_mode else "Create an account",
                style=TextStyle(
                    fontSize=32,
                    fontWeight=800,
                    color=Colors.hex("#111827"),
                    fontFamily="sans-serif",
                ),
            ),
            SizedBox(height=8),
            # Subtitle
            Text(
                (
                    "Simplify your workflow and boost your productivity\nwith Note App. Get started for free."
                    if not self.is_register_mode
                    else "Join our community to organize, plan and write effortlessly."
                ),
                style=TextStyle(
                    fontSize=13,
                    color=Colors.hex("#6B7280"),
                    fontFamily="sans-serif",
                    lineHeight=1.45,
                ),
            ),
            SizedBox(height=28),
        ]

        if feedback_widget:
            form_column_children.extend(
                [
                    feedback_widget,
                    SizedBox(height=16),
                ]
            )

        form_column_children.extend(
            [
                # Username Input
                TextField(
                    key=Key("login_username_field"),
                    controller=self.username_controller,
                    decoration=InputDecoration(
                        hintText="Username",
                        hintStyle=TextStyle(
                            color=Colors.hex("#9CA3AF"),
                            fontSize=14,
                            fontFamily="sans-serif",
                        ),
                        filled=False,
                        borderRadius=BorderRadius.all(26),
                        border=BorderSide(color=Colors.hex("#D1D5DB"), width=1.5),
                        focusedBorder=BorderSide(
                            color=Colors.hex("#111827"), width=1.5
                        ),
                        contentPadding=EdgeInsets.symmetric(horizontal=20, vertical=15),
                    ),
                ),
                SizedBox(height=14),
                # Password Input with Toggle
                TextField(
                    key=Key("login_password_field"),
                    controller=self.password_controller,
                    obscureText=not self.show_password,
                    trailing=IconButton(
                        key=Key("password_toggle_button"),
                        icon=Icon(
                            (
                                Icons.visibility_off_rounded
                                if not self.show_password
                                else Icons.visibility_rounded
                            ),
                            color=Colors.hex("#9CA3AF"),
                            size=20,
                        ),
                        onPressed=self._toggle_password_visibility,
                    ),
                    decoration=InputDecoration(
                        hintText="Password",
                        hintStyle=TextStyle(
                            color=Colors.hex("#9CA3AF"),
                            fontSize=14,
                            fontFamily="sans-serif",
                        ),
                        filled=False,
                        borderRadius=BorderRadius.all(26),
                        border=BorderSide(color=Colors.hex("#D1D5DB"), width=1.5),
                        focusedBorder=BorderSide(
                            color=Colors.hex("#111827"), width=1.5
                        ),
                        contentPadding=EdgeInsets.symmetric(horizontal=20, vertical=15),
                    ),
                ),
                SizedBox(height=10),
                # Forgot Password Link
                Row(
                    mainAxisAlignment=MainAxisAlignment.END,
                    children=[
                        GestureDetector(
                            key=Key("forgot_password_btn"),
                            onTap=lambda d: self._handle_forgot_password(),
                            child=Text(
                                "Forgot Password?",
                                style=TextStyle(
                                    fontSize=12,
                                    fontWeight=600,
                                    color=Colors.hex("#111827"),
                                    fontFamily="sans-serif",
                                ),
                            ),
                        ),
                    ],
                ),
                SizedBox(height=24),
                # Primary Action Button
                ElevatedButton(
                    key=Key("login_primary_button"),
                    onPressed=self._handle_login,
                    onPressedName="login_primary_button_pressed",
                    style=ButtonStyle(
                        backgroundColor=Colors.hex("#000000"),
                        foregroundColor=Colors.white,
                        shape=BorderRadius.all(26),
                        padding=EdgeInsets.symmetric(vertical=14),
                        minimumSize=("100%", 50),
                        hoverColor=Colors.hex("#262626"),
                    ),
                    child=Center(
                        child=Text(
                            "Login" if not self.is_register_mode else "Get Started",
                            style=TextStyle(
                                fontSize=15,
                                fontWeight=600,
                                color=Colors.white,
                                fontFamily="sans-serif",
                            ),
                        ),
                    ),
                ),
                SizedBox(height=24),
                # Divider "or continue with"
                Row(
                    crossAxisAlignment=CrossAxisAlignment.CENTER,
                    children=[
                        Container(height=1, color=Colors.hex("#E5E7EB"), width="35%"),
                        Container(
                            key=Key("login_or_continue_with"),
                            padding=EdgeInsets.symmetric(horizontal=10),
                            child=Text(
                                "or continue with",
                                style=TextStyle(
                                    fontSize=12,
                                    color=Colors.hex("#9CA3AF"),
                                    fontFamily="sans-serif",
                                ),
                            ),
                        ),
                        Container(height=1, color=Colors.hex("#E5E7EB"), width="35%"),
                    ],
                ),
                SizedBox(height=20),
                # Social Auth Buttons
                Row(
                    mainAxisAlignment=MainAxisAlignment.CENTER,
                    children=[
                        GestureDetector(
                            key=Key("social_btn_google"),
                            onTap=lambda d: self._handle_social_login("Google"),
                            child=Image(
                                image=AssetImage("google_btn.png"),
                                width=46,
                                height=46,
                            ),
                        ),
                        SizedBox(width=16),
                        GestureDetector(
                            key=Key("social_btn_apple"),
                            onTap=lambda d: self._handle_social_login("Apple"),
                            child=Image(
                                image=AssetImage("apple_btn.png"),
                                width=46,
                                height=46,
                            ),
                        ),
                        SizedBox(width=16),
                        GestureDetector(
                            key=Key("social_btn_facebook"),
                            onTap=lambda d: self._handle_social_login("Facebook"),
                            child=Image(
                                image=AssetImage("facebook_btn.png"),
                                width=46,
                                height=46,
                            ),
                        ),
                    ],
                ),
                SizedBox(height=36),
                # Registration Footer
                Row(
                    mainAxisAlignment=MainAxisAlignment.CENTER,
                    children=[
                        Text(
                            (
                                "Not a member? "
                                if not self.is_register_mode
                                else "Already a member? "
                            ),
                            style=TextStyle(
                                fontSize=13,
                                color=Colors.hex("#6B7280"),
                                fontFamily="sans-serif",
                            ),
                        ),
                        GestureDetector(
                            key=Key("register_toggle_link"),
                            onTap=lambda d: self._toggle_auth_mode(),
                            child=Text(
                                (
                                    "Register now"
                                    if not self.is_register_mode
                                    else "Login here"
                                ),
                                style=TextStyle(
                                    fontSize=13,
                                    fontWeight=600,
                                    color=Colors.hex("#43965B"),
                                    fontFamily="sans-serif",
                                ),
                            ),
                        ),
                    ],
                ),
            ]
        )

        return Container(
            key=Key("left_form_wrapper"),
            color=Colors.white,
            padding=EdgeInsets.symmetric(horizontal=48, vertical=36),
            child=Center(
                child=Container(
                    width=380,
                    child=Column(
                        mainAxisAlignment=MainAxisAlignment.CENTER,
                        crossAxisAlignment=CrossAxisAlignment.START,
                        children=form_column_children,
                    ),
                ),
            ),
        )

    # ── Right Showcase Component ──────────────────────────────────────
    def _build_right_showcase(self) -> Widget:
        current_slide = self.slides[self.active_slide]

        # Pagination dots (3 indicators, active slide is styled like design pill)
        dots = []
        for i in range(len(self.slides)):
            is_active = i == self.active_slide
            dot_width = 22 if is_active else 8
            dot_color = Colors.hex("#111827") if is_active else Colors.hex("#D1D5DB")

            dot_widget = GestureDetector(
                key=Key(f"carousel_dot_{i}"),
                onTap=lambda d, idx=i: self._set_active_slide(idx),
                child=Container(
                    width=dot_width,
                    height=8,
                    decoration=BoxDecoration(
                        color=dot_color,
                        borderRadius=BorderRadius.all(4),
                    ),
                ),
            )
            dots.append(dot_widget)
            if i < len(self.slides) - 1:
                dots.append(SizedBox(width=6))

        return Container(
            key=Key("right_hero_card_container"),
            height="75.5vh",
            margin=EdgeInsets.all(16),
            decoration=BoxDecoration(
                color=Colors.hex("#F6FAF4"),
                borderRadius=BorderRadius.all(32),
            ),
            child=Center(
                child=Column(
                    mainAxisAlignment=MainAxisAlignment.CENTER,
                    crossAxisAlignment=CrossAxisAlignment.CENTER,
                    children=[
                        # Illustration
                        Image(
                            key=Key("login_hero_illustration"),
                            image=AssetImage("login_illustration.png"),
                            width=435,
                            height=360,
                            fit=ImageFit.CONTAIN,
                        ),
                        SizedBox(height=24),
                        # Interactive Pagination Indicators
                        Row(
                            mainAxisAlignment=MainAxisAlignment.CENTER,
                            children=dots,
                        ),
                        SizedBox(height=28),
                        # Value Proposition Headline
                        Text(
                            current_slide["title"],
                            style=TextStyle(
                                fontSize=18,
                                # fontWeight=600,
                                color=Colors.hex("#111827"),
                                fontFamily="sans-serif",
                            ),
                        ),
                        SizedBox(height=6),
                        Row(
                            mainAxisAlignment=MainAxisAlignment.CENTER,
                            children=[
                                Text(
                                    "with ",
                                    style=TextStyle(
                                        fontSize=18,
                                        fontWeight=500,
                                        color=Colors.hex("#111827"),
                                        fontFamily="sans-serif",
                                    ),
                                ),
                                Text(
                                    "Note App",
                                    style=TextStyle(
                                        fontSize=18,
                                        fontWeight=800,
                                        color=Colors.hex("#111827"),
                                        fontFamily="sans-serif",
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        )

    # ── UI Builder ────────────────────────────────────────────────────
    def build(self) -> Widget:
        return Container(
            key=Key("login_screen_root"),
            width="100vw",
            height="100vh",
            color=Colors.white,
            child=Center(
                child=Row(
                    children=[
                        # Left Side: Form Controls
                        Container(
                            key=Key("login_form_container"),
                            width="50vw",
                            child=SingleChildScrollView(
                                child=self._build_left_form(),
                            ),
                        ),
                        # Right Side: Sage Illustration Showcase Card
                        Container(
                            key=Key("login_right_container"),
                            width="50vw",
                            height="80vh",
                            child=SingleChildScrollView(
                                child=self._build_right_showcase(),
                            ),
                        ),
                    ],
                ),
            ),
        )

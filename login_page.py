import streamlit as st
from modules.auth import AuthManager
import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password_strength(password):
    """Check password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Strong password"

def show_login_page():
    """Display a minimal, modern login page with registration and password reset"""
    
    # Hide Streamlit default elements
    st.markdown("""
        <style>
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Main container styling */
        .stApp {
            background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
        }
        
        /* Header */
        .login-header {
            text-align: center;
            margin-bottom: 2.5rem;
        }
        
        .app-icon {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.5));
        }
        
        .app-title {
            font-size: 1.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }
        
        .app-subtitle {
            color: #888;
            font-size: 0.9rem;
            font-weight: 400;
        }
        
        /* Form inputs */
        .stTextInput input {
            background: rgba(45, 45, 45, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            padding: 0.75rem 1rem !important;
            color: white !important;
            font-size: 0.95rem !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput input:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
        }
        
        .stTextInput input::placeholder {
            color: #666 !important;
        }
        
        /* Buttons */
        .stButton button {
            border-radius: 12px !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            transition: all 0.3s ease !important;
            border: none !important;
        }
        
        .stButton button[kind="primary"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
        }
        
        .stButton button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4) !important;
        }
        
        .stButton button[kind="secondary"] {
            background: rgba(255, 255, 255, 0.05) !important;
            color: #aaa !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background: rgba(45, 45, 45, 0.5) !important;
            border-radius: 12px !important;
            border-left: 3px solid #667eea !important;
            color: #667eea !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
        }
        
        .streamlit-expanderContent {
            background: rgba(45, 45, 45, 0.3) !important;
            border-radius: 0 0 12px 12px !important;
        }
        
        /* Demo item styling */
        .demo-item {
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 0.85rem;
        }
        
        .demo-item:last-child {
            border-bottom: none;
        }
        
        .demo-label {
            color: #999;
        }
        
        .demo-creds {
            color: #667eea;
            font-family: 'Courier New', monospace;
            font-weight: 500;
        }
        
        /* Footer */
        .login-footer {
            text-align: center;
            margin-top: 2rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .footer-text {
            color: #666;
            font-size: 0.75rem;
        }
        
        /* Alerts */
        .stAlert {
            border-radius: 12px !important;
            border: none !important;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 0.75rem 1.5rem;
            color: #aaa;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        /* Hide streamlit label */
        .stTextInput label {
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            color: #aaa !important;
            margin-bottom: 0.5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state for form mode
    if 'form_mode' not in st.session_state:
        st.session_state['form_mode'] = 'login'
    
    # Create centered layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Header
        st.markdown("""
            <div class="login-header">
                <div class="app-icon"></div>
                <h1 class="app-title">HR Analytics Platform</h1>
                <p class="app-subtitle">Enterprise Workforce Intelligence</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Initialize auth manager
        auth_manager = AuthManager()
        
        # Tabs for Login / Register / Reset Password
        tab1, tab2, tab3 = st.tabs([" Login", " Register", "🔑 Reset Password"])
        
        # ===== LOGIN TAB =====
        with tab1:
            st.markdown("### Sign In to Continue")
            
            username = st.text_input(
                "Username",
                placeholder="Enter username",
                key="login_username",
                label_visibility="visible"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password",
                key="login_password",
                label_visibility="visible"
            )
            
            col_a, col_b = st.columns([3, 1])
            
            with col_a:
                login_button = st.button(
                    " Login",
                    use_container_width=True,
                    type="primary",
                    key="login_btn"
                )
            
            with col_b:
                help_button = st.button(
                    "Help",
                    use_container_width=True,
                    type="secondary",
                    key="help_btn"
                )
            
            if login_button:
                if username and password:
                    success, user_info = auth_manager.verify_credentials(username, password)
                    
                    if success:
                        st.session_state['authenticated'] = True
                        st.session_state['username'] = username
                        st.session_state['user_info'] = user_info
                        st.success(f"✅ Welcome, {user_info['name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
                else:
                    st.warning("⚠️ Please fill in all fields")
            
            if help_button:
                st.info("Contact: support@hranalytics.com")
        
        # ===== REGISTER TAB =====
        with tab2:
            st.markdown("### Create New Account")
            
            new_username = st.text_input(
                "Username",
                placeholder="Choose a username",
                key="reg_username",
                label_visibility="visible"
            )
            
            new_name = st.text_input(
                "Full Name",
                placeholder="Enter your full name",
                key="reg_name",
                label_visibility="visible"
            )
            
            new_email = st.text_input(
                "Email",
                placeholder="Enter your email",
                key="reg_email",
                label_visibility="visible"
            )
            
            new_role = st.selectbox(
                "Role",
                ["Analyst", "HR Manager", "Admin"],
                key="reg_role"
            )
            
            new_password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a strong password",
                key="reg_password",
                label_visibility="visible"
            )
            
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter password",
                key="reg_confirm_password",
                label_visibility="visible"
            )
            
            # Password strength indicator
            if new_password:
                is_strong, msg = validate_password_strength(new_password)
                if is_strong:
                    st.success(f"✅ {msg}")
                else:
                    st.warning(f"⚠️ {msg}")
            
            register_button = st.button(
                " Create Account",
                use_container_width=True,
                type="primary",
                key="register_btn"
            )
            
            if register_button:
                if not all([new_username, new_name, new_email, new_password, confirm_password]):
                    st.error("❌ Please fill in all fields")
                elif not validate_email(new_email):
                    st.error("❌ Invalid email format")
                elif new_password != confirm_password:
                    st.error("❌ Passwords do not match")
                else:
                    is_strong, msg = validate_password_strength(new_password)
                    if not is_strong:
                        st.error(f"❌ {msg}")
                    else:
                        success, message = auth_manager.create_user(
                            new_username, new_password, new_name, new_role, new_email
                        )
                        if success:
                            st.success("✅ Account created successfully! Please login.")
                        else:
                            st.error(f"❌ {message}")
        
        # ===== RESET PASSWORD TAB =====
        with tab3:
            st.markdown("### Reset Your Password")
            
            reset_email = st.text_input(
                "Email Address",
                placeholder="Enter your registered email",
                key="reset_email",
                label_visibility="visible"
            )
            
            reset_username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="reset_username",
                label_visibility="visible"
            )
            
            new_reset_password = st.text_input(
                "New Password",
                type="password",
                placeholder="Enter new password",
                key="reset_new_password",
                label_visibility="visible"
            )
            
            confirm_reset_password = st.text_input(
                "Confirm New Password",
                type="password",
                placeholder="Re-enter new password",
                key="reset_confirm_password",
                label_visibility="visible"
            )
            
            # Password strength indicator
            if new_reset_password:
                is_strong, msg = validate_password_strength(new_reset_password)
                if is_strong:
                    st.success(f"✅ {msg}")
                else:
                    st.warning(f"⚠️ {msg}")
            
            reset_button = st.button(
                "🔑 Reset Password",
                use_container_width=True,
                type="primary",
                key="reset_btn"
            )
            
            if reset_button:
                if not all([reset_email, reset_username, new_reset_password, confirm_reset_password]):
                    st.error("❌ Please fill in all fields")
                elif new_reset_password != confirm_reset_password:
                    st.error("❌ Passwords do not match")
                else:
                    is_strong, msg = validate_password_strength(new_reset_password)
                    if not is_strong:
                        st.error(f"❌ {msg}")
                    else:
                        success, message = auth_manager.reset_password(
                            reset_username, reset_email, new_reset_password
                        )
                        if success:
                            st.success("✅ Password reset successfully! Please login.")
                        else:
                            st.error(f"❌ {message}")
        
        # Collapsible Demo Accounts Section
        with st.expander(" **Demo Accounts** (Click to expand)"):
            st.markdown("""
                <div class="demo-item">
                    <span class="demo-label"> Admin</span>
                    <span class="demo-creds">admin / admin123</span>
                </div>
                <div class="demo-item">
                    <span class="demo-label"> HR Manager</span>
                    <span class="demo-creds">hr_manager / hr123</span>
                </div>
                <div class="demo-item">
                    <span class="demo-label"> Analyst</span>
                    <span class="demo-creds">analyst / analyst123</span>
                </div>
            """, unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
            <div class="login-footer">
                <p class="footer-text"> Secure •  Enterprise •  Powered by Streamlit</p>
                <p class="footer-text" style="margin-top: 0.5rem;">© 2026 HR Analytics Platform v1.0</p>
            </div>
        """, unsafe_allow_html=True)

def logout():
    """Handle user logout"""
    for key in ['authenticated', 'username', 'user_info']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
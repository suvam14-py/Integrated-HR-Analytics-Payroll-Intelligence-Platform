import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from modules.database import HRDatabase
from modules.payroll import PayrollEngine
from modules.analytics import PerformanceAnalytics
from modules.ml_model import AttritionPredictor
from modules.visualizations import HRVisualizations
from login_page import show_login_page, logout

# Page config
st.set_page_config(
    page_title="HR Analytics Platform", 
    layout="wide", 
    page_icon="🎯",
    initial_sidebar_state="expanded"
)

# Check authentication
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Show login page if not authenticated
if not st.session_state['authenticated']:
    show_login_page()
    st.stop()

# Initialize database and model (only after login)
@st.cache_resource
def init_database():
    db = HRDatabase()
    db.load_data_from_csv()
    return db

@st.cache_resource
def train_ml_model():
    db = init_database()
    data = db.get_consolidated_data()
    predictor = AttritionPredictor()
    accuracy = predictor.train(data)
    return predictor, accuracy

# Minimal dashboard styling
st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Clean sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e1e 0%, #2d2d2d 100%);
    }
    
    /* User card */
    .user-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.25rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }
    
    .user-avatar {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 0.75rem;
    }
    
    .user-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: white;
        text-align: center;
        margin-bottom: 0.25rem;
    }
    
    .user-role {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.85);
        text-align: center;
        margin-bottom: 0.25rem;
    }
    
    .user-email {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.7);
        text-align: center;
    }
    
    /* Navigation radio buttons */
    .stRadio > div {
        gap: 0.5rem;
    }
    
    .stRadio > div > label {
        background: rgba(255, 255, 255, 0.05);
        padding: 0.75rem 1rem;
        border-radius: 10px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stRadio > div > label:hover {
        background: rgba(102, 126, 234, 0.2);
    }
    
    /* Logout button */
    .stButton button[kind="secondary"] {
        background: rgba(239, 68, 68, 0.15) !important;
        color: #ef4444 !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
    }
    
    .stButton button[kind="secondary"]:hover {
        background: rgba(239, 68, 68, 0.25) !important;
        border-color: #ef4444 !important;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    /* Clean headers */
    h1 {
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    h3 {
        font-weight: 600;
        color: #aaa;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar with user info
with st.sidebar:
    # Minimal user info card
    user_info = st.session_state.get('user_info', {})
    st.markdown(f"""
        <div class="user-card">
            <div class="user-avatar">👤</div>
            <div class="user-name">{user_info.get('name', 'User')}</div>
            <div class="user-role">{user_info.get('role', 'Role')}</div>
            <div class="user-email">{user_info.get('email', 'N/A')}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Simplified navigation
    page = st.radio(
        "Navigate",
        [
            "📊 Dashboard",
            "💰 Payroll",
            "📈 Performance",
            "⚠️ Attrition",
            "👤 Employees"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Logout button
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        logout()
    
    # Footer info
    st.markdown("""
        <div style="text-align: center; margin-top: 2rem; color: #666; font-size: 0.75rem;">
            <p>HR Analytics Platform</p>
            <p>v1.0 • Streamlit</p>
        </div>
    """, unsafe_allow_html=True)

# Load data
db = init_database()
data = db.get_consolidated_data()
data = data.loc[:, ~data.columns.duplicated()]
predictor, model_accuracy = train_ml_model()

# ===== PAGE 1: Dashboard Overview =====
if page == "📊 Dashboard":
    st.title("📊 HR Analytics Dashboard")
    st.markdown(f"### Welcome back, {user_info.get('name')}! 👋")
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Employees", len(data))
    with col2:
        avg_salary = data['base_salary'].mean()
        st.metric("Avg Salary", f"₹{avg_salary:,.0f}")
    with col3:
        avg_performance = data['performance_rating'].mean()
        st.metric("Avg Performance", f"{avg_performance:.2f}/5")
    with col4:
        high_risk = len(data[data['attrition_risk'] == 1])
        st.metric("High Attrition Risk", high_risk)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(HRVisualizations.create_salary_distribution(data), use_container_width=True)
    
    with col2:
        dept_perf = PerformanceAnalytics.department_performance(data)
        st.plotly_chart(HRVisualizations.create_department_performance(dept_perf), use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        predicted_data = predictor.predict_attrition(data.copy())
        st.plotly_chart(HRVisualizations.create_attrition_risk_pie(predicted_data), use_container_width=True)
    
    with col2:
        st.plotly_chart(HRVisualizations.create_performance_scatter(data), use_container_width=True)

# ===== PAGE 2: Payroll Management =====
elif page == "💰 Payroll":
    st.title("💰 Payroll Management")
    
    payroll_data = PayrollEngine.calculate_payroll(data)
    st.plotly_chart(HRVisualizations.create_payroll_summary(payroll_data), use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Gross Payroll", f"₹{payroll_data['gross_salary'].sum():,.0f}")
    with col2:
        st.metric("Total Deductions", f"₹{(payroll_data['tax_deduction'].sum() + payroll_data['pf_deduction'].sum()):,.0f}")
    with col3:
        st.metric("Total Net Payroll", f"₹{payroll_data['net_salary'].sum():,.0f}")
    
    st.subheader("📋 Monthly Payroll Report")
    display_df = payroll_data.copy()
    st.dataframe(display_df.style.format({
        'base_salary': '₹{:,.0f}',
        'performance_bonus': '₹{:,.0f}',
        'overtime_pay': '₹{:,.0f}',
        'gross_salary': '₹{:,.0f}',
        'tax_deduction': '₹{:,.0f}',
        'pf_deduction': '₹{:,.0f}',
        'net_salary': '₹{:,.0f}'
    }), use_container_width=True)
    
    csv = payroll_data.to_csv(index=False)
    st.download_button("📥 Download Payroll Report", csv, "payroll_report.csv", "text/csv")

# ===== PAGE 3: Performance Analytics =====
elif page == "📈 Performance":
    st.title("📈 Performance Analytics")
    
    st.subheader("🏢 Department Performance")
    dept_perf = PerformanceAnalytics.department_performance(data)
    st.dataframe(dept_perf, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⭐ Top 10 Performers")
        top_performers = PerformanceAnalytics.identify_top_performers(data, 10)
        st.dataframe(top_performers, use_container_width=True)
    
    with col2:
        st.subheader("⚠️ Bottom 10 Performers")
        underperformers = PerformanceAnalytics.identify_underperformers(data, 10)
        st.dataframe(underperformers, use_container_width=True)
    
    data_copy = data.copy()
    data_copy['productivity_score'] = PerformanceAnalytics.calculate_productivity_score(data_copy)
    
    import plotly.express as px
    fig = px.histogram(data_copy, x='productivity_score', nbins=30,
                      title='Productivity Score Distribution')
    st.plotly_chart(fig, use_container_width=True)

# ===== PAGE 4: Attrition Prediction =====
elif page == "⚠️ Attrition":
    st.title("⚠️ Attrition Prediction")
    
    st.info(f"🎯 Model Accuracy: {model_accuracy*100:.2f}%")
    
    predicted_data = predictor.predict_attrition(data.copy())
    
    col1, col2, col3 = st.columns(3)
    
    low_risk = len(predicted_data[predicted_data['risk_level'] == 'Low'])
    medium_risk = len(predicted_data[predicted_data['risk_level'] == 'Medium'])
    high_risk = len(predicted_data[predicted_data['risk_level'] == 'High'])
    
    with col1:
        st.metric("🟢 Low Risk", low_risk)
    with col2:
        st.metric("🟡 Medium Risk", medium_risk)
    with col3:
        st.metric("🔴 High Risk", high_risk)
    
    st.subheader("🚨 High-Risk Employees")
    high_risk_employees = predicted_data[predicted_data['risk_level'] == 'High'][
        ['emp_id', 'name', 'department', 'attrition_probability', 'performance_rating', 'base_salary']
    ].sort_values('attrition_probability', ascending=False)
    
    st.dataframe(high_risk_employees.style.format({
        'attrition_probability': '{:.2%}',
        'base_salary': '₹{:,.0f}'
    }), use_container_width=True)
    
    st.subheader("📊 Key Attrition Factors")
    importance = predictor.get_feature_importance()
    import plotly.express as px
    fig = px.bar(importance.head(10), x='importance', y='feature', orientation='h',
                title='Top 10 Features Influencing Attrition')
    st.plotly_chart(fig, use_container_width=True)

# ===== PAGE 5: Employee Details =====
elif page == "👤 Employees":
    st.title("👤 Employee Details")
    
    emp_list = data['emp_id'].tolist()
    selected_emp = st.selectbox("Select Employee", emp_list)
    
    emp_details = data[data['emp_id'] == selected_emp].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📋 Basic Info")
        st.write(f"**Name:** {emp_details['name']}")
        st.write(f"**Employee ID:** {emp_details['emp_id']}")
        st.write(f"**Department:** {emp_details['department']}")
        st.write(f"**Designation:** {emp_details['designation']}")
    
    with col2:
        st.subheader("💼 Work Info")
        st.write(f"**Experience:** {emp_details['experience_years']} years")
        st.write(f"**Joining Date:** {emp_details['joining_date']}")
        st.write(f"**Performance Rating:** {emp_details['performance_rating']}/5")
        st.write(f"**Tasks Completed:** {emp_details['tasks_completed']}/{emp_details['tasks_assigned']}")
    
    with col3:
        st.subheader("💰 Compensation")
        emp_data_single = data[data['emp_id'] == selected_emp].copy()
        payslip = PayrollEngine.generate_payslip(emp_data_single)
        st.write(f"**Base Salary:** ₹{payslip['base_salary']:,.0f}")
        st.write(f"**Performance Bonus:** ₹{payslip['performance_bonus']:,.0f}")
        st.write(f"**Gross Salary:** ₹{payslip['gross_salary']:,.0f}")
        st.write(f"**Net Salary:** ₹{payslip['net_salary']:,.0f}")
    
    st.subheader("⚠️ Attrition Risk Assessment")
    emp_data_for_pred = data[data['emp_id'] == selected_emp].copy()
    prediction = predictor.predict_attrition(emp_data_for_pred)
    
    risk_level = prediction['risk_level'].iloc[0]
    risk_prob = prediction['attrition_probability'].iloc[0]
    
    color_map = {'Low': '🟢', 'Medium': '🟡', 'High': '🔴'}
    st.write(f"**Risk Level:** {color_map[risk_level]} {risk_level}")
    st.write(f"**Attrition Probability:** {risk_prob:.2%}")
    
    st.progress(float(risk_prob))
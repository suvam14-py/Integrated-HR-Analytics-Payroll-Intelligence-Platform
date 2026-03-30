# 🎯 Integrated HR Analytics & Payroll Intelligence Platform

An enterprise-grade **Workforce Intelligence System** developed with **Python** and **Streamlit**. This platform serves as a centralized hub for HR professionals to manage payroll, track performance, and leverage machine learning to predict employee attrition.

## 🚀 Key Features

* [cite_start]**🔐 Advanced Authentication System**: A custom-styled, secure login interface featuring user registration, password strength validation, and role-based access control (Admin, HR Manager, Analyst)[cite: 191].
* [cite_start]**⚠️ Predictive Attrition Modeling**: Integrates a **Scikit-learn** backend to calculate attrition probabilities and identify high-risk employees based on performance, salary, and engagement metrics[cite: 191, 192].
* [cite_start]**💰 Automated Payroll Engine**: Provides real-time calculation of gross salaries, tax deductions (TDS), PF contributions, and net pay, with support for exporting reports to CSV[cite: 191].
* [cite_start]**📈 Performance Analytics**: Deep-dive analytics into department-wise productivity, identifying top performers and under-performers using automated scoring algorithms[cite: 191].
* [cite_start]**📊 Dynamic Data Storytelling**: Utilizes **Plotly** for interactive visualizations, including salary distributions, risk assessment pie charts, and performance scatter plots[cite: 191, 192].
* [cite_start]**👤 Employee 360° Profile**: A dedicated module for granular inspection of individual employee data, work history, and compensation breakdowns[cite: 191].

## 🛠️ Tech Stack

* [cite_start]**Frontend**: Streamlit (with custom CSS injection for an enterprise dark-theme UI)[cite: 191, 192].
* [cite_start]**Backend**: Python[cite: 191].
* [cite_start]**Database**: SQLite (`hr_analytics.db`) managing relational tables for employees, attendance, and performance[cite: 191].
* [cite_start]**Data Science**: Pandas, NumPy, and Scikit-learn[cite: 191, 192].
* [cite_start]**Visualization**: Plotly Express[cite: 191, 192].

## 📂 Project Structure

```text
├── app.py                # Main application entry point & dashboard logic
├── login_page.py         # Authentication UI and validation logic
├── hr_analytics.db       # SQLite database containing employee records
├── requirements.txt      # Project dependencies
└── modules/              # Modular backend logic (Database, Payroll, ML, etc.)

import sqlite3
import pandas as pd

class HRDatabase:
    def __init__(self, db_name='hr_analytics.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        
    def load_data_from_csv(self):
        """Load CSV data into SQLite"""
        employees = pd.read_csv('data/employees.csv')
        performance = pd.read_csv('data/performance.csv')
        attendance = pd.read_csv('data/attendance.csv')
        activities = pd.read_csv('data/activities.csv')
        
        employees.to_sql('employees', self.conn, if_exists='replace', index=False)
        performance.to_sql('performance', self.conn, if_exists='replace', index=False)
        attendance.to_sql('attendance', self.conn, if_exists='replace', index=False)
        activities.to_sql('activities', self.conn, if_exists='replace', index=False)
        
    def get_all_employees(self):
        return pd.read_sql("SELECT * FROM employees", self.conn)
    
    def get_employee_details(self, emp_id):
        query = """
        SELECT 
            e.*,
            p.performance_rating, p.tasks_completed, p.tasks_assigned, 
            p.quality_score, p.projects_delivered,
            a.days_present, a.days_absent, a.overtime_hours,
            ac.avg_login_hours, ac.emails_sent, ac.meetings_attended, 
            ac.collaboration_score
        FROM employees e
        LEFT JOIN performance p ON e.emp_id = p.emp_id
        LEFT JOIN attendance a ON e.emp_id = a.emp_id
        LEFT JOIN activities ac ON e.emp_id = ac.emp_id
        WHERE e.emp_id = ?
        """
        return pd.read_sql(query, self.conn, params=(emp_id,))
    
    def get_consolidated_data(self):
        """Get all data joined - with explicit column selection to avoid duplicates"""
        query = """
        SELECT 
            e.emp_id, e.name, e.department, e.designation, 
            e.base_salary, e.joining_date, e.experience_years, e.attrition_risk,
            p.performance_rating, p.tasks_completed, p.tasks_assigned, 
            p.quality_score, p.projects_delivered,
            a.days_present, a.days_absent, a.overtime_hours,
            ac.avg_login_hours, ac.emails_sent, ac.meetings_attended, 
            ac.collaboration_score
        FROM employees e
        LEFT JOIN performance p ON e.emp_id = p.emp_id
        LEFT JOIN attendance a ON e.emp_id = a.emp_id
        LEFT JOIN activities ac ON e.emp_id = ac.emp_id
        """
        return pd.read_sql(query, self.conn)
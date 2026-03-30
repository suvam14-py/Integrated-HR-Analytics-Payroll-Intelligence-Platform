import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Create data directory
os.makedirs('data', exist_ok=True)

np.random.seed(42)
n_employees = 100

# Employee Master Data
employees = pd.DataFrame({
    'emp_id': [f'EMP{str(i).zfill(3)}' for i in range(1, n_employees + 1)],
    'name': [f'Employee {i}' for i in range(1, n_employees + 1)],
    'department': np.random.choice(['IT', 'Sales', 'HR', 'Finance', 'Operations'], n_employees),
    'designation': np.random.choice(['Junior', 'Senior', 'Lead', 'Manager'], n_employees),
    'base_salary': np.random.randint(30000, 120000, n_employees),
    'joining_date': [(datetime.now() - timedelta(days=np.random.randint(365, 1825))).strftime('%Y-%m-%d') 
                    for _ in range(n_employees)],
    'experience_years': np.random.randint(1, 8, n_employees),
})

# Performance Data
performance = pd.DataFrame({
    'emp_id': employees['emp_id'],
    'performance_rating': np.random.choice([3, 4, 5], n_employees, p=[0.2, 0.5, 0.3]),
    'tasks_completed': np.random.randint(20, 100, n_employees),
    'tasks_assigned': np.random.randint(25, 105, n_employees),
    'quality_score': np.random.randint(60, 100, n_employees),
    'projects_delivered': np.random.randint(1, 10, n_employees),
})

# Attendance Data
attendance = pd.DataFrame({
    'emp_id': employees['emp_id'],
    'days_present': np.random.randint(20, 31, n_employees),
    'days_absent': np.random.randint(0, 5, n_employees),
    'overtime_hours': np.random.randint(0, 40, n_employees),
})

# Activity Logs
activities = pd.DataFrame({
    'emp_id': employees['emp_id'],
    'avg_login_hours': np.random.uniform(6, 10, n_employees),
    'emails_sent': np.random.randint(50, 300, n_employees),
    'meetings_attended': np.random.randint(10, 50, n_employees),
    'collaboration_score': np.random.randint(50, 100, n_employees),
})

# Add attrition labels
attrition_prob = (
    (5 - performance['performance_rating']) * 0.3 +
    (attendance['days_absent'] / 10) * 0.3 +
    np.random.random(n_employees) * 0.4
)
employees['attrition_risk'] = (attrition_prob > 0.5).astype(int)

# Save files
employees.to_csv('data/employees.csv', index=False)
performance.to_csv('data/performance.csv', index=False)
attendance.to_csv('data/attendance.csv', index=False)
activities.to_csv('data/activities.csv', index=False)

print("✅ Data generated successfully!")
print(f"✅ Created {len(employees)} employee records")
print(f"✅ Files saved in 'data/' directory")
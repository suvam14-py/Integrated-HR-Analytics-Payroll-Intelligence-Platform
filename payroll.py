import pandas as pd
import numpy as np

class PayrollEngine:
    @staticmethod
    def calculate_payroll(employee_data):
        """Calculate net salary with deductions and bonuses"""
        
        # Create a copy to avoid modifying original
        emp_data = employee_data.copy()
        
        # Performance bonus (5-15% of base salary)
        bonus_percentage = emp_data['performance_rating'] * 0.03
        performance_bonus = emp_data['base_salary'] * bonus_percentage
        
        # Overtime pay (500 per hour)
        overtime_pay = emp_data['overtime_hours'] * 500
        
        # Gross salary
        gross_salary = emp_data['base_salary'] + performance_bonus + overtime_pay
        
        # Tax deductions (20% of gross)
        tax_deduction = gross_salary * 0.20
        
        # Provident Fund (12% of base)
        pf_deduction = emp_data['base_salary'] * 0.12
        
        # Net salary
        net_salary = gross_salary - tax_deduction - pf_deduction
        
        return pd.DataFrame({
            'emp_id': emp_data['emp_id'].values,
            'name': emp_data['name'].values,
            'base_salary': emp_data['base_salary'].values,
            'performance_bonus': performance_bonus.values,
            'overtime_pay': overtime_pay.values,
            'gross_salary': gross_salary.values,
            'tax_deduction': tax_deduction.values,
            'pf_deduction': pf_deduction.values,
            'net_salary': net_salary.values
        })
    
    @staticmethod
    def generate_payslip(emp_data):
        """Generate individual payslip"""
        payroll = PayrollEngine.calculate_payroll(emp_data)
        return payroll.iloc[0].to_dict()
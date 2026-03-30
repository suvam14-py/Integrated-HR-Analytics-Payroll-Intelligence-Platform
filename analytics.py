import pandas as pd
import numpy as np

class PerformanceAnalytics:
    @staticmethod
    def calculate_productivity_score(data):
        """Calculate overall productivity score (0-100)"""
        completion_rate = (data['tasks_completed'] / data['tasks_assigned']) * 100
        quality_score = data['quality_score']
        attendance_score = (data['days_present'] / 30) * 100
        
        # Weighted average
        productivity_score = (
            completion_rate * 0.4 +
            quality_score * 0.4 +
            attendance_score * 0.2
        )
        return productivity_score.clip(0, 100)
    
    @staticmethod
    def identify_top_performers(data, top_n=10):
        """Identify top N performers"""
        data['productivity_score'] = PerformanceAnalytics.calculate_productivity_score(data)
        return data.nlargest(top_n, 'productivity_score')[['emp_id', 'name', 'department', 'productivity_score']]
    
    @staticmethod
    def identify_underperformers(data, bottom_n=10):
        """Identify bottom N performers"""
        data['productivity_score'] = PerformanceAnalytics.calculate_productivity_score(data)
        return data.nsmallest(bottom_n, 'productivity_score')[['emp_id', 'name', 'department', 'productivity_score']]
    
    @staticmethod
    def department_performance(data):
        """Department-wise performance summary"""
        data['productivity_score'] = PerformanceAnalytics.calculate_productivity_score(data)
        return data.groupby('department').agg({
            'productivity_score': 'mean',
            'performance_rating': 'mean',
            'tasks_completed': 'sum',
            'emp_id': 'count'
        }).rename(columns={'emp_id': 'employee_count'}).round(2)
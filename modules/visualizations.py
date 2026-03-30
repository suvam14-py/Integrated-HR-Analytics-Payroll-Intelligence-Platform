import plotly.express as px
import plotly.graph_objects as go

class HRVisualizations:
    @staticmethod
    def create_salary_distribution(data):
        fig = px.histogram(data, x='base_salary', nbins=20,
                          title='Salary Distribution',
                          labels={'base_salary': 'Base Salary', 'count': 'Number of Employees'})
        return fig
    
    @staticmethod
    def create_department_performance(dept_data):
        fig = px.bar(dept_data.reset_index(), x='department', y='productivity_score',
                    title='Department-wise Performance',
                    labels={'productivity_score': 'Avg Productivity Score'})
        return fig
    
    @staticmethod
    def create_attrition_risk_pie(data):
        risk_counts = data['risk_level'].value_counts()
        fig = px.pie(values=risk_counts.values, names=risk_counts.index,
                    title='Attrition Risk Distribution',
                    color_discrete_sequence=['#00CC96', '#FFA15A', '#EF553B'])
        return fig
    
    @staticmethod
    def create_performance_scatter(data):
        fig = px.scatter(data, x='performance_rating', y='base_salary',
                        size='experience_years', color='department',
                        hover_data=['name'],
                        title='Performance vs Compensation')
        return fig
    
    @staticmethod
    def create_payroll_summary(payroll_data):
        summary = {
            'Total Gross Payroll': payroll_data['gross_salary'].sum(),
            'Total Tax Deductions': payroll_data['tax_deduction'].sum(),
            'Total Net Payroll': payroll_data['net_salary'].sum(),
            'Total Bonuses Paid': payroll_data['performance_bonus'].sum()
        }
        
        fig = go.Figure(data=[go.Bar(
            x=list(summary.keys()),
            y=list(summary.values()),
            marker_color=['#636EFA', '#EF553B', '#00CC96', '#AB63FA']
        )])
        fig.update_layout(title='Payroll Summary Overview')
        return fig
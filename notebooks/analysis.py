import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# 1. MySQL Connect
engine = create_engine('mysql+mysqlconnector://root:kalai@localhost/hr_analytics')

# 2. Business Question 1
query1 = """
    SELECT department, 
           COUNT(*) as total_employees,
           SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as left_employees,
           ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as attrition_rate
    FROM employees
    GROUP BY department
    ORDER BY attrition_rate DESC;
"""
df1 = pd.read_sql(query1, engine)
print("📊 Department-wise Attrition:")
print(df1)

# 3. Business Question 2
query2 = """
    SELECT attrition,
           ROUND(AVG(monthly_income), 2) as avg_salary
    FROM employees
    GROUP BY attrition;
"""
df2 = pd.read_sql(query2, engine)
print("\n💰 Salary vs Attrition:")
print(df2)

# 4. Business Question 3
query3 = """
    SELECT e.attrition, j.overtime,
           COUNT(*) as total
    FROM employees e
    JOIN job_satisfaction j ON e.employee_id = j.employee_id
    GROUP BY e.attrition, j.overtime
    ORDER BY e.attrition;
"""
df3 = pd.read_sql(query3, engine)
print("\n⏰ Overtime vs Attrition:")
print(df3)

# =============================
# CHARTS & GRAPHS
# =============================

# Chart 1: Department-wise Attrition Rate
plt.figure(figsize=(8, 5))
sns.barplot(data=df1, x='department', y='attrition_rate', palette='Reds_d')
plt.title('Department-wise Attrition Rate (%)', fontsize=14)
plt.xlabel('Department')
plt.ylabel('Attrition Rate (%)')
plt.tight_layout()
plt.savefig('outputs/chart1_department_attrition.png')
plt.close()
print("✅ Chart 1 Saved!")

# Chart 2: Salary vs Attrition
plt.figure(figsize=(6, 5))
sns.barplot(data=df2, x='attrition', y='avg_salary', palette='Blues_d')
plt.title('Average Salary vs Attrition', fontsize=14)
plt.xlabel('Attrition (Yes/No)')
plt.ylabel('Average Monthly Salary')
plt.tight_layout()
plt.savefig('outputs/chart2_salary_attrition.png')
plt.close()
print("✅ Chart 2 Saved!")

# Chart 3: Overtime vs Attrition
plt.figure(figsize=(7, 5))
sns.barplot(data=df3, x='overtime', y='total', hue='attrition', palette='Set2')
plt.title('Overtime vs Attrition', fontsize=14)
plt.xlabel('Overtime (Yes/No)')
plt.ylabel('Number of Employees')
plt.tight_layout()
plt.savefig('outputs/chart3_overtime_attrition.png')
plt.close()
print("✅ Chart 3 Saved!")

print("\n🎉 All Charts Saved in outputs/ folder!")
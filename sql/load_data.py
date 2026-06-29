import pandas as pd
from sqlalchemy import create_engine

# 1. CSV Load பண்ணு
df = pd.read_csv('data/hr_data.csv')
print("✅ CSV Loaded! Shape:", df.shape)

# 2. MySQL Connect பண்ணு
# 'root' = username, 'yourpassword' = உன் MySQL password
engine = create_engine('mysql+mysqlconnector://root:kalai@localhost/hr_analytics')

# 3. Employees Table Data
employees_df = df[[
    'EmployeeNumber', 'Age', 'Gender', 'MaritalStatus',
    'Education', 'Department', 'JobRole', 'JobLevel',
    'YearsAtCompany', 'MonthlyIncome', 'Attrition'
]].copy()

employees_df.columns = [
    'employee_id', 'age', 'gender', 'marital_status',
    'education', 'department', 'job_role', 'job_level',
    'years_at_company', 'monthly_income', 'attrition'
]

# 4. Job Satisfaction Table Data
satisfaction_df = df[[
    'EmployeeNumber', 'JobSatisfaction', 'WorkLifeBalance',
    'EnvironmentSatisfaction', 'OverTime'
]].copy()

satisfaction_df.columns = [
    'employee_id', 'job_satisfaction', 'work_life_balance',
    'environment_satisfaction', 'overtime'
]

# 5. MySQL-ல Insert பண்ணு
employees_df.to_sql('employees', engine, if_exists='replace', index=False)
satisfaction_df.to_sql('job_satisfaction', engine, if_exists='replace', index=False)

print("✅ Data Loaded Successfully!")
print(f"Total Employees: {len(employees_df)}")
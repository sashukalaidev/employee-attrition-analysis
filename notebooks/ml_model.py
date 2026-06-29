import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. MySQL Connect
engine = create_engine('mysql+mysqlconnector://root:kalai@localhost/hr_analytics')

# 2. Data Load from SQL
query = """
    SELECT e.age, e.education, e.job_level,
           e.years_at_company, e.monthly_income,
           e.attrition, j.job_satisfaction,
           j.work_life_balance, j.environment_satisfaction,
           j.overtime
    FROM employees e
    JOIN job_satisfaction j ON e.employee_id = j.employee_id;
"""
df = pd.read_sql(query, engine)
print("✅ Data Loaded! Shape:", df.shape)

# 3. Data Prepare
# Yes/No → 1/0
df['attrition'] = df['attrition'].map({'Yes': 1, 'No': 0})
df['overtime'] = df['overtime'].map({'Yes': 1, 'No': 0})

# 4. Features & Target
X = df[['age', 'education', 'job_level', 'years_at_company',
        'monthly_income', 'job_satisfaction',
        'work_life_balance', 'environment_satisfaction', 'overtime']]
y = df['attrition']

# 5. Train & Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"✅ Train: {len(X_train)} rows, Test: {len(X_test)} rows")

# 6. Model Train
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
print("✅ Model Trained!")

# 7. Predict
y_pred = model.predict(X_test)

# 8. Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\n🎯 Model Accuracy: {accuracy * 100:.2f}%")
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))

# 9. Confusion Matrix Chart
plt.figure(figsize=(6, 5))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Stay', 'Leave'],
            yticklabels=['Stay', 'Leave'])
plt.title('Confusion Matrix', fontsize=14)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.tight_layout()
plt.savefig('outputs/chart4_confusion_matrix.png')
plt.close()
print("✅ Confusion Matrix Saved!")

# 10. Predict New Employee
print("\n🔮 New Employee Prediction:")
new_employee = pd.DataFrame([{
    'age': 28,
    'education': 2,
    'job_level': 1,
    'years_at_company': 2,
    'monthly_income': 3000,
    'job_satisfaction': 2,
    'work_life_balance': 2,
    'environment_satisfaction': 2,
    'overtime': 1
}])

result = model.predict(new_employee)
probability = model.predict_proba(new_employee)

if result[0] == 1:
    print(f"⚠️  இந்த Employee QUIT பண்ணுவாங்க!")
else:
    print(f"✅ இந்த Employee STAY பண்ணுவாங்க!")

print(f"📈 Quit Probability: {probability[0][1]*100:.2f}%")
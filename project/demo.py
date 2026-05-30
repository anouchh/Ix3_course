import requests

BASE_URL = "http://localhost:8000"

# Тестовый сотрудник — высокий риск
high_risk = {
    "Age": 28,
    "BusinessTravel": "Travel_Frequently",
    "DailyRate": 500,
    "Department": "Sales",
    "DistanceFromHome": 25,
    "Education": 2,
    "EducationField": "Life Sciences",
    "EnvironmentSatisfaction": 1,
    "Gender": "Male",
    "HourlyRate": 40,
    "JobInvolvement": 2,
    "JobLevel": 1,
    "JobRole": "Sales Representative",
    "JobSatisfaction": 1,
    "MaritalStatus": "Single",
    "MonthlyIncome": 2500,
    "MonthlyRate": 5000,
    "NumCompaniesWorked": 5,
    "OverTime": "Yes",
    "PercentSalaryHike": 11,
    "PerformanceRating": 3,
    "RelationshipSatisfaction": 2,
    "StockOptionLevel": 0,
    "TotalWorkingYears": 3,
    "TrainingTimesLastYear": 1,
    "WorkLifeBalance": 1,
    "YearsAtCompany": 1,
    "YearsInCurrentRole": 0,
    "YearsSinceLastPromotion": 0,
    "YearsWithCurrManager": 0
}

# Тестовый сотрудник — низкий риск
low_risk = {
    "Age": 45,
    "BusinessTravel": "Non-Travel",
    "DailyRate": 1200,
    "Department": "Research & Development",
    "DistanceFromHome": 2,
    "Education": 4,
    "EducationField": "Medical",
    "EnvironmentSatisfaction": 4,
    "Gender": "Female",
    "HourlyRate": 90,
    "JobInvolvement": 4,
    "JobLevel": 4,
    "JobRole": "Manager",
    "JobSatisfaction": 4,
    "MaritalStatus": "Married",
    "MonthlyIncome": 12000,
    "MonthlyRate": 20000,
    "NumCompaniesWorked": 1,
    "OverTime": "No",
    "PercentSalaryHike": 18,
    "PerformanceRating": 4,
    "RelationshipSatisfaction": 4,
    "StockOptionLevel": 3,
    "TotalWorkingYears": 20,
    "TrainingTimesLastYear": 3,
    "WorkLifeBalance": 4,
    "YearsAtCompany": 15,
    "YearsInCurrentRole": 8,
    "YearsSinceLastPromotion": 2,
    "YearsWithCurrManager": 7
}

def check_employee(employee: dict, label: str):
    response = requests.post(f"{BASE_URL}/predict", json=employee)
    result = response.json()
    print(f"\n{label}")
    print(f"  Вероятность увольнения: {result['attrition_probability']:.1%}")
    print(f"  Уровень риска: {result['risk_level']}")

# Health check
health = requests.get(f"{BASE_URL}/health")
print(f"Статус сервиса: {health.json()['status']}")

check_employee(high_risk, "Сотрудник в зоне риска:")
check_employee(low_risk, "Стабильный сотрудник:")
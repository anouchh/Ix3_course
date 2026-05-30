import pytest
from fastapi.testclient import TestClient
from src.service.app import app

client = TestClient(app)

VALID_EMPLOYEE = {
    "Age": 34,
    "BusinessTravel": "Travel_Rarely",
    "DailyRate": 1102,
    "Department": "Sales",
    "DistanceFromHome": 1,
    "Education": 3,
    "EducationField": "Life Sciences",
    "EnvironmentSatisfaction": 2,
    "Gender": "Male",
    "HourlyRate": 65,
    "JobInvolvement": 3,
    "JobLevel": 2,
    "JobRole": "Sales Executive",
    "JobSatisfaction": 3,
    "MaritalStatus": "Married",
    "MonthlyIncome": 5993,
    "MonthlyRate": 19479,
    "NumCompaniesWorked": 3,
    "OverTime": "Yes",
    "PercentSalaryHike": 11,
    "PerformanceRating": 3,
    "RelationshipSatisfaction": 3,
    "StockOptionLevel": 1,
    "TotalWorkingYears": 10,
    "TrainingTimesLastYear": 2,
    "WorkLifeBalance": 3,
    "YearsAtCompany": 4,
    "YearsInCurrentRole": 3,
    "YearsSinceLastPromotion": 2,
    "YearsWithCurrManager": 3
}


def test_health():
    """Сервис живой"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_valid_input():
    """Корректный запрос возвращает 200 и нужные поля"""
    response = client.post("/predict", json=VALID_EMPLOYEE)
    assert response.status_code == 200
    data = response.json()
    assert "attrition_probability" in data
    assert "risk_level" in data


def test_predict_probability_range():
    """Вероятность всегда между 0 и 1"""
    response = client.post("/predict", json=VALID_EMPLOYEE)
    prob = response.json()["attrition_probability"]
    assert 0.0 <= prob <= 1.0


def test_predict_risk_levels():
    """Уровень риска всегда один из трёх допустимых"""
    response = client.post("/predict", json=VALID_EMPLOYEE)
    risk = response.json()["risk_level"]
    assert risk in ["low", "medium", "high"]


def test_predict_invalid_input():
    """Некорректные данные возвращают 422"""
    response = client.post("/predict", json={"Age": "не число"})
    assert response.status_code == 422
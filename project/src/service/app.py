import os
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from src.models.predictor import AttritionPredictor
from src.data.preprocessor import preprocess_input

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(title='HR Attrition API')
predictor = AttritionPredictor()


class EmployeeFeatures(BaseModel):
    Age: int
    BusinessTravel: str
    DailyRate: int
    Department: str
    DistanceFromHome: int
    Education: int
    EducationField: str
    EnvironmentSatisfaction: int
    Gender: str
    HourlyRate: int
    JobInvolvement: int
    JobLevel: int
    JobRole: str
    JobSatisfaction: int
    MaritalStatus: str
    MonthlyIncome: int
    MonthlyRate: int
    NumCompaniesWorked: int
    OverTime: str
    PercentSalaryHike: int
    PerformanceRating: int
    RelationshipSatisfaction: int
    StockOptionLevel: int
    TotalWorkingYears: int
    TrainingTimesLastYear: int
    WorkLifeBalance: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsSinceLastPromotion: int
    YearsWithCurrManager: int


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.post('/predict')
def predict(employee: EmployeeFeatures):
    logger.info(f'Запрос на предсказание: {employee.model_dump()}')
    
    df = preprocess_input(employee.model_dump())
    result = predictor.predict(df)
    
    logger.info(f'Результат: {result}')
    return result
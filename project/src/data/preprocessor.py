import pandas as pd
from sklearn.preprocessing import LabelEncoder

COLUMNS_TO_DROP = ['EmployeeCount', 'Over18', 'StandardHours', 'EmployeeNumber']

CAT_COLUMNS = [
    'Attrition', 'BusinessTravel', 'Department', 'EducationField',
    'Gender', 'JobRole', 'MaritalStatus', 'OverTime'
]

# Фиксированные маппинги — важно чтобы кодировка была одинаковой всегда
CAT_MAPPINGS = {
    'BusinessTravel': {'Non-Travel': 0, 'Travel_Frequently': 1, 'Travel_Rarely': 2},
    'Department': {'Human Resources': 0, 'Research & Development': 1, 'Sales': 2},
    'EducationField': {'Human Resources': 0, 'Life Sciences': 1, 'Marketing': 2,
                       'Medical': 3, 'Other': 4, 'Technical Degree': 5},
    'Gender': {'Female': 0, 'Male': 1},
    'JobRole': {'Healthcare Representative': 0, 'Human Resources': 1,
                'Laboratory Technician': 2, 'Manager': 3,
                'Manufacturing Director': 4, 'Research Director': 5,
                'Research Scientist': 6, 'Sales Executive': 7,
                'Sales Representative': 8},
    'MaritalStatus': {'Divorced': 0, 'Married': 1, 'Single': 2},
    'OverTime': {'No': 0, 'Yes': 1},
}

def preprocess_input(data: dict) -> pd.DataFrame:
    """Принимает словарь с признаками, возвращает DataFrame готовый для модели"""
    df = pd.DataFrame([data])

    # Кодируем категориальные признаки по фиксированным маппингам
    for col, mapping in CAT_MAPPINGS.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)

    return df
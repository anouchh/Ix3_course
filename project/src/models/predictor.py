import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).parent.parent.parent / 'artifacts' / 'model.pkl'

class AttritionPredictor:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def predict(self, df: pd.DataFrame) -> dict:
        proba = self.model.predict_proba(df)[:, 1][0]

        if proba >= 0.6:
            risk = 'high'
        elif proba >= 0.35:
            risk = 'medium'
        else:
            risk = 'low'

        return {
            'attrition_probability': round(float(proba), 3),
            'risk_level': risk
        }
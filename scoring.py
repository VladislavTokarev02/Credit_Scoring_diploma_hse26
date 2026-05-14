#!/usr/bin/env python3

import joblib
import pandas as pd


class CreditScoringService:

    def __init__(self, model_path: str, threshold: float):

        self.model = joblib.load(model_path)
        self.threshold = threshold

    def predict(self, features: dict):

        df = pd.DataFrame([features])

        proba = self.model.predict_proba(df)[0, 1]

        return {
            "probability": round(float(proba), 4),
            "decision": (
                "REJECT"
                if proba >= self.threshold
                else "APPROVE"
            )
        }
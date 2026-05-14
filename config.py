#!/usr/bin/env python3

from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GIGACHAT_CREDENTIALS = os.getenv("AUTH")

MODEL_PATH = "credit_scoring_pipeline.joblib"
THRESHOLD = 0.77

FEATURES = [
    "age",
    "MonthlyIncome",
    "DebtRatio",
    "NumberOfDependents",
    "RevolvingUtilizationOfUnsecuredLines",
    "NumberOfTime30-59DaysPastDueNotWorse",
    "NumberOfTime60-89DaysPastDueNotWorse",
    "NumberOfTimes90DaysLate",
    "NumberRealEstateLoansOrLines"
]


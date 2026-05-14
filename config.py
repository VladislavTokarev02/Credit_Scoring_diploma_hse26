#!/usr/bin/env python3

from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GIGACHAT_CREDENTIALS = os.getenv("GIGACHAT_CREDENTIALS")

MODEL_PATH = "credit_scoring_pipeline.joblib"

THRESHOLD = 0.77
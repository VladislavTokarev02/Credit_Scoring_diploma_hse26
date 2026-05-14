#!/usr/bin/env python3

import json
from gigachat import GigaChat
from gigachat.models import Chat, Messages

from config import GIGACHAT_CREDENTIALS


class GigaChatService:

    def __init__(self):

        self.client = GigaChat(
            credentials=GIGACHAT_CREDENTIALS,
            verify_ssl_certs=False
        )

    def extract_features(self, text: str):

        prompt = f"""
Извлеки из текста клиента JSON:

{{
  "age": int,
  "MonthlyIncome": float,
  "DebtRatio": float,
  "NumberOfDependents": int,
  "RevolvingUtilizationOfUnsecuredLines": float,
  "NumberOfTime30-59DaysPastDueNotWorse": int,
  "NumberOfTime60-89DaysPastDueNotWorse": int,
  "NumberOfTimes90DaysLate": int,
  "NumberRealEstateLoansOrLines": int
}}

Если значения нет — ставь null.

Текст клиента:
{text}
"""

        response = self.client.chat(
            Chat(
                messages=[
                    Messages(
                        role="user",
                        content=prompt
                    )
                ]
            )
        )

        content = response.choices[0].message.content

        return json.loads(content)

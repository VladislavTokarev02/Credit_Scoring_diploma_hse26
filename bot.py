#!/usr/bin/env python3

import asyncio
import json

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN, MODEL_PATH, THRESHOLD
from scoring import CreditScoringService
from services.gigachat_service import GigaChatService


bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()
router = Router()

dp.include_router(router)

scoring = CreditScoringService(
    MODEL_PATH,
    THRESHOLD
)

giga = GigaChatService()


@router.message(CommandStart())
async def start(message: Message):

    await message.answer(
        """
Отправьте информацию о клиенте одним сообщением.

Например:

Возраст 35 лет
Доход 120000
2 иждивенца
Debt ratio 0.45
Просрочки:
30-59: 1
60-89: 0
90+: 0
Недвижимость: 1
Кредитная нагрузка: 0.7
"""
    )


@router.message()
async def scoring_handler(message: Message):

    try:

        features = giga.extract_features(
            message.text
        )

        missing = [
            k for k, v in features.items()
            if v is None
        ]

        if missing:

            await message.answer(
                f"""
Не удалось определить поля:

{', '.join(missing)}

Пожалуйста, укажите их явно.
"""
            )

            return

        result = scoring.predict(features)

        await message.answer(
            f"""
<b>Результат скоринга</b>

Probability of default: <b>{result['probability']:.4f}</b>

Decision: <b>{result['decision']}</b>
"""
        )

    except json.JSONDecodeError:

        await message.answer(
            "Ошибка обработки данных GigaChat."
        )

    except Exception as e:

        await message.answer(
            f"Ошибка: {str(e)}"
        )


async def main():

    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())
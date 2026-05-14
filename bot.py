#!/usr/bin/env python3

import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN, MODEL_PATH, THRESHOLD
from scoring import CreditScoringService


bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher(storage=MemoryStorage())
router = Router()

dp.include_router(router)

scoring = CreditScoringService(MODEL_PATH, THRESHOLD)


class CreditForm(StatesGroup):
    age = State()
    income = State()
    debt = State()
    dependents = State()
    revol = State()
    dpd1 = State()
    dpd2 = State()
    dpd3 = State()
    real_estate = State()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(CreditForm.age)
    await message.answer("Введите возраст:")


@router.message(CreditForm.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=float(message.text))
    await state.set_state(CreditForm.income)
    await message.answer("Введите доход:")


@router.message(CreditForm.income)
async def income(message: Message, state: FSMContext):
    await state.update_data(MonthlyIncome=float(message.text))
    await state.set_state(CreditForm.debt)
    await message.answer("Debt Ratio:")


@router.message(CreditForm.debt)
async def debt(message: Message, state: FSMContext):
    await state.update_data(DebtRatio=float(message.text))
    await state.set_state(CreditForm.dependents)
    await message.answer("Иждивенцы:")


@router.message(CreditForm.dependents)
async def dep(message: Message, state: FSMContext):
    await state.update_data(NumberOfDependents=float(message.text))
    await state.set_state(CreditForm.revol)
    await message.answer("Revolving Utilization:")


@router.message(CreditForm.revol)
async def revol(message: Message, state: FSMContext):
    await state.update_data(RevolvingUtilizationOfUnsecuredLines=float(message.text))
    await state.set_state(CreditForm.dpd1)
    await message.answer("Просрочка 30-59:")


@router.message(CreditForm.dpd1)
async def dpd1(message: Message, state: FSMContext):
    await state.update_data(NumberOfTime30_59DaysPastDueNotWorse=float(message.text))
    await state.set_state(CreditForm.dpd2)
    await message.answer("Просрочка 60-89:")


@router.message(CreditForm.dpd2)
async def dpd2(message: Message, state: FSMContext):
    await state.update_data(NumberOfTime60_89DaysPastDueNotWorse=float(message.text))
    await state.set_state(CreditForm.dpd3)
    await message.answer("Просрочка 90+:")


@router.message(CreditForm.dpd3)
async def dpd3(message: Message, state: FSMContext):
    await state.update_data(NumberOfTimes90DaysLate=float(message.text))
    await state.set_state(CreditForm.real_estate)
    await message.answer("Недвижимость:")


@router.message(CreditForm.real_estate)
async def final(message: Message, state: FSMContext):

    data = await state.get_data()
    data["NumberRealEstateLoansOrLines"] = float(message.text)

    result = scoring.predict(data)

    await message.answer(
        f"Probability: {result['probability']:.2f}\nDecision: {result['decision']}"
    )

    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
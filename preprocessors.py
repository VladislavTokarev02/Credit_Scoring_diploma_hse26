#!/usr/bin/env python3

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class CreditScoringPreprocessor(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.columns = None

    def fit(self, X, y=None):
        self.columns = X.columns.tolist()
        return self

    def transform(self, X):

        X = pd.DataFrame(X, columns=self.columns).copy()

        debt = X["DebtRatio"]

        X.loc[(debt >= 2) & (debt < 10), "DebtRatio"] /= 10
        X.loc[(debt >= 10) & (debt < 100), "DebtRatio"] /= 100
        X.loc[(debt >= 100) & (debt < 1000), "DebtRatio"] /= 1000

        X["age"] = X["age"].clip(18, 93)
        X["MonthlyIncome"] = X["MonthlyIncome"].clip(upper=100000)

        X["RevolvingUtilizationOfUnsecuredLines"] = X["RevolvingUtilizationOfUnsecuredLines"].clip(0, 2)

        X["NumberOfTime30-59DaysPastDueNotWorse"] = X["NumberOfTime30-59DaysPastDueNotWorse"].clip(0, 8)
        X["NumberOfTime60-89DaysPastDueNotWorse"] = X["NumberOfTime60-89DaysPastDueNotWorse"].clip(0, 6)
        X["NumberOfTimes90DaysLate"] = X["NumberOfTimes90DaysLate"].clip(0, 4)
        X["NumberRealEstateLoansOrLines"] = X["NumberRealEstateLoansOrLines"].clip(0, 10)
        X["NumberOfDependents"] = X["NumberOfDependents"].clip(0, 6)

        return X
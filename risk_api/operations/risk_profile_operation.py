#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List
from risk_api.constants import Constants as c

class RiskProfileOperation:
    def __init__(self, user_data):
        self.user_data = user_data
        self.risk_report = {key:'' for key in c.INS_TYPES}
        base_score = self._base_score
        self.risk_score =  [
            base_score, #auto
            base_score, #disability
            base_score, #home
            base_score, #life
        ]

    def run(self):
        self._set_eligibility()
        self._apply_global_factors()
        self._apply_local_factors() 
        self._set_final_report()
        return self.risk_report

    def _set_eligibility(self):
        under_60 = self.user_data[c.DATA_AGE] < c.AGE_RANGE_3
        self.risk_report = {
            c.INS_TYPES[c.KEY_AUTO]: self._is_elegible(self.user_data[c.DATA_VEHICLE]),
            c.INS_TYPES[c.KEY_DISABILITY]: self._is_elegible(self.user_data[c.DATA_INCOME], under_60),
            c.INS_TYPES[c.KEY_HOME]: self._is_elegible(self.user_data[c.DATA_HOUSE]),
            c.INS_TYPES[c.KEY_LIFE]: self._is_elegible(under_60),
        }

    def _is_elegible(self, *args) -> str:
        """
            A user must have every item in args
            to be eligible.
            Otherwise, returns INELEGIBLE
        """
        if all(args):
            return ""
        return c.PLAN_INELEGIBLE

    def _suggest_plan(self, key) -> str:
        if self.risk_score[key] < 1:
            return c.PLAN_ECONOMIC
        if self.risk_score[key] < 3:
            return c.PLAN_REGULAR
        return c.PLAN_RESPONSIBLE

    @property
    def _base_score(self) -> int:
        return sum(self.user_data[c.DATA_RISK_QUESTIONS])

    @property
    def _age_factor(self) -> int:
        if self.user_data[c.DATA_AGE] < c.AGE_RANGE_1:
            return -2
        elif self.user_data['age'] <= c.AGE_RANGE_2:
            return -1
        return 0

    @property
    def _income_factor(self) -> int:
        if self.user_data[c.DATA_INCOME] > c.INCOME_THRESHOLD:
            return -1
        return 0

    def _apply_global_factors(self):
        """
        Apply factors that affect all plans globally
        """
        age_factor = self._age_factor
        income_factor = self._income_factor
        self.risk_score = [sum([x,age_factor,income_factor]) for x in self.risk_score]

    def _apply_local_factors(self):
        """
        Apply factors that only impact certain insurance plans
        """
        self._apply_house_factor()
        self._apply_dependents_factor()
        self._apply_married_factor()
        self._apply_vehicle_factor()

    def _set_final_report(self):
        for ins_key, insurance_type in enumerate(c.INS_TYPES):
            if self.risk_report[insurance_type] != c.PLAN_INELEGIBLE:
                self.risk_report[insurance_type] = self._suggest_plan(ins_key)

    def _modify_score_points(self, key, points):
        """
        Alter the score of plan with key by a certain amount of points
        """
        self.risk_score[key] += points

    def _apply_house_factor(self):
        if self.user_data[c.DATA_HOUSE] and \
                self.user_data[c.DATA_HOUSE][c.DATA_OWNERSHIP_STATUS] == c.MORTGAGED:
            self._modify_score_points(c.KEY_HOME, 1)
            self._modify_score_points(c.KEY_DISABILITY, 1)

    def _apply_dependents_factor(self):
        if self.user_data[c.DATA_DEPENDENTS] > 0:
            self._modify_score_points(c.KEY_DISABILITY, 1)
            self._modify_score_points(c.KEY_LIFE, 1)

    def _apply_married_factor(self):
        if self.user_data[c.DATA_MARITAL_STATUS] == c.MARRIED:
            self._modify_score_points(c.KEY_LIFE, 1)
            self._modify_score_points(c.KEY_DISABILITY, -1)

    def _apply_vehicle_factor(self):
        if self.user_data[c.DATA_VEHICLE]:
            currentYear = datetime.now().year
            if abs(self.user_data[c.DATA_VEHICLE][c.DATA_V_YEAR] - currentYear) <= 5:
                self._modify_score_points(c.KEY_AUTO, 1)

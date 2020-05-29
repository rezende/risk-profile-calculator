import json
import operator
from datetime import datetime
import falcon
from .constants import Constants as c


def validate_data(req, resp, resource, params):
    for r_field in c.REQUIRED_FIELDS:
        if r_field not in req.media.keys():
            msg = f'{r_field} field required'
            raise falcon.HTTPBadRequest('Bad request', msg)


class RiskProfileResource:
    def _is_elegible(self, *args):
        """
            A user must have every item in args
            to be eligible.
            Otherwise, returns INELEGIBLE
        """
        for a in args:
            if not a:
                return c.PLAN_INELEGIBLE
        return ""

    def _calculate_report(self, key, score_data):
        if score_data[key] < 0:
            return c.PLAN_ECONOMIC
        if score_data[key] < 3:
            return c.PLAN_REGULAR
        return c.PLAN_RESPONSIBLE

    @falcon.before(validate_data)
    def on_post(self, req, resp):
        user_data = req.media
        base_score = sum(user_data['risk_questions'])

        risk_score =  [
            base_score, #auto
            base_score, #disability
            base_score, #home
            base_score, #life
        ]

        vehicle = user_data['vehicle']
        income = user_data['income']
        house = user_data['house']
        under_60 = user_data['age'] < c.AGE_RANGE_3

        risk_report =  {
            c.INS_TYPES[c.KEY_AUTO]: self._is_elegible(vehicle),
            c.INS_TYPES[c.KEY_DISABILITY]: self._is_elegible(income, under_60),
            c.INS_TYPES[c.KEY_HOME]: self._is_elegible(house),
            c.INS_TYPES[c.KEY_LIFE]: self._is_elegible(under_60),
        }
        
        # age_factor
        age_factor = 0
        if user_data[c.DATA_AGE] < c.AGE_RANGE_1:
            age_factor = -2
        elif user_data['age'] < c.AGE_RANGE_2:
            age_factor = -1

        # income_factor
        income_factor = 0
        if user_data[c.DATA_INCOME] > c.INCOME_THRESHOLD:
           income_factor = -1

        risk_score = [sum([x,age_factor,income_factor]) for x in risk_score]

        # house_factor
        if house and house[c.DATA_OWNERSHIP_STATUS] == c.DATA_OS_MORTGAGED:
            risk_score[c.KEY_HOME] += 1
            risk_score[c.KEY_DISABILITY] += 1

        # dependents_factor
        if user_data[c.DATA_DEPENDENTS] > 0:
            risk_score[c.KEY_DISABILITY] += 1
            risk_score[c.KEY_LIFE] += 1

        # married_factor
        if user_data[c.DATA_MARITAL_STATUS] == c.DATA_MS_MARRIED:
            risk_score[c.KEY_LIFE] += 1
            risk_score[c.KEY_DISABILITY] -= 1

        # vehicle_factor
        if vehicle:
            currentYear = datetime.now().year
            if operator.abs(operator.sub(vehicle[c.DATA_V_YEAR], currentYear)) <= 5:
                risk_score[c.KEY_AUTO] += 1

        for key, value in enumerate(c.INS_TYPES):
            if risk_report[value] != c.PLAN_INELEGIBLE:
                risk_report[value] = self._calculate_report(key, risk_score)

        resp.body = json.dumps(risk_report)

#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pytest
from datetime import datetime

from risk_api.constants import Constants as c
from risk_api.operations import RiskProfileOperation


@pytest.fixture
def base_data():
    return {
      c.DATA_AGE: 35,
      c.DATA_DEPENDENTS: 2,
      c.DATA_HOUSE: {c.DATA_OWNERSHIP_STATUS: c.OWNED},
      c.DATA_INCOME: 0,
      c.DATA_MARITAL_STATUS: c.MARRIED,
      c.DATA_RISK_QUESTIONS: [0, 1, 0],
      c.DATA_VEHICLE: {c.DATA_V_YEAR: 2011}
    }

def test_base_score_2(base_data):
    base_data['risk_questions'] = [0,1,1]
    op = RiskProfileOperation(base_data)
    assert op._base_score == 2
    for sc in op.risk_score:
        assert sc == 2

def test_base_score_3(base_data):
    base_data['risk_questions'] = [1,1,1]
    op = RiskProfileOperation(base_data)
    assert op._base_score == 3
    for sc in op.risk_score:
        assert sc == 3

def test_is_eligible(base_data):
    op = RiskProfileOperation(base_data)
    assert op._is_elegible(True, True) == ''
    assert op._is_elegible(False, False) == 'inelegible'
    assert op._is_elegible(True, False) == 'inelegible'

def test_age_factor(base_data):
    base_data['age'] = -5 # < 0
    assert RiskProfileOperation(base_data)._age_factor == -2
    base_data['age'] = 0 # = 0
    assert RiskProfileOperation(base_data)._age_factor == -2
    base_data['age'] = 29 # < 30
    assert RiskProfileOperation(base_data)._age_factor == -2
    base_data['age'] = 30 # 30-40
    assert RiskProfileOperation(base_data)._age_factor == -1
    base_data['age'] = 40 # 30-40
    assert RiskProfileOperation(base_data)._age_factor == -1
    base_data['age'] = 41 # > 40
    assert RiskProfileOperation(base_data)._age_factor == 0

def test_income_factor(base_data):
    base_data[c.DATA_INCOME] = -5 # < 0
    assert RiskProfileOperation(base_data)._income_factor == 0
    base_data[c.DATA_INCOME] = 0 # = 0
    assert RiskProfileOperation(base_data)._income_factor == 0
    base_data[c.DATA_INCOME] = 200000 # == THRESHOLD
    assert RiskProfileOperation(base_data)._income_factor == 0
    base_data[c.DATA_INCOME] = 200001 # > THRESHOLD
    assert RiskProfileOperation(base_data)._income_factor == -1

def test_apply_local_factors(base_data, mocker):
    m_house = mocker.patch.object(RiskProfileOperation, '_apply_house_factor')
    m_dependents = mocker.patch.object(RiskProfileOperation, '_apply_dependents_factor')
    m_married = mocker.patch.object(RiskProfileOperation, '_apply_married_factor')
    m_vehicle = mocker.patch.object(RiskProfileOperation, '_apply_vehicle_factor')

    RiskProfileOperation(base_data)._apply_local_factors()

    m_house.assert_called()
    m_dependents.assert_called()
    m_married.assert_called()
    m_vehicle.assert_called()

def test_apply_global_factors_for_base_data(base_data, mocker):
    op = RiskProfileOperation(base_data)
    assert op.risk_score == [1,1,1,1]
    assert op._age_factor == -1
    assert op._income_factor == 0
    op._apply_global_factors()
    assert op.risk_score == [0,0,0,0]

def test_apply_global_factors_young_and_rich(base_data, mocker):
    base_data['age'] = 25
    base_data['income'] = 300000
    op = RiskProfileOperation(base_data)
    assert op.risk_score == [1,1,1,1]
    assert op._age_factor == -2
    assert op._income_factor == -1
    op._apply_global_factors()
    assert op.risk_score == [-2,-2,-2,-2]

def test_run(base_data, mocker):
    op = RiskProfileOperation(base_data)
    m_eligibility = mocker.spy(op, '_set_eligibility')
    m_global = mocker.spy(op, '_apply_global_factors')
    m_local = mocker.spy(op, '_apply_local_factors') 
    m_final = mocker.spy(op, '_set_final_report')

    report = op.run()
    
    m_eligibility.assert_called()
    m_global.assert_called()
    m_local.assert_called()
    m_final.assert_called()
    assert report[c.INS_AUTO] == 'economic'
    assert report[c.INS_DISABILITY] == 'inelegible'
    assert report[c.INS_HOME] == 'economic'
    assert report[c.INS_LIFE] == 'regular'

def test_house_factor_owned(base_data):
    op = RiskProfileOperation(base_data)
    assert op.risk_score == [1,1,1,1]
    op._apply_house_factor()
    assert op.risk_score == [1,1,1,1]

def test_house_factor_mortgaged(base_data):
    base_data[c.DATA_HOUSE] = {c.DATA_OWNERSHIP_STATUS: c.MORTGAGED}
    op = RiskProfileOperation(base_data)
    assert op.risk_score[c.KEY_AUTO] == 1
    assert op.risk_score[c.KEY_DISABILITY] == 1
    assert op.risk_score[c.KEY_HOME] == 1
    assert op.risk_score[c.KEY_LIFE] == 1
    op._apply_house_factor()
    assert op.risk_score[c.KEY_AUTO] == 1
    assert op.risk_score[c.KEY_DISABILITY] == 2
    assert op.risk_score[c.KEY_HOME] == 2
    assert op.risk_score[c.KEY_LIFE] == 1

def test_dependents_factor_with_dependents(base_data):
    op = RiskProfileOperation(base_data)
    assert op.risk_score[c.KEY_AUTO] == 1
    assert op.risk_score[c.KEY_DISABILITY] == 1
    assert op.risk_score[c.KEY_HOME] == 1
    assert op.risk_score[c.KEY_LIFE] == 1
    op._apply_dependents_factor()
    assert op.risk_score[c.KEY_AUTO] == 1
    assert op.risk_score[c.KEY_DISABILITY] == 2
    assert op.risk_score[c.KEY_HOME] == 1
    assert op.risk_score[c.KEY_LIFE] == 2

def test_dependents_factor_no_dependents(base_data):
    base_data[c.DATA_DEPENDENTS] = 0
    op = RiskProfileOperation(base_data)
    assert op.risk_score == [1,1,1,1]
    op._apply_dependents_factor()
    assert op.risk_score == [1,1,1,1]

def test_married_factor_married(base_data):
    op = RiskProfileOperation(base_data)
    assert op.risk_score[c.KEY_AUTO] == 1
    assert op.risk_score[c.KEY_DISABILITY] == 1
    assert op.risk_score[c.KEY_HOME] == 1
    assert op.risk_score[c.KEY_LIFE] == 1
    op._apply_married_factor()
    assert op.risk_score[c.KEY_AUTO] == 1
    assert op.risk_score[c.KEY_DISABILITY] == 0
    assert op.risk_score[c.KEY_HOME] == 1
    assert op.risk_score[c.KEY_LIFE] == 2

def test_married_factor_single(base_data):
    base_data[c.DATA_MARITAL_STATUS] = c.SINGLE
    op = RiskProfileOperation(base_data)
    assert op.risk_score == [1,1,1,1]
    op._apply_married_factor()
    assert op.risk_score == [1,1,1,1]

def test_vehicle_factor_recent_vehicle(base_data):
    base_data[c.DATA_VEHICLE] = {c.DATA_V_YEAR: datetime.now().year}
    op = RiskProfileOperation(base_data)
    assert op.risk_score[c.KEY_AUTO] == 1
    assert op.risk_score[c.KEY_DISABILITY] == 1
    assert op.risk_score[c.KEY_HOME] == 1
    assert op.risk_score[c.KEY_LIFE] == 1
    op._apply_vehicle_factor()
    assert op.risk_score[c.KEY_AUTO] == 2
    assert op.risk_score[c.KEY_DISABILITY] == 1
    assert op.risk_score[c.KEY_HOME] == 1
    assert op.risk_score[c.KEY_LIFE] == 1

def test_vehicle_factor_old_vehicle(base_data):
    op = RiskProfileOperation(base_data)
    assert op.risk_score == [1,1,1,1]
    op._apply_vehicle_factor()
    assert op.risk_score == [1,1,1,1]

def test_suggest_plan(base_data):
    op = RiskProfileOperation(base_data)
    op.risk_score[c.KEY_AUTO] = -15
    assert op._suggest_plan(c.KEY_AUTO) == 'economic'
    op.risk_score[c.KEY_AUTO] = 0
    assert op._suggest_plan(c.KEY_AUTO) == 'economic'
    op.risk_score[c.KEY_AUTO] = 1
    assert op._suggest_plan(c.KEY_AUTO) == 'regular'
    op.risk_score[c.KEY_AUTO] = 2
    assert op._suggest_plan(c.KEY_AUTO) == 'regular'
    op.risk_score[c.KEY_AUTO] = 3
    assert op._suggest_plan(c.KEY_AUTO) == 'responsible'
    op.risk_score[c.KEY_AUTO] = 44
    assert op._suggest_plan(c.KEY_AUTO) == 'responsible'

def test_set_final_report_does_not_override_inelegible_plans(base_data):
    op = RiskProfileOperation(base_data)
    op._set_final_report()
    assert op.risk_report[c.INS_AUTO] == 'regular'

    op.risk_report[c.INS_AUTO] = c.PLAN_INELEGIBLE
    op.risk_report[c.INS_DISABILITY] = c.PLAN_INELEGIBLE
    op._set_final_report()
    assert op.risk_report[c.INS_AUTO] == 'inelegible'
    assert op.risk_report[c.INS_DISABILITY] == 'inelegible'


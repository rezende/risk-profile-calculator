class Constants:
    # user_data
    DATA_AGE = "age"
    DATA_DEPENDENTS = "dependents"
    DATA_HOUSE = "house"
    DATA_INCOME = "income"
    DATA_MARITAL_STATUS = "marital_status"
    DATA_MS_SINGLE = "single"
    DATA_MS_MARRIED = "married"
    DATA_RISK_QUESTIONS = "risk_questions"
    DATA_VEHICLE = "vehicle"
    DATA_V_YEAR = "year"
    DATA_OWNERSHIP_STATUS = "ownership_status"
    DATA_OS_OWNED = "owned"
    DATA_OS_MORTGAGED = "mortgaged"
    REQUIRED_FIELDS = [
        DATA_AGE,
        DATA_DEPENDENTS,
        DATA_HOUSE,
        DATA_INCOME,
        DATA_MARITAL_STATUS,
        DATA_RISK_QUESTIONS,
        DATA_VEHICLE
    ]

    # risk_score
    KEY_AUTO = 0
    KEY_DISABILITY =1
    KEY_HOME = 2
    KEY_LIFE = 3
    INCOME_THRESHOLD = 200000
    AGE_RANGE_1 = 30
    AGE_RANGE_2 = 40
    AGE_RANGE_3 = 60

    #risk_report
    INS_AUTO = "auto"
    INS_DISABILITY = "disability"
    INS_HOME = "home"
    INS_LIFE= "life"

    INS_TYPES = [
        INS_AUTO,
        INS_DISABILITY,
        INS_HOME,
        INS_LIFE
    ]

    PLAN_INELEGIBLE = "inelegible"
    PLAN_ECONOMIC = "economic"
    PLAN_REGULAR = "regular"
    PLAN_RESPONSIBLE = "responsible"

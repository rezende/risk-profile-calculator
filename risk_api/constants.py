class Constants:
    # user_data_keys
    DATA_AGE = "age"
    DATA_DEPENDENTS = "dependents"
    DATA_HOUSE = "house"
    DATA_INCOME = "income"
    DATA_MARITAL_STATUS = "marital_status"
    DATA_RISK_QUESTIONS = "risk_questions"
    DATA_V_YEAR = "year"
    DATA_VEHICLE = "vehicle"
    DATA_OWNERSHIP_STATUS = "ownership_status"
    REQUIRED_FIELDS = [
        DATA_AGE,
        DATA_DEPENDENTS,
        DATA_HOUSE,
        DATA_INCOME,
        DATA_MARITAL_STATUS,
        DATA_RISK_QUESTIONS,
        DATA_VEHICLE
    ]

    # user_data_values
    SINGLE = "single"
    MARRIED = "married"
    OWNED = "owned"
    MORTGAGED = "mortgaged"

    # business rules
    INCOME_THRESHOLD = 200000
    AGE_RANGE_1 = 30
    AGE_RANGE_2 = 40
    AGE_RANGE_3 = 60
    CAR_DEPRECATION = 5

    # insurance lines
    INS_AUTO = "auto"
    INS_DISABILITY = "disability"
    INS_HOME = "home"
    INS_LIFE= "life"

    # insurance score positions
    KEY_AUTO = 0
    KEY_DISABILITY =1
    KEY_HOME = 2
    KEY_LIFE = 3
    INS_TYPES = [
        INS_AUTO,
        INS_DISABILITY,
        INS_HOME,
        INS_LIFE
    ]

    # plan types
    PLAN_INELEGIBLE = "inelegible"
    PLAN_ECONOMIC = "economic"
    PLAN_REGULAR = "regular"
    PLAN_RESPONSIBLE = "responsible"

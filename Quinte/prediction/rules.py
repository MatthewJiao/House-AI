import pandas as pd
import numpy as np
import preprocessing
import const
# Dataframe = pd.DataFrame

#pt_identifier time BP1 BP2 Pulse Temp	RR O2Sat Age_Number Gender Lactate_value Lactate_ref_range  WBC_value WBC_ref_range
# A1B2C3, 0, 100, 80, 65, 37, 20, 100, 15, Male, 3, 2-5, 5, 4-11
def master_rules(dict_of_lists, curr) -> bool:
    # print("rule")
    # for s in dict_of_lists:
    #     print(s)
    if age_rule(dict_of_lists, curr) == True: 
        return True

    elif rr_and_bp_rule(dict_of_lists, curr) == True: #mayo clinic
        return True
    #rule 2
    #rule 3
    return False


def age_rule(input, curr) -> bool:
    age = int(input["age_number"][curr])
    if age<=16:
        print("Too Young for Prediction!")
        return True
    else:
        return False

def rr_and_bp_rule(input, curr) -> bool:
    curr_rr = int(input["rr"][curr])
    curr_bp = int(input["bp1"][curr])

    if curr_rr>=const.RR_LIMIT and curr_bp<=const.BP1_LIMIT: #relatively high values
        print("Sepsis: RR and BP")
        return True
    else:
        return False


def lactate_rule(input, curr) -> bool:
    curr_lactate = float(input["lactate_adjusted"][curr])

    if curr_lactate > const.LACTATE_ADJUSTED_LIMIT:
        print("Sepsis: Lactate")
        return True

    else:
        return False

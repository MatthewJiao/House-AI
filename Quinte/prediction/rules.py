import pandas as pd
import numpy as np
import preprocessing

Dataframe = pd.DataFrame

#pt_identifier time BP1 BP2 Pulse Temp	RR O2Sat Age_Number Gender Lactate_value Lactate_ref_range  WBC_value WBC_ref_range
# A1B2C3, 0, 100, 80, 65, 37, 20, 100, 15, Male, 3, 2-5, 5, 4-11
def master_rules(list_of_lists, curr) -> bool:
    # print("rule")
    # for s in list_of_lists:
    #     print(s)
    if age_rule(list_of_lists, curr) == True:
        return True
    #rule 2
    #rule 3
    return False


def age_rule(input, curr) -> bool:
    age = int(input[8][curr])
    if age<=16:
        print("Too Young for Prediction!")
        return True
    else:
        return False

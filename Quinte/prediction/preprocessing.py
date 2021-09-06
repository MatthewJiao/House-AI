#preprocess the data

import pandas as pd
import numpy as np

Dataframe = pd.DataFrame


def insert_into_dict(raw_input, dict_of_lists) -> list:
    raw_list = raw_input.split(", ")

    count = 0
    size = len(raw_list)
    for key in dict_of_lists:
        if count<size:
            dict_of_lists[key].append(raw_list[count])
            count+=1

    # print("here")
    # for key in dict_of_lists:
    #     print(key, " ", dict_of_lists[key])
    
    result = ohe_male_female(dict_of_lists)
    result2 = normalize_labs(result)
    return result2

def ohe_male_female(input) -> dict:
    gender = input["gender"][0]

    if gender == "Male":
        input["male"].append(1)
        input["female"].append(0)
    else:
        input["male"].append(0)
        input["female"].append(1)

    input["gender"].pop()

    return input

def normalize_labs(input) -> dict:
    #10-13
    #divide real by high
    lact_val = float(input["lactate_value"][0])
    lact_range = input["lactate_ref_range"][0]
    wbc_val = float(input["wbc_value"][0])
    wbc_range = input["wbc_ref_range"][0]

    lact_high = float(lact_range.split("-")[-1])
    wbc_high = float(wbc_range.split("-")[-1])

    input["lactate_adjusted"].append(float(lact_val/lact_high))
    input["wbc_adjusted"].append(float(wbc_val/wbc_high))

    input["lactate_value"].pop()
    input["lactate_ref_range"].pop()
    input["wbc_value"].pop()
    input["wbc_ref_range"].pop()
    
    return input

def pop_lists(input) -> dict:
    input.pop("gender", None)
    input.pop("lactate_value", None)
    input.pop("lactate_ref_range", None)
    input.pop("wbc_value", None)
    input.pop("wbc_ref_range", None)

    return input
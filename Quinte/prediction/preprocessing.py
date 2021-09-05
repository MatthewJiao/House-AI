#preprocess the data

import pandas as pd
import numpy as np

Dataframe = pd.DataFrame

# def open_test_data(path: str) -> Dataframe:
#     df1 = pd.read_csv(path)
#     #normalize labs
#     #zero the times
#     return df1

# def insert_into_df(raw_input, df_raw) -> Dataframe:
#     # raw_list = raw_input.split(" ")

#     #list of input headers:
#     #pt_identifier	time BP1 BP2 Pulse Temp	RR O2Sat Age_Number Gender Lactate_value Lactate_ref_range  WBC_value WBC_ref_range
#     #list of output headers:
#     #pt_identifier	normalized_time BP1 BP2 Pulse Temp	RR O2Sat Age_Number Male Female Lactate_)adjusted WBC_adjusted
#     #maybe just use a bunch of lists, then concatenate; --> faster
#     pass

def insert_into_arrays(raw_input, list_of_lists) -> list:
    raw_list = raw_input.split(", ")
    
    for idx in range(14):
        list_of_lists[idx].append(raw_list[idx])

    result = ohe_male_female(list_of_lists)
    result2 = normalize_labs(result)
    return result2

def ohe_male_female(input) -> list:
    gender = input[9][0]

    if gender == "Male":
        input[14].append(1)
        input[15].append(0)
    else:
        input[14].append(0)
        input[15].append(1)

    input[9].pop()

    return input

def normalize_labs(input) -> list:
    #10-13
    #divide real by high
    lact_val = float(input[10][0])
    lact_range = input[11][0]
    wbc_val = float(input[12][0])
    wbc_range = input[13][0]

    lact_high = float(lact_range.split("-")[-1])
    wbc_high = float(wbc_range.split("-")[-1])

    input[16].append(float(lact_val/lact_high))
    input[17].append(float(wbc_val/wbc_high))

    input[10].pop()
    input[11].pop()
    input[12].pop()
    input[13].pop()
    
    return input

def pop_lists(input) -> list:
    for i in range(5):
        input.pop(9)

    return input
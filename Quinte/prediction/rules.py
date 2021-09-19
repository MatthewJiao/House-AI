import pandas as pd
import numpy as np
import preprocessing
import const
import math
# Dataframe = pd.DataFrame

#whenever new data entry is inputted, this runs. takes the past hour of info and averages it to compare with pre-decided values

#pt_identifier time BP1 BP2 Pulse Temp	RR O2Sat Age_Number Gender Lactate_value Lactate_ref_range  WBC_value WBC_ref_range
# A1B2C3, 0, 100, 80, 65, 37, 20, 100, 15, Male, 3, 2-5, 5, 4-11
def master_rules(dict_of_lists, curr) -> bool:
    # print("rule")
    # for s in dict_of_lists:
    #     print(s)

    #find indexes of 'curr' for last hour, and store in list
    index_hour = []

    times = (dict_of_lists["time"])
    times = list(map(int, times))
    curr_time = times[curr]

    hour_earlier = curr_time-const.MINUTES_AVERAGE

    if hour_earlier<0:
        hour_earlier = 0

    for idx in range(len(times)):
        if times[idx] >= hour_earlier and times[idx] <= curr_time:
            index_hour.append(idx)

    # print("index_hour", index_hour)

    #auto return rules here
    if age_rule(dict_of_lists, curr) == True: 
        return False
    #elif other auto-return-rule

    #next, a bunch of conditions. if 2 of them are true (1), then we return sepsis. else, none
    lactate = lactate_rule(dict_of_lists, index_hour)
    rr = rr_rule(dict_of_lists, index_hour)
    pulse = pulse_rule(dict_of_lists, index_hour)
    temp = temp_rule(dict_of_lists, index_hour)
    bp1 = bp1_rule(dict_of_lists, index_hour)
    wbc = wbc_rule(dict_of_lists, index_hour)

    total_sum = lactate+rr+pulse+temp+bp1+wbc

    if total_sum >= const.NUM_SATISFIED:
        print("Total Sum Satisfied, ", total_sum)
        return True

    return False


def age_rule(input, curr) -> bool:
    age = input["age_number"][curr]

    if math.isnan(age) == False:
        if age<=const.MIN_AGE:
            # print("Too Young for Prediction!")
            return True
        else:
            return False
    else:
        return False


def lactate_rule(input, index_hour) -> int:
    #if in the past hour, there are any lactate values that are over the limit

    for idx in index_hour:
        lactate_val = float(input["lactate_adjusted"][idx])
        if lactate_val > const.LACTATE_ADJUSTED_LIMIT:
            # print("Lactate Over")
            # print("Lactate value: ", lactate_val)
            return 1
    
    return 0


def rr_rule(input, index_hour) -> int:
    rr_sum = 0
    zero_count = 0
    for idx in index_hour:
        val = input["rr"][idx]
        if val != 0 and math.isnan(val)==False and val != "nan" :
            val = int(val)
            rr_sum = rr_sum + val
        else:
            zero_count+=1
    try:
        rr_average = float(rr_sum/(len(index_hour)-zero_count))
    except:
        return 0

    if rr_average >= const.RR_LIMIT:
        # print("RR OVER")
        # print("rr_average: ", rr_average)
        return 1
    else:
        # print("rr_average: ", rr_average)
        return 0


def pulse_rule(input, index_hour) -> int:
    pulse_sum = 0
    zero_count = 0

    for idx in index_hour:
        val = input["pulse"][idx]
        if val != 0 and math.isnan(val)==False and val != "nan" :
            val = int(val)
            pulse_sum = pulse_sum + val
        else:
            zero_count+=1
    try:
        pulse_average = float(pulse_sum/(len(index_hour)-zero_count))
    except:
        return 0

    if pulse_average >= const.HR_LIMIT:
        # print("PULSE OVER")
        # print("pulse_average: ", pulse_average)
        return 1
    else:
        # print("pulse_average: ", pulse_average)
        return 0


def temp_rule(input, index_hour) -> int:
    temp_sum = 0
    zero_count = 0

    for idx in index_hour:
        val = input["temp"][idx]
        if val != 0 and math.isnan(val)==False and val != "nan" :
            val = int(val)
            temp_sum = temp_sum + val
        else:
            zero_count+=1
    try:
        temp_average = float(temp_sum/(len(index_hour)-zero_count))
    except: 
        return 0

    if temp_average >= const.TEMP_UPPER_LIMIT or temp_average <= const.TEMP_LOWER_LIMIT:
        # print("TEMP OVER/UNDER")
        # print("temp_average: ", temp_average)
        return 1
    else:
        # print("temp_average: ", temp_average)
        return 0


def bp1_rule(input, index_hour) -> int:
    bp1_sum = 0
    zero_count = 0

    for idx in index_hour:
        val = input["bp1"][idx]
        if val != 0 and math.isnan(val)==False and val != "nan" :
            val = int(val)
            bp1_sum = bp1_sum + val
        else:
            zero_count+=1
    try:
        bp1_average = float(bp1_sum/(len(index_hour)-zero_count))
    except:
        return 0

    if bp1_average <= const.BP1_LIMIT:
        # print("BP1 UNDER")
        # print("bp1_average: ", bp1_average)
        return 1
    else:
        # print("bp1_average: ", bp1_average)
        return 0


def wbc_rule(input, index_hour) -> int:
    #if in the past hour, there are any lactate values that are over the limit

    for idx in index_hour:
        wbc_val = float(input["wbc_adjusted"][idx])
        if wbc_val > const.WBC_ADJUSTED_LIMIT:
            # print("WBC Over")
            # print("WBC value: ", wbc_val)
            return 1
    
    return 0
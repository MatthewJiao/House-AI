#main driver code

import pandas as pd
import numpy as np
import multiprocessing
import ray

import call_model
import postprocessing
import preprocessing
import rules


#preprocessing to a usable format
# df1 = preprocessing.open_test_data("test_data.csv")


def single_work():               #monitors a single patient
    count = 0
    df_raw = pd.DataFrame

    pt_identifier = []
    time = [] 
    Bp1 = [] 
    Bp2 = []
    Pulse = [] 
    Temp = []
    Rr = [] 
    O2Sat = [] 
    Age_Number = [] 
    Gender = []
    Lactate_value = [] 
    Lactate_ref_range = []  
    WBC_value = [] 
    WBC_ref_range = []
    Male = []
    Female = []
    Lactate_adjusted = []
    WBC_adjusted = []

    #what input is like
    list_of_lists = [pt_identifier, time, Bp1, Bp2, Pulse, Temp, Rr, O2Sat, Age_Number, Gender, Lactate_value, Lactate_ref_range, WBC_value, 
                    WBC_ref_range, Male, Female, Lactate_adjusted, WBC_adjusted]

    #preprocessing changes the lists a bit

    
    while count<20:        #20 for now, should be indefinite waiting time
        raw_input = input("Enter Values: ")
        count+=1
        list_of_lists = preprocessing.insert_into_arrays(raw_input, list_of_lists)
        # for s in list_of_lists:
        #     print(s)

        if count>3:      #3 for now; if greater than 3 then run through the rules and models

            #only pop for model call

            result1 = rules.master_rules(list_of_lists, count-1)
            if result1 == True:
                print("Done")
                break
            else:
                #continue with model
                model_result = call_model.call(list_of_lists, count-1)
                if model_result>0.7:
                    print("Sepsis!")
                    break
                else:
                    print("not done")
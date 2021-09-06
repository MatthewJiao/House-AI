#main driver code

import pandas as pd
import numpy as np
import multiprocessing
import ray

import call_model
import postprocessing
import preprocessing
import rules
import const

#preprocessing to a usable format
# df1 = preprocessing.open_test_data("test_data.csv")


def single_work():               #monitors a single patient
    count = 0
    df_raw = pd.DataFrame

    #for list of list implementation
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

    # #what input is like

    #preprocessing changes the lists a bit

    #for dict of list implementation (faster speed, future proof, indexing)
    main_dict = {}

    main_dict["pt_identifier"] = pt_identifier
    main_dict["time"] = time
    main_dict["bp1"] = Bp1
    main_dict["bp2"] = Bp2
    main_dict["pulse"] = Pulse
    main_dict["temp"] = Temp
    main_dict["rr"] = Rr
    main_dict["o2sat"] = O2Sat
    main_dict["age_number"] = Age_Number
    main_dict["gender"] = Gender
    main_dict["lactate_value"] = Lactate_value
    main_dict["lactate_ref_range"] = Lactate_ref_range
    main_dict["wbc_value"] = WBC_value
    main_dict["wbc_ref_range"] = WBC_ref_range
    main_dict["male"] = Male
    main_dict["female"] = Female
    main_dict["lactate_adjusted"] = Lactate_adjusted
    main_dict["wbc_adjusted"] = WBC_adjusted

    preprocessed = main_dict

    
    while count<20:        #20 for now, should be indefinite waiting time
        raw_input = input("Enter Values: ")
        count+=1
        
        #preprocessed = preprocessing.insert_into_arrays(raw_input, preprocessed)
        preprocessed = preprocessing.insert_into_dict(raw_input, preprocessed)
        for s in preprocessed:
            print(s, ": ", preprocessed[s])

        if count>const.INITIAL_WAIT:      #3 for now; if greater than 3 then run through the rules and models
            result1 = rules.master_rules(preprocessed, count-1)
            if result1 == True:
                break
            else:
                #continue with model
                model_result = call_model.call(preprocessed, count-1)
                if model_result>const.ML_THRESHOLD:
                    print("Sepsis!")
                    break
                else:
                    print("not done")
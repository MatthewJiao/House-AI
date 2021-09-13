#main driver code

import copy
import pandas as pd
import numpy as np
import multiprocessing
import ray

import call_model
import postprocessing
import preprocessing
import rules
import const

def single_work(input = None, frontend = None):               #monitors a single patient
    count = 0
    # df_raw = pd.DataFrame

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

    if frontend and input:
        fe = copy.deepcopy(main_dict)
        #print ("TYPE: ",type(input))
        # raw_input1 = "A1B2C3, 0, 100, 80, 65, 37, 20, 100, 13, Male, 3, 2-5, 5, 4-11"
        # raw_input2 = "A1B2C3, 5, 100, 80, 65, 37, 20, 100, 13, Male, 3, 2-5, 5, 4-11"
        # raw_input3 = "A1B2C3, 15, 100, 80, 65, 37, 20, 100, 13, Male, 3, 2-5, 5, 4-11"
        # raw_input4 = "A1B2C3, 25, 100, 80, 65, 37, 20, 100, 13, Male, 3, 2-5, 5, 4-11"
        try:
            input = input.split(", ")
            raw_input1 = input[0:14]
            raw_input2 = input[14:28]
            raw_input3 = input[28:42]
            raw_input4 = input[42:56]

            new_1 = ""
            new_2 = ""
            new_3 = ""
            new_4 = ""

            for x in range(14):
                new_1 = new_1+raw_input1[x] + ", "
                new_2 = new_2+raw_input2[x] + ", "
                new_3 = new_3+raw_input3[x] + ", "
                new_4 = new_4+raw_input4[x] + ", "
        except:
            return "Please Enter 4 Rows of Data"

#A1B2C3, 0, 100, 80, 65, 37, 20, 100, 13, Male, 3, 2-5, 5, 4-11, A1B2C3, 0, 100, 80, 65, 37, 20, 100, 13, Male, 3, 2-5, 5, 4-11, A1B2C3, 0, 100, 80, 65, 37, 20, 100, 13, Male, 3, 2-5, 5, 4-11, A1B2C3, 0, 100, 80, 65, 37, 20, 100, 13, Male, 3, 2-5, 5, 4-11

        fe = preprocessing.insert_into_dict(new_1, fe)
        fe = preprocessing.insert_into_dict(new_2, fe)
        fe = preprocessing.insert_into_dict(new_3, fe)
        fe = preprocessing.insert_into_dict(new_4, fe) 

        result1 = rules.master_rules(fe, 0)

        if result1==True:
            return "Sepsis!"

        else:
            return "No Sepsis Detected"


    else:
        preprocessed = copy.deepcopy(main_dict)

        
        while count<20:        #20 for now, should be indefinite waiting time
            print("\n")
            raw_input = input("Enter Values: ")        
            #preprocessed = preprocessing.insert_into_arrays(raw_input, preprocessed)
            preprocessed = preprocessing.insert_into_dict(raw_input, preprocessed)
            for s in preprocessed:
                print(s, ": ", preprocessed[s])

            if count>=const.INITIAL_WAIT-1:      #3 for now; if greater than 3 then run through the rules and models
                result1 = rules.master_rules(preprocessed, count)
                if result1 == True:
                    break
                else:
                    #continue with model
                    model_result = call_model.call(preprocessed, count)
                    if model_result>const.ML_THRESHOLD:
                        print("Sepsis!")
                        break
                    else:
                        print("not done")

            count+=1

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

    while count<20:        #20 for now, should be indefinite waiting time
        raw_input = input("Enter Values")
        count+=1
        df_raw = preprocessing.insert_into_df(raw_input, df_raw)
        if count>3:      #3 for now; if greater than 3 then run through the rules and models
            result1 = rules.master_rules(df_raw)
            if result1 == True:
                print("Done")

            else:
                #continue with model
                pass
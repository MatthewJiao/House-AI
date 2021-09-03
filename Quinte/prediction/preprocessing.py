#preprocess the data

import pandas as pd
import numpy as np

Dataframe = pd.DataFrame

def open_test_data(path: str) -> Dataframe:
    df1 = pd.read_csv(path)
    #normalize labs
    #zero the times
    return df1

def insert_into_df(raw_input, df_raw) -> Dataframe:
    raw_list = raw_input.split(" ")
    
    pass
#for inference
import pandas as pd
import numpy as np
import preprocessing
import copy

def call(new_result, curr):
    for s in new_result:
        print(s)
    new_list = copy.deepcopy(new_result)
    new_list = preprocessing.pop_lists(new_list)
    return 0.6
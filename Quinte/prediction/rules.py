import pandas as pd
import numpy as np

Dataframe = pd.DataFrame

def master_rules(df) -> bool:
    if age_rule(df) == True:
        return True
    #rule 2
    #rule 3
    return False


def age_rule(df) -> bool:
    if df["Age_Num"] <=16:
        return True

    else:
        return False

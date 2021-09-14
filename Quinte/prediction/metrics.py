#metrics to test
#have to run on the overall dataset and see if the rules/model is actually working

#run on 16 in the end, run on test first, have an option in app.py that takes in adjusted labs and male female already. 

import csv
import pandas

def run_on_dataset():
    # with open('test_metrics.csv', 'r') as file:
    #     reader = csv.reader(file)
    #     for row in reader:
    #         print(row)'
    df1 = pandas.read_csv("test_metrics.csv")
    df1 = df1.drop('Unnamed: 0', 1)

    print(df1)
    #separate at every 0 in new_date
        #going through each row and finding all the 0s
        #splitting df into that many df[0:rowNUM] df[rowNum, rowNum2]
        #list of dfs and list for rownum
    #store into dict of lists properly
    #call master_rules, changing curr each time
    #also store sepsis prediction values
    #change hour before constant 
    #compare outputs
    #create metrics
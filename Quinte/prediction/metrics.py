#metrics to test
#have to run on the overall dataset and see if the rules/model is actually working

#run on 16 in the end, run on test first, have an option in app.py that takes in adjusted labs and male female already. 

import csv
import rules
import pandas
import copy

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

def run_on_dataset():
    dict_to_send = copy.deepcopy(main_dict)
    # with open('test_metrics.csv', 'r') as file:
    #     reader = csv.reader(file)
    #     for row in reader:
    #         print(row)'
    df1 = pandas.read_csv("16.csv")
    df1 = df1.drop(columns=['Unnamed: 0', 'Most_responsible', 'pre_admit', 'post_admit', 'secondary'])

    #print(df1)
    print ("\n\n\\nn\n")
    rows = len(df1)
    i = 0
    correct_bool = False
    correct = []
    count = 0
    while i<rows:
        new_date = df1.iloc[i][3]
        if new_date == 0:
            j = i+1
            while j<rows:
                search_next_date = df1.iloc[j][3]
                if search_next_date == 0:
                    break
                j+=1
            
            df_new = df1[i:j]

            pos_or_neg = df1.iloc[0][1] #1 if pos, #0 if neg
            df_new = df_new.drop(columns=['positive_diag', 'negative_diag'])

            dict_to_send["pt_identifier"] = df_new['pt_identifier'].to_list()
            dict_to_send["time"] = df_new['new_date'].to_list()
            dict_to_send["bp1"] =  df_new['BP1'].to_list()
            dict_to_send["bp2"] =  df_new['BP2'].to_list()
            dict_to_send["pulse"] =  df_new['Pulse'].to_list()
            dict_to_send["temp"] =  df_new['Temp'].to_list()
            dict_to_send["rr"] =  df_new['RR'].to_list()
            dict_to_send["o2sat"] = df_new['O2Sat'].to_list()
            dict_to_send["age_number"] =  df_new['Age_Number'].to_list()
            dict_to_send["gender"] = []
            dict_to_send["lactate_value"] = []
            dict_to_send["lactate_ref_range"] = []
            dict_to_send["wbc_value"] = []
            dict_to_send["wbc_ref_range"] = []
            dict_to_send["male"] =  df_new['Male'].to_list()
            dict_to_send["female"] =  df_new['Female'].to_list()
            dict_to_send["lactate_adjusted"] =  df_new['Lactate_adjusted'].to_list()
            dict_to_send["wbc_adjusted"] =  df_new['WBC_adjusted'].to_list()

            #print(dict_to_send)
            num_rows = len(dict_to_send["time"])

            correct_bool = False
            
            for idx in range(num_rows):
                correct_bool = False
                result = rules.master_rules(dict_to_send, idx)
                if result == True:
                    count+=1
                if result == True and pos_or_neg == 0:
                    correct_bool = False
                    break
                elif result == True and pos_or_neg == 1:
                    correct_bool = True
                    break
                elif result == False and pos_or_neg == 0:
                    correct_bool = True
                    break
                
            if correct_bool == True:
                correct.append(1)
            else:
                correct.append(0)


            #print(df_new) #works

        i+=1

    print ("length: ", len(correct))
    num_correct = 0
    for val in correct:
        if val == 1:
            num_correct+=1
    print("num_right: ", num_correct)
    print("accuracy: ", float(num_correct/len(correct)))
    print ("positive count: ", count)
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
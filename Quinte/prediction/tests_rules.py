import pytest
import copy
import preprocessing
import rules
#pt_identifier time BP1 BP2 Pulse Temp	RR O2Sat Age_Number Gender Lactate_value Lactate_ref_range  WBC_value WBC_ref_range
# A1B2C3, 0, 100, 80, 65, 37, 20, 100, 15, Male, 3, 2-5, 5, 4-11
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

def test_age():
    age_dict = copy.deepcopy(main_dict)
    raw_input1 = "A1B2C3, 0, 100, 80, 65, 37, 20, 100, 13, Male, 3, 2-5, 5, 4-11"
    raw_input2 = "A1B2C3, 5, 100, 80, 65, 37, 20, 100, 13, Male, 3, 2-5, 5, 4-11"
    raw_input3 = "A1B2C3, 15, 100, 80, 65, 37, 20, 100, 13, Male, 3, 2-5, 5, 4-11"
    raw_input4 = "A1B2C3, 25, 100, 80, 65, 37, 20, 100, 13, Male, 3, 2-5, 5, 4-11"

    age_dict = preprocessing.insert_into_dict(raw_input1, age_dict)
    age_dict = preprocessing.insert_into_dict(raw_input2, age_dict)
    age_dict = preprocessing.insert_into_dict(raw_input3, age_dict)
    age_dict = preprocessing.insert_into_dict(raw_input4, age_dict)

    result1 = rules.age_rule(age_dict, 3)

    age_dict2 = copy.deepcopy(main_dict)
    raw_input5 = "A1B2C3, 0, 100, 80, 65, 37, 20, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input6 = "A1B2C3, 5, 100, 80, 65, 37, 20, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input7 = "A1B2C3, 15, 100, 80, 65, 37, 20, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input8 = "A1B2C3, 25, 100, 80, 65, 37, 20, 100, 19, Male, 3, 2-5, 5, 4-11"

    age_dict2 = preprocessing.insert_into_dict(raw_input5, age_dict2)
    age_dict2 = preprocessing.insert_into_dict(raw_input6, age_dict2)
    age_dict2 = preprocessing.insert_into_dict(raw_input7, age_dict2)
    age_dict2 = preprocessing.insert_into_dict(raw_input8, age_dict2)

    result2 = rules.age_rule(age_dict2, 3)

    assert result1 == True
    assert result2 == False

def test_lactate():
    lactate_dict = copy.deepcopy(main_dict)
    raw_input1 = "A1B2C3, 0, 100, 80, 65, 37, 20, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input2 = "A1B2C3, 5, 100, 80, 65, 37, 20, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input3 = "A1B2C3, 15, 100, 80, 65, 37, 20, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input4 = "A1B2C3, 25, 100, 80, 65, 37, 20, 100, 19, Male, 3, 2-5, 5, 4-11"

    lactate_dict = preprocessing.insert_into_dict(raw_input1, lactate_dict)
    lactate_dict = preprocessing.insert_into_dict(raw_input2, lactate_dict)
    lactate_dict = preprocessing.insert_into_dict(raw_input3, lactate_dict)
    lactate_dict = preprocessing.insert_into_dict(raw_input4, lactate_dict)

    result1 = rules.lactate_rule(lactate_dict, [0,1,2,3])

    lactate_dict2 = copy.deepcopy(main_dict)
    raw_input5 = "A1B2C3, 0, 100, 80, 65, 37, 20, 100, 19, Male, 7, 2-5, 5, 4-11"
    raw_input6 = "A1B2C3, 5, 100, 80, 65, 37, 20, 100, 19, Male, 7, 2-5, 5, 4-11"
    raw_input7 = "A1B2C3, 15, 100, 80, 65, 37, 20, 100, 19, Male, 7, 2-5, 5, 4-11"
    raw_input8 = "A1B2C3, 25, 100, 80, 65, 37, 20, 100, 19, Male, 7, 2-5, 5, 4-11"

    lactate_dict2 = preprocessing.insert_into_dict(raw_input5, lactate_dict2)
    lactate_dict2 = preprocessing.insert_into_dict(raw_input6, lactate_dict2)
    lactate_dict2 = preprocessing.insert_into_dict(raw_input7, lactate_dict2)
    lactate_dict2 = preprocessing.insert_into_dict(raw_input8, lactate_dict2)

    result2 = rules.lactate_rule(lactate_dict2, [0,1,2,3])

    assert result1 == 0
    assert result2 == 1

def test_rr():
    rr_dict = copy.deepcopy(main_dict)
    raw_input1 = "A1B2C3, 0, 100, 80, 65, 37, 19, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input2 = "A1B2C3, 5, 100, 80, 65, 37, 0, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input3 = "A1B2C3, 15, 100, 80, 65, 37, 0, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input4 = "A1B2C3, 25, 100, 80, 65, 37, 20, 100, 19, Male, 3, 2-5, 5, 4-11"

    rr_dict = preprocessing.insert_into_dict(raw_input1, rr_dict)
    rr_dict = preprocessing.insert_into_dict(raw_input2, rr_dict)
    rr_dict = preprocessing.insert_into_dict(raw_input3, rr_dict)
    rr_dict = preprocessing.insert_into_dict(raw_input4, rr_dict)

    result1 = rules.rr_rule(rr_dict, [0,1,2,3])

    rr_dict2 = copy.deepcopy(main_dict)
    raw_input5 = "A1B2C3, 0, 100, 80, 65, 37, 50, 100, 19, Male, 7, 2-5, 5, 4-11"
    raw_input6 = "A1B2C3, 5, 100, 80, 65, 37, 0, 100, 19, Male, 7, 2-5, 5, 4-11"
    raw_input7 = "A1B2C3, 15, 100, 80, 65, 37, 0, 100, 19, Male, 7, 2-5, 5, 4-11"
    raw_input8 = "A1B2C3, 25, 100, 80, 65, 37, 0, 100, 19, Male, 7, 2-5, 5, 4-11"

    rr_dict2 = preprocessing.insert_into_dict(raw_input5, rr_dict2)
    rr_dict2 = preprocessing.insert_into_dict(raw_input6, rr_dict2)
    rr_dict2 = preprocessing.insert_into_dict(raw_input7, rr_dict2)
    rr_dict2 = preprocessing.insert_into_dict(raw_input8, rr_dict2)

    result2 = rules.rr_rule(rr_dict2, [0,1,2,3])

    assert result1 == 0
    assert result2 == 1

def test_pulse():
    pulse_dict = copy.deepcopy(main_dict)
    raw_input1 = "A1B2C3, 0, 100, 80, 65, 37, 19, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input2 = "A1B2C3, 5, 100, 80, 65, 37, 10, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input3 = "A1B2C3, 15, 100, 80, 65, 37, 15, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input4 = "A1B2C3, 25, 100, 80, 65, 37, 16, 100, 19, Male, 3, 2-5, 5, 4-11"

    pulse_dict = preprocessing.insert_into_dict(raw_input1, pulse_dict)
    pulse_dict = preprocessing.insert_into_dict(raw_input2, pulse_dict)
    pulse_dict = preprocessing.insert_into_dict(raw_input3, pulse_dict)
    pulse_dict = preprocessing.insert_into_dict(raw_input4, pulse_dict)

    result1 = rules.pulse_rule(pulse_dict, [0,1,2,3])

    pulse_dict2 = copy.deepcopy(main_dict)
    raw_input5 = "A1B2C3, 0, 100, 80, 105, 37, 50, 100, 19, Male, 7, 2-5, 5, 4-11"
    raw_input6 = "A1B2C3, 5, 100, 80, 0, 37, 0, 100, 19, Male, 7, 2-5, 5, 4-11"
    raw_input7 = "A1B2C3, 15, 100, 80, 90, 37, 0, 100, 19, Male, 7, 2-5, 5, 4-11"
    raw_input8 = "A1B2C3, 25, 100, 80, 75, 37, 0, 100, 19, Male, 7, 2-5, 5, 4-11"

    pulse_dict2 = preprocessing.insert_into_dict(raw_input5, pulse_dict2)
    pulse_dict2 = preprocessing.insert_into_dict(raw_input6, pulse_dict2)
    pulse_dict2 = preprocessing.insert_into_dict(raw_input7, pulse_dict2)
    pulse_dict2 = preprocessing.insert_into_dict(raw_input8, pulse_dict2)

    result2 = rules.pulse_rule(pulse_dict2, [0,1,2,3])

    assert result1 == 0
    assert result2 == 1

def test_temp():
    temp_dict = copy.deepcopy(main_dict)
    raw_input1 = "A1B2C3, 0, 100, 80, 65, 37, 19, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input2 = "A1B2C3, 5, 100, 80, 65, 37, 10, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input3 = "A1B2C3, 15, 100, 80, 65, 37, 15, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input4 = "A1B2C3, 25, 100, 80, 65, 37, 16, 100, 19, Male, 3, 2-5, 5, 4-11"

    temp_dict = preprocessing.insert_into_dict(raw_input1, temp_dict)
    temp_dict = preprocessing.insert_into_dict(raw_input2, temp_dict)
    temp_dict = preprocessing.insert_into_dict(raw_input3, temp_dict)
    temp_dict = preprocessing.insert_into_dict(raw_input4, temp_dict)

    result1 = rules.temp_rule(temp_dict, [0,1,2,3])

    temp_dict2 = copy.deepcopy(main_dict)
    raw_input5 = "A1B2C3, 0, 100, 80, 105, 35, 50, 100, 19, Male, 7, 2-5, 5, 4-11"
    raw_input6 = "A1B2C3, 5, 100, 80, 0, 35, 0, 100, 19, Male, 7, 2-5, 5, 4-11"
    raw_input7 = "A1B2C3, 15, 100, 80, 90, 34, 0, 100, 19, Male, 7, 2-5, 5, 4-11"
    raw_input8 = "A1B2C3, 25, 100, 80, 75, 37, 0, 100, 19, Male, 7, 2-5, 5, 4-11"

    temp_dict2 = preprocessing.insert_into_dict(raw_input5, temp_dict2)
    temp_dict2 = preprocessing.insert_into_dict(raw_input6, temp_dict2)
    temp_dict2 = preprocessing.insert_into_dict(raw_input7, temp_dict2)
    temp_dict2 = preprocessing.insert_into_dict(raw_input8, temp_dict2)

    result2 = rules.temp_rule(temp_dict2, [0,1,2,3])

    assert result1 == 0
    assert result2 == 1

def test_bp1():
    bp_dict = copy.deepcopy(main_dict)
    raw_input1 = "A1B2C3, 0, 110, 80, 65, 37, 19, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input2 = "A1B2C3, 5, 110, 80, 65, 37, 10, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input3 = "A1B2C3, 15, 110, 80, 65, 37, 15, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input4 = "A1B2C3, 25, 0, 80, 65, 37, 16, 100, 19, Male, 3, 2-5, 5, 4-11"

    bp_dict = preprocessing.insert_into_dict(raw_input1, bp_dict)
    bp_dict = preprocessing.insert_into_dict(raw_input2, bp_dict)
    bp_dict = preprocessing.insert_into_dict(raw_input3, bp_dict)
    bp_dict = preprocessing.insert_into_dict(raw_input4, bp_dict)

    result1 = rules.bp1_rule(bp_dict, [0,1,2,3])

    bp_dict2 = copy.deepcopy(main_dict)
    raw_input5 = "A1B2C3, 0, 100, 80, 105, 35, 50, 100, 19, Male, 7, 2-5, 5, 4-11"
    raw_input6 = "A1B2C3, 5, 0, 80, 0, 35, 0, 100, 19, Male, 7, 2-5, 5, 4-11"
    raw_input7 = "A1B2C3, 15, 0, 80, 90, 34, 0, 100, 19, Male, 7, 2-5, 5, 4-11"
    raw_input8 = "A1B2C3, 25, 0, 80, 75, 37, 0, 100, 19, Male, 7, 2-5, 5, 4-11"

    bp_dict2 = preprocessing.insert_into_dict(raw_input5, bp_dict2)
    bp_dict2 = preprocessing.insert_into_dict(raw_input6, bp_dict2)
    bp_dict2 = preprocessing.insert_into_dict(raw_input7, bp_dict2)
    bp_dict2 = preprocessing.insert_into_dict(raw_input8, bp_dict2)

    result2 = rules.bp1_rule(bp_dict2, [0,1,2,3])

    assert result1 == 0
    assert result2 == 1

def test_wbc():
    wbc_dict = copy.deepcopy(main_dict)
    raw_input1 = "A1B2C3, 0, 100, 80, 65, 37, 20, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input2 = "A1B2C3, 5, 100, 80, 65, 37, 20, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input3 = "A1B2C3, 15, 100, 80, 65, 37, 20, 100, 19, Male, 3, 2-5, 5, 4-11"
    raw_input4 = "A1B2C3, 25, 100, 80, 65, 37, 20, 100, 19, Male, 3, 2-5, 5, 4-11"

    wbc_dict = preprocessing.insert_into_dict(raw_input1, wbc_dict)
    wbc_dict = preprocessing.insert_into_dict(raw_input2, wbc_dict)
    wbc_dict = preprocessing.insert_into_dict(raw_input3, wbc_dict)
    wbc_dict = preprocessing.insert_into_dict(raw_input4, wbc_dict)

    result1 = rules.wbc_rule(wbc_dict, [0,1,2,3])

    wbc_dict2 = copy.deepcopy(main_dict)
    raw_input5 = "A1B2C3, 0, 100, 80, 65, 37, 20, 100, 19, Male, 7, 2-5, 12, 4-11"
    raw_input6 = "A1B2C3, 5, 100, 80, 65, 37, 20, 100, 19, Male, 7, 2-5, 0, 4-11"
    raw_input7 = "A1B2C3, 15, 100, 80, 65, 37, 20, 100, 19, Male, 7, 2-5, 0, 4-11"
    raw_input8 = "A1B2C3, 25, 100, 80, 65, 37, 20, 100, 19, Male, 7, 2-5, 0, 4-11"

    wbc_dict2 = preprocessing.insert_into_dict(raw_input5, wbc_dict2)
    wbc_dict2 = preprocessing.insert_into_dict(raw_input6, wbc_dict2)
    wbc_dict2 = preprocessing.insert_into_dict(raw_input7, wbc_dict2)
    wbc_dict2 = preprocessing.insert_into_dict(raw_input8, wbc_dict2)

    result2 = rules.wbc_rule(wbc_dict2, [0,1,2,3])

    assert result1 == 0
    assert result2 == 1
# this program's purpose is to read through the initial dataset accident_data.csv, check each row
# and remove the datapoints that correspond to the "Slight" category of accidents, while also not
# containing missing values for "1st road class" and or "2nd road class". Along with that, the 
# print statements represent the number of total values that are present, the number of datapoints 
# that have missing values for the 1st or 2nd road class, and the final % of class shares that are 
# present in the final dataset. This is where and how we quantified the class imbalance. 

import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily
import time

count = 0
count_class = 0
count_class_slight = 0
count_class_serious = 0
count_class_fatal = 0
count_slight = 0
count_serious = 0
count_fatal = 0

with open('accident_data.csv', 'r', newline = '') as inp, open('fixed_data.csv', 'w', newline = '') as out, open('fixed_data.csv', 'r', newline = '') as final:
    reader = csv.reader(inp)
    reader = csv.reader(final)
    writer = csv.writer(out)

    for row in csv.reader(inp):
        if count == 0: 
            writer.writerow(row)
            count += 1
            continue
            
        # 1, 3, 5 [1st road class, 2nd road class, accident severity]
        if row[1] == '' or row[3] == '' or row[1] == 'Unclassified' or row[3] == 'Unclassified':
            count_class += 1
            if row[5] == 'Slight': 
                count_class_slight += 1
            elif row[5] == 'Serious': 
                count_class_serious += 1
            elif row[5] == 'Fatal': 
                count_class_fatal += 1

        elif row[0] != '' and row[0] != 'Unclassified' and row[1] != '' and row[1] != 'Unclassified':
            if row[5] != 'Fatal' and row[5] != 'Serious':
                writer.writerow(row)
        if row[5] == 'Fatal' or row[5] == 'Serious':
            writer.writerow(row)

        if row[5] == 'Slight': 
            count_slight += 1
        elif row[5] == 'Serious': 
            count_serious += 1
        elif row[5] == 'Fatal': 
            count_fatal += 1

    count_slight2 = 0
    count_serious2 = 0
    count_fatal2 = 0
    for row in csv.reader(inp):
        if row[27] == 'Slight': 
            count_slight2 += 1
        elif row[27] == 'Serious': 
            count_serious2 += 1
        elif row[27] == 'Fatal': 
            count_fatal2 += 1
    
    total = count_slight2 + count_serious2 + count_fatal2


print("# cells with missing vals: ", count_class)
print("# slight with missing vals: ", count_class_slight, " out of: ", count_slight, ", % = ", count_class_slight*100/count_slight)
print("# serious with missing vals: ", count_class_serious, " out of: ", count_serious, ", % = ", count_class_serious*100/count_serious)
print("# fatal with missing vals: ", count_class_fatal, " out of: ", count_fatal, ", % = ", count_class_fatal*100/count_fatal)

print("Slight count in new dataset: ", count_slight2, ", % = ", count_slight2*100/total)
print("Serious count in new dataset: ", count_serious2, ", % = ", count_serious2*100/total)
print("Fatal count in new dataset: ", count_fatal2, ", % = ", count_fatal2*100/total)


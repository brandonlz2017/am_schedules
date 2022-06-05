"""
Created on Sun Jun  5 12:02:15 2022

@author: Brandon Zeman
"""

# This function calculates the continuously compounded discount factor when 
# given an array of monthly dates

import math

dates_working = ['2020-09-01', '2020-10-01', '2020-11-01']
temp_discounts = [0.99, 0.98, 0.97, 0.96]

def ccdf_calc(month_list, discount_rate):
    string_text_dt = 'date = '
    string_text_disc_factor = 'discount factor = '
    
    date_list = []
    factor_list = []
    for i in range(len(dates_working)):
        output_date = string_text_dt+dates_working[i]
        #print(output_date)
        discount_factor = math.e**-abs(discount_rate*(i+1))
        output_factor = string_text_disc_factor+str(discount_factor)
        #print(output_factor)
        date_list.append(output_date)
        factor_list.append(output_factor)
        
    return set(zip(date_list, factor_list))
        
ccdf_calc(dates_working, 0.02)    
    

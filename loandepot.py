"""
Created on Sun Jun  5 12:02:15 2022

@author: Brandon Zeman
"""

# This function calculates the continuously compounded discount factor when 
# given an array of monthly dates

import pandas as pd
import numpy_financial as npf
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




# if loan has an interest only term, set io_term equal to term.
# if loan is fixed, set io_term to 0
    
def amortizer_calc(rate, term, orig_bal, io_term, balloon_term):
    balance_list = []
    #new_bal = []
    rate = rate/1200
    term = term*12
    io_term = io_term*12
    balloon_term = balloon_term*12
    fixed_periods = term-io_term
    periods_list = []
    pmt_list = []
    int_list = []
    prin_list = []
    io_pmt_list = []
    io_total_pmt = []
    io_balance = []
    balloon_prin = []
    balloon_bal = []
    balloon_total_pay = []
    fixed_periods_int_list = []
    fixed_periods_prin_list = []
    #total_pmt = round(npf.pmt(rate, term, orig_bal)*-1, 2)
    #int_pmt = round(npf.ipmt(rate, term, orig_bal, orig_bal)*-1, 2)
    #prin_pmt = round(npf.ppmt(rate, 1, term, orig_bal)*-1, 2)
    #print(total_pmt, prin_pmt, int_pmt)
    
    for i in range(term):
        period = i+1
        total_pmt = round(npf.pmt(rate, term, orig_bal)*-1, 2)
        int_pmt = round(npf.ipmt(rate, period, term, orig_bal)*-1, 2)
        prin_pmt = round(npf.ppmt(rate, period, term, orig_bal)*-1, 2)
        
        if period <= io_term:
            #print(period)
            io_pmt = round(npf.ipmt(rate, 1, term, orig_bal)*-1, 2)
            io_pmt_list.append(io_pmt)
            io_balance.append(orig_bal)
            
            
        if period == 1:
            current_bal = round(orig_bal-prin_pmt, 2)
        else:
            current_bal = round(balance_list[-1]-prin_pmt, 2)
            if current_bal < 0:
                current_bal = 0
        
        if period < balloon_term:
            balloon_pay = prin_pmt
        elif period == balloon_term:
            balloon_pay = balance_list[-1]
        else:
            balloon_pay = 0
        balloon_prin.append(balloon_pay)
        
        pmt_list.append(total_pmt)
        int_list.append(int_pmt)
        prin_list.append(prin_pmt)
        periods_list.append(period)
        balance_list.append(current_bal)
        
    for i in range(fixed_periods):
        period = i+1
        total_pmt = round(npf.pmt(rate, fixed_periods, orig_bal)*-1, 2)
        int_pmt = round(npf.ipmt(rate, period, fixed_periods, orig_bal)*-1, 2)
        prin_pmt = round(npf.ppmt(rate, period, fixed_periods, orig_bal)*-1, 2)
        current_bal = round(io_balance[-1]-prin_pmt, 2)
        if current_bal < 0.02:
            current_bal = 0
        
        fixed_periods_int_list.append(int_pmt)
        fixed_periods_prin_list.append(prin_pmt)
        io_total_pmt.append(total_pmt)
        io_balance.append(current_bal)
    #print(total_pmt)    
    io_int_list = io_pmt_list+fixed_periods_int_list    
    io_prin_list = [0]*io_term+fixed_periods_prin_list
    io_total = io_pmt_list+io_total_pmt

    #balloon_prin_pay = prin_list[:balloon_term]
    balloon_ending_periods = [0]*(term-balloon_term) 
    balloon_int = int_list[:balloon_term]+balloon_ending_periods
    #balloon_ending_periods = [0]*(term-balloon_term) 
    for i in range(balloon_term):
        period = i+1
        if period < balloon_term:
            total_pmt = pmt_list[i]
            current_bal = balance_list[i]
        else:
            total_pmt = balloon_prin[i]+balloon_int[i]
            #print(balance_list[i-1])
            current_bal = round(balance_list[i-1]-prin_pmt, 2)-balloon_prin[i]
            if current_bal < 0:
                current_bal = 0
        balloon_total_pay.append(total_pmt)
        balloon_bal.append(current_bal)
    balloon_total_pay = balloon_total_pay+balloon_ending_periods
    balloon_bal = balloon_bal+balloon_ending_periods
    #balloon_int = int_list[:balloon_term]+balloon_ending_periods
    #print(balloon_prin)
    
    print(balloon_bal)
    #print(balloon_total_pay)
    df = pd.DataFrame([periods_list, pmt_list, prin_list, int_list, balance_list, io_total, io_int_list, io_prin_list, io_balance, balloon_total_pay, balloon_int, balloon_prin, balloon_bal]).T
    df.columns = ['Month','Total Payment (Fixed)', 'Principal', 'Interest', 'Current Balance','IO Total Payment', 'IO Interest', 'IO Principal', 'IO Current Balance', 'Balloon Total Payment', 'Balloon Interest', 'Balloon Principal', 'Balloon Balance']
    #print(df[['Month', 'IO Total Payment', 'IO Interest', 'IO Principal']])
    
    df.to_excel('am_sched.xlsx')
    
    #print(balance_list)
    #print(len(io_pmt_list))
        
    #print(int_list)
    
amortizer_calc(3, 30, 200000, 10, 10)














        
ccdf_calc(dates_working, 0.02)    
    



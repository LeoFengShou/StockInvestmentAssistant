'''
Author:     Shoujun Feng
            1T9 Engsci, UofT

Purpose:    To calculate the amplitude of the sotck price drop which is large
            enough to serve as an implication for a buy action.

Algorithm:  Calculate the standard deviation of a list of stocks.
            Amplitude/reference_Amplitude = stddiv/reference_stddiv
            Use stock ESV as a reference. From my analysis, when ESV drops more
            than 30% in a certain period, it is an implication for a buy action.
            Therefore, the reference_Amplitude is 30 and reference_stddiv is the
            stddiv of ESV based on ESV's history.
'''

import glob
import numpy as np

list_of_stock_filenames = glob.glob('*.csv')
dic_of_stddiv = {}
dic_of_amplitude = {}
stock_history_price_in_list = []
for stock_filename in list_of_stock_filenames:
    stock_history_in_table = open(stock_filename,"r").read().split("\n")
    stock_history_price_in_list = []
    for i in range(1,len(stock_history_in_table),1):
        stock_history_in_table[i] = stock_history_in_table[i].split(",")
        try:
            stock_history_price_in_list.append(float(stock_history_in_table[i][6]))
        except:
            continue
    stddiv = np.std(stock_history_price_in_list)
    stock_name = stock_filename[:stock_filename.find(".csv")]
    dic_of_stddiv[stock_name] = stddiv
fo = open("Drop_To_Buy_Amplitude_For_All.txt","w+")
for stock in dic_of_stddiv.keys():
    amplitude = dic_of_stddiv[stock]/dic_of_stddiv['ESV']*30
    fo.write(stock+"-"+str(amplitude)+"\n")
fo.close()

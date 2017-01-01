'''
Author:     Shoujun Feng
            1T9 Engsci, UofT
Purpose:    To find the stock that has dropped sharply in the past 10 days.
Parameter:  stock_symbol, the certain number of days ago.
Process:    compare today's price with the prices in the past 10 days, if the
            price drop is more than 10%, record it.
'''
import single_stock_recent_change_check as sc
import time
import os

def short_term_drop_picker(filename_list_file_path):
    '''
    create the date in the filename for output
    '''
    all_symbols = open(filename_list_file_path,"r").read().split("\n")
    current_day = int(time.strftime("%d"))
    if current_day < 10:
        current_day = "0" + str(current_day)
    current_day = str(current_day)
    current_month = int(time.strftime("%m"))
    if current_month < 10:
        current_month = "0" + str(current_month)
    current_month = str(current_month)
    current_year = int(time.strftime("%Y"))
    '''create the store path'''
    saving_folder_date = str(current_year) + current_month + current_day
    os.chdir("..")
    os.chdir("..")
    os.chdir("ShortTermDailyResult/")
    if not os.path.exists(saving_folder_date):
        os.makedirs(saving_folder_date)
    os.chdir(saving_folder_date)
    res = open("stocks_drop_sharply_recently"+saving_folder_date+".txt","w+")
    invalid = open("unable_to_check.txt","w+")
    for stock in all_symbols:
        print stock
        for i in range(1,11,1):
            recent_change = sc.check_increase_or_decrease_recent_days(stock,i)
            if recent_change != None and recent_change < -10:
                res.write(stock+"\n")
                print stock,recent_change
                break
            if recent_change == None:
                invalid.write(stock+"\n")
                break
    invalid.close()
    res.close()

if __name__ == '__main__':
    short_term_drop_picker("allSymbol.txt")

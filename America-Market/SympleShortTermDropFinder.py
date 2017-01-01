'''
Author:     Shoujun Feng
            1T9 Engsci, UofT
Purpose:    Find potential stocks which drops continuously recently, which may be
            stocks worth to buy.
Algorithm:  Calls single_stock_recent_change_check repeatedly to check whether a
            a stock drops continuouely for more than 4 days before today.
Output:     A list of stock symbols stored in the designated folder in the name
            of today's date.
'''
import single_stock_recent_change_check as sc
import time
import os

def continuous_drop_picker(filename_list_file_path):
    all_symbols = open(filename_list_file_path,"r").read().split("\n")
    # obtain the current date to form the name of the output
    current_day = int(time.strftime("%d"))
    if current_day < 10:
        current_day = "0" + str(current_day)
    current_day = str(current_day)
    current_month = int(time.strftime("%m"))
    if current_month < 10:
        current_month = "0" + str(current_month)
    current_month = str(current_month)
    current_year = int(time.strftime("%Y"))
    saving_folder_date = str(current_year) + current_month + current_day
    # designate folder path here
    os.chdir("..")
    os.chdir("..")
    os.chdir("ShortTermDailyResult/")
    if not os.path.exists(saving_folder_date):
        os.makedirs(saving_folder_date)
    os.chdir(saving_folder_date)
    
    res = open("stocks_drop_continuously_recently"+saving_folder_date+".txt","w+")
    invalid = open("unable_to_check.txt","w+")
    continuous_down = True
    count = 0
    for stock in all_symbols:
        if stock != "":
            stock = stock.split(":")[0]
            print stock
            front = -1
            end = -1
            for i in range(1,6,1):
                if front == -1 and end == -1:
                    front,front_day = sc.get_back_price(stock,i)
                    end, end_day = front,front_day
                else:
                    front,front_day = sc.get_back_price(stock,i)
                if front != None and front > end :
                    count += 1
                if front != None and front < end:
                    break
                end, end_day = front,front_day
            if count >= 4:
                res.write(stock+"\n")
                print(stock+"\n")
                count = 0

    invalid.close()
    res.close()

if __name__ == '__main__':
    continuous_drop_picker("allSymbol.txt")

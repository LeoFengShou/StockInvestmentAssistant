'''
Author:     Shoujun Leo Feng
            1T9 Engsci, UofT
Purpose:    To find the stock that has dropped sharply in the past 10 days.
Parameter:  stock_symbol, the certain number of days ago.
Process:    compare today's price with the prices in the past 10 days, if the
            price drop is more than 10%, record it.
'''
import grabHistoryPrice as ghp
import os
import time

def short_term_drop_picker(filename_list_file_path):
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
    saving_folder_date = str(current_year) + current_month + current_day
    os.chdir("..")
    os.chdir("..")
    os.chdir("ShortTermDailyResult/")
    if not os.path.exists(saving_folder_date):
        os.makedirs(saving_folder_date)
    os.chdir(saving_folder_date)
    res = open("stocks_drop_sharply_recently_improved"+saving_folder_date+".txt","w+")
    invalid = open("unable_to_check.txt","w+")
    for stock in all_symbols:
        if stock != "":
            print stock
            stock = stock.split(":")[0]
            ghp.grabHistoryPriceForOneStock(stock)
            price_history = open(stock + '.csv',"r").read().split("\n")
            sharp_down = False
            for i in range(1,20,1):
                if (float(price_history[i].split(",")[1]) -
                    float(price_history[0].split(",")[1]))/
                    float(price_history[i].split(",")[1]) > 0.1 :
                    sharp_down = True
                    break
            if sharp_down:
                res.write(stock+"\n")
            os.remove(stock+".csv")
    invalid.close()
    res.close()

if __name__ == '__main__':
    short_term_drop_picker("allSymbol.txt")

'''
Author:     Shoujun Leo Feng
            1T9 Engsci, UofT
purpose:    To check the stock price at a certain number of days ago
            For example, check the price of 600510 3 days ago
'''

import urllib2
import time

MONTH_SHORT = ["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTH_DAYS_LEAP = ["",31,29,31,30,31,30,31,31,30,31,30,31]
MONTH_DAYS_REG = ["",31,28,31,30,31,30,31,31,30,31,30,31]
WEEKDAYS = {"Mon":1,"Tue":2,"Wed":3,"Thu":4,"Fri":5,"Sat":5,"Sun":5}

def get_back_price(symbol = None, back_days = 0):
    if symbol == None:
        symbol = input("Enter the symbol of the stock you want to check:")
    if back_days == 0:
        back_days = input("Enter how many days backwards you want to check(<30):")
    if back_days >= 30:
        back_days = input("Enter how many days backwards you want to check(<30):")
    search_date = data_calculator(back_days)
    html = urllib2.urlopen(
    "http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/" +
    symbol + '.phtml').read()
    start_position = html.find(search_date)
    count = 0
    if start_position == -1:
        while start_position == -1:
            back_days += 1
            search_date = data_calculator(back_days)
            start_position = html.find(search_date)
            count += 1
            if count >= 5:
                break
    if start_position == -1:
        return None,None
    print search_date
    for i in range(3):
        start_position = html.find("<td><div align=\"center\">",start_position
                                    + len("<td><div align=\"center\">"))
    start_position = start_position + len("<td><div align=\"center\">")
    end_position = html.find("</div>",start_position)
    back_day_price = float(html[start_position:end_position])
    return back_day_price, search_date


def data_calculator(back_days):
    '''return the day when the function should search for the history price'''
    # dd/mm/yyyy format
    current_day = int(time.strftime("%d"))
    current_month = int(time.strftime("%m"))
    current_year = int(time.strftime("%Y"))
    current_weekday = time.strftime("%a")
    if back_days >= WEEKDAYS[current_weekday]:
        if back_days > 5:
            back_days += 2*(int(back_days/5))
        else:
            back_days += 2
    if back_days >= current_day:
        search_month = current_month - 1
        search_year = current_year
        if search_month <= 0:
            search_year = current_year - 1
            search_month = 12
        if search_year % 4 == 0:
            search_day = MONTH_DAYS_LEAP[search_month] - (back_days - current_day)
        else:
            search_day = MONTH_DAYS_REG[search_month] - (back_days - current_day)
    else:
        search_day = current_day - back_days
        search_month = current_month
        search_year = current_year
    if search_day < 10:
        search_day = "0"+str(search_day)
    else:
        search_day = str(search_day)
    if search_month < 10:
        search_month = "0"+str(search_month)
    else:
        search_month = str(search_month)
    return str(search_year) + "-" + search_month + "-" + search_day

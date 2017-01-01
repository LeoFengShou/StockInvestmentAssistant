'''
Author:     Shoujun Feng
            1T9 Engsci, UofT
Purpose:    To check the stock price at a certain number of days ago
            For example, check the price of ESV 3 days ago
Parameter:  stock_symbol, the certain number of days ago.
Process:    Get the back day in a certain format in accordance with the web
            source used.
            Search the date obtained in the html file from the web source.
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
    html = urllib2.urlopen("https://ca.finance.yahoo.com/q/hp?s=" + symbol).read()
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
        print "bad"
        return None,None
    print search_date       # this is to show the program running process
    for i in range(3):
        start_position = html.find("<td class=\"yfnc_tabledata1\" align=\"right\">",
        start_position + len("<td class=\"yfnc_tabledata1\" align=\"right\">"))
    start_position = start_position + len("<td class=\"yfnc_tabledata1\" align=\"right\">")
    end_position = html.find("</td>",start_position)
    back_day_price = float(html[start_position:end_position])
    return back_day_price,search_date


def data_calculator(back_days):
    '''return the day when the function should search for the history price
       in the format of Month day, year'''
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
    return MONTH_SHORT[search_month]+" "+str(search_day)+", " + str(search_year)

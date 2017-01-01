'''
Author:     Shoujun Leo Feng
            1T9 Engsci, UofT
Purpose:    grab the historical price of a stock and output as a csv file
'''
import csv
import urllib2, os
from bs4 import BeautifulSoup

def grabHistoryPriceForOneStock(symbol = None):
    if symbol == None:
        print "please enter a symbol"
    html = urllib2.urlopen("http://www.aigaogao.com/tools/history.html?s=" +
                            symbol).read()
    records = []
    soup = BeautifulSoup(html)
    table2 = soup.find_all('table')[1]
    for tr in table2.find_all('tr')[2:]:
        tds = tr.find_all('td')
        #import pdb; pdb.set_trace()
        #url = tds[8].a.get('href')
        records.append([elem.text.encode('utf-8') for elem in tds])
    with open(symbol + 'raw.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(records)
    process(symbol)

def process(symbol):
    raw_data = open(symbol + 'raw.csv', "r").read().split('\n')
    output = open(symbol + '.csv', 'w+')
    for i in range(len(raw_data)):
        #if i == 200:
        #    import pdb; pdb.set_trace()
        entrys = raw_data[i].split(",")
        if len(entrys) == 17:
            output.write(entrys[0]+","+entrys[4]+"\n")
    output.close()
    os.remove(symbol + 'raw.csv')
if __name__ == '__main__':
    grabHistoryPriceForOneStock("002004")

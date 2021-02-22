import time
import datetime
from bs4 import BeautifulSoup
import requests
import lxml
import logging
import pandas as pd
    
def Filter_Transaction(transactions):
    Transaction_List = []
    for transaction in transactions:
        Hash = transaction.find('a')
        Time_BTC_USD = transaction.find_all('span')
        skip_text = ['Hash', 'Time', 'Amount (BTC)', 'Amount (USD)']
        trans = []
        trans.append(Hash.text)
        for element in Time_BTC_USD:
            if (element.text not in skip_text):
                trans.append(element.text)
        trans[3] = trans[3].replace('$', '').replace(',', '')
        trans[3] = float(trans[3])
        Transaction_List.append(trans)
    df_transactions = pd.DataFrame(Transaction_List, columns=['Hash', 'Time', 'BTC', 'USD'])
    #print(df_transactions)
    Highest_transaction = df_transactions.sort_values(by = ['USD'], ascending=False).head(1)
    print(Highest_transaction)


def GetData():
    source = requests.get('https://www.blockchain.com/btc/unconfirmed-transactions').text
    soup = BeautifulSoup(source, 'lxml')
    transactions = soup.find_all('div', class_='hXyplo')
    Filter_Transaction(transactions)


while True:
    GetData()
    time.sleep(60)

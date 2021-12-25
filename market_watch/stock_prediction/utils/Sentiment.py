import nltk
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from yahoofinance import *
#from googlesearch import search

class Sentiment:
    def __init__(self,ticker,num):
        self.ticker=ticker
        self.num=num

    def fv_sentiment(self):
        finviz_url = 'https://finviz.com/quote.ashx?t=' 
        news_tables = {}
        url = finviz_url + self.ticker        #extracting finviz news for given company
        vader = SentimentIntensityAnalyzer()   

        req = Request(url=url, headers={'user-agent': 'my-app'})  #making request using URL
        response = urlopen(req)

        html = BeautifulSoup(response, features='html.parser')    #to extract data from html format
        news_table = html.find(id='news-table')
        news_tables[self.ticker] = news_table

        parsed_data = []

        for ticker, news_table in news_tables.items():          #loading date time and headlines 
            for ind,row in enumerate(news_table.findAll('tr')):
                if self.num>0:
                    title = row.a.text           #extracting healine
                    date_data = row.td.text.split(' ')       #extracting date_time

                    if len(date_data) == 1:
                        time = date_data[0]     #extracting time
                    else:
                        date = date_data[0]     
                        time = date_data[1]
                    
                    s=vader.polarity_scores(title)      #predicting polarity scores
                    compound = s['compound']            #finding compound of the headline
                    if compound >= 0:            
                        sentiment = 1                     #predicting sentiment of the headline
                    else:
                        sentiment = 0

                    parsed_data.append([ticker, date, time, title, compound, sentiment])

                (self.num)=(self.num)-1;

        df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title', 'compound' , 'sentiment'])      #preparing dataframe of final output with sentiments and compounds
        df['date'] = pd.to_datetime(df.date).dt.date
        df['date'] = df['date'].astype(str)+' '+df['time'].astype(str)
        df=df.drop(labels= ['ticker','time'] , axis=1)
        headlines_sentiment = df.to_dict('records')
        return headlines_sentiment

    '''def name_convert(self):
        searchval = 'yahoo finance '+self
        link = []
        #limits to the first link
        for url in search(searchval, tld='es', lang='es', stop=1):
            link.append(url)
        
        link = str(link[0])
        link=link.split("/")
        if link[-1]=='':
            ticker=link[-2]
        else:
            x=link[-1].split('=')
            ticker=x[-1]
        
        return(ticker)

        company_name=input("Enter a company name: ")
        ticker=name_convert(company_name)
        print(ticker)'''
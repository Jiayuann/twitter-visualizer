from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import csv
import pandas as pd
from pandas import Series,DataFrame
import regex as re
import datetime

def get_sentiemnt(name_of_file):
    data_file = pd.read_csv(name_of_file)
    # Read first column of the dataframe and convert it to a list of string.
    sentences = data_file['Text'].tolist()
    # Create a list to store sentiment analysis result.
    sentiment_result = []
    # Sentiment Intensity Analyzer from 'nltk'.
    sid = SentimentIntensityAnalyzer()
    for sentence in sentences:
        # Sentence is the raw text from tweets.
        # A filter, remove all non-ASCII charaters.
        sentence = re.sub(r'[^\x00-\x7f]',r'', sentence) 
        # Get sentiment
        ss = sid.polarity_scores(sentence) 
        # ss is a dict type like {'neg':0.5,...}
        sentiment_result.append(ss)
    # print(sentiment_result)
    data_file['sentiment'] = Series(sentiment_result)
    # list = data_file['sentiment'].tolist()
    data_file.to_csv(name_of_file)



# A function to get data string.
def get_date_string(start,end):
    list = []
    for n in range( ( end - start ).days):
        list.append( start + datetime.timedelta( n ) )
    l_date = []
    for d in list:
        l_date.append(d.strftime('%Y-%m-%d'))
    return l_date

# Get list of a string of date time with format "yyyy-mm-dd".
list_date = get_date_string(datetime.date( year = 2017, month = 3, day = 1 ),
                         datetime.date( year = 2017, month = 3, day = 9 ))
# Create a list of states.
list_of_state = ['ALABAMA','ALASKA','ARIZONA','ARKANSAS','CALIFORNIA','COLORADO','CONNECTICUT',
                'DELAWARE','FLORIDA','GEORGIA','HAWAII','IDAHO','ILLINOIS','INDIANA','IOWA','KANSAS',
                'KENTUCKY','LOUISIANA','MAINE','MARYLAND','MASSACHUSETTS','MICHIGAN','MINNESOTA',
                'MISSISSIPPI','MISSOURI','MONTANA','NEBRASKA','NEVADA','NEW%20HAMPSHIRE','NEW%20JERSEY',
                'NEW%20MEXICO','NEW%20YORK','NORTH%20CAROLINA','NORTH%20DAKOTA','OHIO','OKLAHOMA','OREGON',
                'PENNSYLVANIA','RHODE%20ISLAND','SOUTH%20CAROLINA','SOUTH%20DAKOTA','TENNESSEE','TEXAS','UTAH',
                'VERMONT','VIRGINIA','WASHINGTON','WEST%20VIRGINIA','WISCONSIN','WYOMING']
'''
pass..........
'''
for state in list_of_state:
    print state
    for i in range(0,len(list_date) - 1,1):
        print 'Getting Sentiment'
        file_name = "/Users/tianchao/Desktop/python_crawler/data/" + state + list_date[i] + ".csv"
        get_sentiemnt(file_name)
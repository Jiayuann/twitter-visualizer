import os,json,numpy,pandas,codecs,jieba,csv
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import datetime

os.chdir('/Users/jiayuan/Documents/data/project_263/tweets_bystate/csv_bystate/')
contents = []

states = ['HAWAII','ALASKA','FLORIDA','SOUTH%20CAROLINA','GEORGIA','ALABAMA','NORTH%20CAROLINA',
        'TENNESSEE','RHODE%20ISLAND','CONNECTICUT','MASSACHUSETTS','MAINE','NEW%20HAMPSHIRE',
        'VERMONT','NEW%20YORK','NEW%20JERSEY','PENNSYLVANIA','DELAWARE','MARYLAND','WEST%20VIRGINIA',
        'KENTUCKY','OHIO','MICHIGAN','WYOMING','MONTANA','IDAHO','WASHINGTON',"WASHINGTON%2CD.C.",
        'TEXAS','CALIFORNIA','ARIZONA','NEVADA','UTAH','COLORADO','NEW%20MEXICO','OREGON',
        'NORTH%20DAKOTA','SOUTH%20CAROLINA','NEBRASKA','IOWA','MISSISSIPPI','INDIANA',
        'ILLINOIS','MINNESOTA','WISCONSIN','MISSOURI','ARKANSAS','OKLAHOMA','KANSAS','LOUISIANA','VIRGINIA',]


def get_date_string(start,end):
    date_list = []
    l_date = []
    for n in range( ( end - start ).days):
        date_list.append( start + datetime.timedelta( n ) )
    for d in date_list:
        l_date.append(d.strftime('%Y-%m-%d'))
    return l_date
dates = get_date_string(datetime.date( year = 2017, month = 3, day = 4 ),
                         datetime.date( year = 2017, month = 3, day = 8 ))

for state in states:
    content = [state]
    for date in dates:
        file = state + str(date) +'.csv'
        if '\0' not in open(file).read():
            csv_file = codecs.open(file,'r')
            csv_data = csv.DictReader(csv_file)
            for row in csv_data:
                for cont in jieba.cut(row['Text']):
                    content.append(cont)
    contents.append(content)  

for index, segment in enumerate(contents):
    words_df = pandas.DataFrame({'segment':segment})
    stopwords = pandas.read_csv("/Users/jiayuan/Documents/data/project_263/script/stopwords.txt",
                                index_col=False,
                                quoting=3,
                                sep="\t",
                                names=['stopword'],
                                encoding="utf8")
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
    words_stat = words_df.groupby(by = ['segment'])['segment'].agg({'count':numpy.size})
    words_stat = words_stat.reset_index().sort(columns ='count',ascending = False)
    print(words_stat.head(30))

    #words_stat = words_stat.drop(words_stat.index[[i for i in range (30)]])
    #print(words_stat.head(30))
    #matplotlib inline
    wordcloud = WordCloud(font_path = None,background_color = 'white')   
    wordcloud = wordcloud.fit_words(words_stat.head(1000).itertuples(index = False))
    plt.figure(figsize=(5,2)) 

    plt.imshow(wordcloud,interpolation='nearest', aspect='auto')
    plt.savefig("figure2_"+str(index)+".png")
    #plt.show()
    plt.close()
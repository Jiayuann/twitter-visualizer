import os,json,numpy,pandas,codecs,jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud

print(os.getcwd())
tweets_file = codecs.open('/Users/jiayuan/Documents/data/project_263/tweets_data/tweets_adv1.json','r').read()
segment = []
for i in json.loads(tweets_file):
    for seg in jieba.cut(i['text']):
        segment.append(seg)

words_df = pandas.DataFrame({'segment':segment})
stopwords = pandas.read_csv("/Users/jiayuan/Documents/data/project_263/word_cloud_Valentines_Day/stopwords.txt",
                            index_col=False,
                            quoting=3,
                            sep="\t",
                            names=['stopword'],
                            encoding="utf8")
words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
words_stat = words_df.groupby(by = ['segment'])['segment'].agg({'count':numpy.size})
words_stat = words_stat.reset_index().sort(columns ='count',ascending = False)
print(words_stat.head(30))


# words_stat = words_stat.drop(words_stat.index[[i for i in range (30)]])
# print(words_stat.head(30))
#matplotlib inline
wordcloud = WordCloud(font_path = None,background_color = 'white')
wordcloud = wordcloud.fit_words(words_stat.head(1000).itertuples(index = False))
plt.figure(figsize=(5,2)) 
plt.imshow(wordcloud,interpolation='nearest', aspect='auto')
plt.savefig("/Users/jiayuan/Documents/data/project_263/tweets_data/figure_1.png")
plt.show() 
plt.close()
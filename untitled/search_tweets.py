import json,sys,os,tweepy,dataset,oauth2
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from tweepy.streaming import StreamListener 
from tweepy import OAuthHandler, Stream



API_KEY = 'f5hlSu4oAGqU7fYyxhSQMjxCI'
API_SECRET = 'nUl1BD0ZzX1svURMFhTAENUPCdm7C4G01dbg5MuKTHKFOGJvNL'
TOKEN_KEY = '796415807966179328-WPWG4OSYo59dhH3z3XXHaA0iqunFXNK'
TOKEN_SECRET = 'e2lTeksloFiY6Y7TYFGioObf8zbsfv7ksvdY1Q1AgLmlG'

# Simple Data pull from REST API. To establish a connection to OAuth. Create connections via oauth2.Token.
# To provide consumer with the keys so it can properly identify via API
# Search for all related tweets with keyword california and save it to scraping_tweets1.txt
def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
	consumer = oauth2.Consumer(key=API_KEY, secret=API_SECRET)
	token = oauth2.Token(key=key, secret=secret)
	client = oauth2.Client(consumer, token)
	resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
	return content
url='https://api.twitter.com/1.1/search/tweets.json?q=%23california&src=typd'
data = oauth_req(url, TOKEN_KEY, TOKEN_SECRET)
with open("/Users/jiayuan/Documents/data/project_263/tweets_data/tweets1.json", "w+") as data_file:
	data_file.write(data)
	

# Use Python OAuth2, which is a protocol for identifying and connecting securely when using APIs.
# search the results of tweets with keyword "california" with a count of 50
oauth = OAuth(TOKEN_KEY, TOKEN_SECRET, API_KEY, API_SECRET)
twitter= Twitter(auth=oauth)
iterator=twitter.search.tweets(q='#california',result_type='recent',lang='en',count=20)
with open("/Users/jiayuan/Documents/data/project_263/tweets_data/tweets2.json","w+") as data_file2:
	data_file2.write(json.dumps(iterator,indent=4))
	
# Advanced data collection from Twitter's rest API
# Tweepy can help us manage a series of requests as well as OAuth using Twitter.
# cursor can return an iterator on a per-item orper-page level. You can also define  
# limitsto determine how many pages or items thecursor grabs.
# store_tweet(item)
def store_tweet(item):
	db = dataset.connect('sqlite:///scraping_tweets3.db')
	table = db['tweets']
	item_json = item._json.copy()
	for k,v in item_json.items():
		if isinstance(v,dict):
			item_json[k] = str(v)
		table.insert(item_json)
		
auth = tweepy.OAuthHandler(API_KEY,API_SECRET)
auth.set_access_token(TOKEN_KEY,TOKEN_SECRET)
api = tweepy.API(auth)
query = '#california'
cursor = tweepy.Cursor(api.search,q = query,lang ='en')
data_file3 = open("/Users/jiayuan/Documents/data/project_263/tweets_data/tweets3.json","w+")
for page in cursor.pages():
	tweets = []
	for item in page:
		tweets.append(item._json)
		if len(tweets)>20:
			break		
print tweets
data_file3.write(json.dumps(tweets))
data_file3.close()


# Initiate the connection to Twitter Streaming API
# Stream Listener helps create a streaming session and listen to messages
# Stream handles TwitterStream.
class Listener(StreamListener):
	def on_data(self, data): 
		print data
		with open("/Users/jiayuan/Documents/data/project_263/tweets_data/tweets4.json","w") as data_file4:
			data_file4.write(data)
		return True
auth = OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(TOKEN_KEY, TOKEN_SECRET)
stream = Stream(auth, Listener())
stream.filter(track=['#california'])
import urllib2
import csv
import json
import datetime
from abc import ABCMeta
from urllib import urlencode
from abc import abstractmethod
from urlparse import urlunparse
from bs4 import BeautifulSoup
from time import sleep




class TwitterSearch:

    __metaclass__ = ABCMeta

    def __init__(self, rate_delay, error_delay=5):
        """
        :param rate_delay: How long to pause between calls to Twitter
        :param error_delay: How long to pause when an error occurs
        """
        self.rate_delay = rate_delay
        self.error_delay = error_delay

    def search(self, query):
        """
        Scrape items from twitter
        :param query:   Query to search Twitter with. Takes form of queries constructed with using Twitters
                        advanced search: https://twitter.com/search-advanced
        """
        url = self.construct_url(query)
        # # print url.......
        # print 
        #print url
        continue_search = True
        min_tweet = None
        response = self.execute_search(url)
        print url
        counter_num = 0
        while response is not None and continue_search and response['items_html'] is not None and counter_num <=100:
            
            print response
            # Parse tweets and create a tweets list
            tweets = self.parse_tweets(response['items_html'])

            # If we have no tweets, then we can break the loop early
            if len(tweets) == 0:
                break
            # Set a counter to count the number of tweets and print the nunber
            counter_num = counter_num + len(tweets)
            print counter_num

            # If we haven't set our min tweet yet, set it now
            if min_tweet is None:
                min_tweet = tweets[0]

            continue_search = self.save_tweets(tweets)

            # Our max tweet is the last tweet in the list
            max_tweet = tweets[-1]
            if min_tweet['tweet_id'] is not max_tweet['tweet_id']:

                max_position = "TWEET-%s-%s" % (
                    max_tweet['tweet_id'], min_tweet['tweet_id'])
                url = self.construct_url(query, max_position=max_position)
                # Sleep for our rate_delay
                sleep(self.rate_delay)
                response = self.execute_search(url)

    def execute_search(self, url):
        """
        Executes a search to Twitter for the given URL
        :param url: URL to search twitter with
        :return: A JSON object with data from Twitter
        """
        try:
            # Specify a user agent to prevent Twitter from returning a profile
            # card
            headers = {
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
            }
            req = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(req)
            data = json.loads(response.read())
            return data

        # If we get a ValueError exception due to a request timing out, we sleep for our error delay, then make
        # another attempt
        except ValueError as e:
            print e.message
            print "Sleeping for %i" % self.error_delay
            sleep(self.error_delay)
            return self.execute_search(url)

    @staticmethod
    def parse_tweets(items_html):
        """
        Parses Tweets from the given HTML
        :param items_html: The HTML block with tweets
        :return: A JSON list of tweets
        """
        soup = BeautifulSoup(items_html, "html.parser")
        tweets = []
        for li in soup.find_all("li", class_='js-stream-item'):

            # If our li doesn't have a tweet-id, we skip it as it's not going
            # to be a tweet.
            if 'data-item-id' not in li.attrs:
                continue

            tweet = {
                'tweet_id': li['data-item-id'],
                'text': None,
                'user_id': None,
                'user_screen_name': None,
                'user_name': None,
                'created_at': None,
                'retweets': 0,
                'favorites': 0
            }

            # Tweet Text
            text_p = li.find("p", class_="tweet-text")
            if text_p is not None:
                tweet['text'] = text_p.get_text().encode('utf-8')

            # Tweet User ID, User Screen Name, User Name
            user_details_div = li.find("div", class_="tweet")
            if user_details_div is not None:
                tweet['user_id'] = user_details_div['data-user-id']
                tweet['user_screen_name'] = user_details_div['data-user-id']
                tweet['user_name'] = user_details_div['data-name']

            # Tweet date
            date_span = li.find("span", class_="_timestamp")
            if date_span is not None:
                tweet['created_at'] = float(date_span['data-time-ms'])

            # Tweet Retweets
            retweet_span = li.select(
                "span.ProfileTweet-action--retweet > span.ProfileTweet-actionCount")
            if retweet_span is not None and len(retweet_span) > 0:
                tweet['retweets'] = int(
                    retweet_span[0]['data-tweet-stat-count'])

            # Tweet Favourites
            favorite_span = li.select(
                "span.ProfileTweet-action--favorite > span.ProfileTweet-actionCount")
            if favorite_span is not None and len(retweet_span) > 0:
                tweet['favorites'] = int(
                    favorite_span[0]['data-tweet-stat-count'])

            tweets.append(tweet)
        return tweets

    @staticmethod
    def construct_url(query, max_position=None):
        """
        For a given query, will construct a URL to search Twitter with
        :param query: The query term used to search twitter
        :param max_position: The max_position value to select the next pagination of tweets
        :return: A string URL
        """

        params = {
            
            # Type Param
            'f': 'tweets',
            # Query Param
            'q': query,
            # 'lang':'en',
            # 'include_entities':'1',
            # 'include_available_features':'1',
            # 'src': 'typd'
        }

        # If our max_position param is not None, we add it to the parameters
        if max_position is not None:
            params['max_position'] = max_position
        # print ('params=', params)
        url_tuple = ('https', 'twitter.com', '/i/search/timeline',
                     '',query, urlencode(params))
        
        # show constructed url
        # print urlencode(params)
        # print urlunparse(url_tuple)
        return urlunparse(url_tuple)

    @abstractmethod
    def save_tweets(self, tweets):
        """
        An abstract method that's called with a list of tweets.
        When implementing this class, you can do whatever you want with these tweets.
        """


class TwitterSearchImpl(TwitterSearch):

    def __init__(self, rate_delay, error_delay, csv_writer):
        """
        :param rate_delay: How long to pause between calls to Twitter
        :param error_delay: How long to pause when an error occurs
        :param max_tweets: Maximum number of tweets to collect for this example
        """
        super(TwitterSearchImpl, self).__init__(rate_delay, error_delay)
        self.writer = csv_writer

    def save_tweets(self, tweets):
        """
        Prints out the tweets to a local CSV file.
        """
        print "hello"
        for tweet in tweets:
            if tweet['created_at'] is not None:
                time = datetime.datetime.fromtimestamp(
                    (tweet['created_at'] / 1000))
                fmt = "%Y-%m-%d %H:%M:%S"
                row = [tweet['text'], time.strftime(fmt), tweet['favorites'],
                       tweet['retweets'], tweet['tweet_id']]
                self.writer.writerow(row)
        return True

if __name__ == '__main__':
    # get list of a string of date time with format "yyyy-mm-dd"
    def get_date_string(start,end):
        list = []
        for n in range( ( end - start ).days):
            list.append( start + datetime.timedelta( n ) )
        l_date = []
        for d in list:
            l_date.append(d.strftime('%Y-%m-%d'))
        return l_date

    list_date = get_date_string(datetime.date( year = 2016, month = 12, day = 1 ),
                             datetime.date( year = 2016, month = 12, day = 5 ))

    # create a list of states
    list_of_state = ['ALABAMA','ALASKA','ARIZONA','ARKANSAS','CALIFORNIA','COLORADO','CONNECTICUT',
                    'DELAWARE','FLORIDA','GEORGIA','HAWAII','IDAHO','ILLINOIS','INDIANA','IOWA','KANSAS',
                    'KENTUCKY','LOUISIANA','MAINE','MARYLAND','MASSACHUSETTS','MICHIGAN','MINNESOTA',
                    'MISSISSIPPI','MISSOURI','MONTANA','NEBRASKA','NEVADA','NEW%20HAMPSHIRE','NEW%20JERSEY',
                    'NEW%20MEXICO','NEW%20YORK','NORTH%20CAROLINA','NORTH%20DAKOTA','OHIO','OKLAHOMA','OREGON',
                    'PENNSYLVANIA','RHODE%20ISLAND','SOUTH%20CAROLINA','SOUTH%20DAKOTA','TENNESSEE','TEXAS','UTAH',
                    'VERMONT','VIRGINIA','WASHINGTON','WEST%20VIRGINIA','WISCONSIN','WYOMING']

    '''
    counstruct a query string 
    query_str = 'q=Donald%20Trump%20near%3A%22' + state + '%22%20within%3A15mi%20since%3A' + list_date[0] + '%20until%3A' +list_date[1]
    '''

    # for state in list_of_state:
    #     print state
    state = 'VIRGINIA'
    for i in range(0,len(list_date) - 1,2):
        result_file = "/Users/jiayuan/Documents/data/project_263/tweets_bystate／" + state + list_date[i] + ".csv"
        query_str = 'q=Donald%20Trump%20near%3A%22' + state + '%22%20within%3A15mi%20since%3A' + list_date[i] + '%20until%3A' +list_date[i + 1]
        with open(result_file, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Text", "Date", "Favorites", "Retweets", "Tweet ID"])
            twit = TwitterSearchImpl(0, 5, writer)
            twit.search(query_str)
from textblob import TextBlob
import pandas as pd

class ReviewClient(object):
    '''
    Generic Review Class for sentiment analysis.
    '''
    def get_review_sentiment(self, review):
        '''
        Utility function to classify sentiment of passed review
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(review)
        # set sentiment
        if analysis.sentiment.polarity > 0.2:
            return 'positive'
        elif -0.1 < analysis.sentiment.polarity <= 0.2:
            return 'neutral'
        else:
            return 'negative'

    def get_reviews(self, query, count=10):
        '''
        Main function to fetch reviews.
        '''

        # empty list to store reviews
        reviews = []

        try:
            # call twitter api to fetch tweets
            csv_data = df.read_csv('C:/Users/jeanc/Documents/reviews/items_trustpilot_' + razer + '_clean.csv',
                                 encoding='utf-8', index=False)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

                    # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

# calling function to get tweets
tweets = api.get_tweets(query='Razer', count=200)

# picking positive tweets from tweets
ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
# percentage of positive tweets
print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
# picking negative tweets from tweets
ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

tweets_len = len(tweets)
ptweets_len = len(ptweets)
ntweets_len = len(ntweets)

# percentage of negative tweets
print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
# percentage of neutral tweets
print("Neutral tweets percentage: {} % \ ".format(100 * (tweets_len - ptweets_len - ntweets_len) / len(tweets)))

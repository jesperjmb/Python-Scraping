#Scrape tweets from Twitter by the use of the snscrape library
#The snscrape library was developed by https://github.com/JustAnotherArchivist/snscrape.

#This example will scrape tweets based on the keyword "vertical farming"

#snscrape can be installed using pip: "pip3 install snscrape"

#Import snscrape and pandas
import snscrape.modules.twitter as sntwitter
import pandas as pd

# Create a list to append tweet data to
tweets_list = []

#A list of search parameters can be found at https://github.com/JustAnotherArchivist/snscrape/blob/ffd9289edc5bab32e1e2314e7c04b4da9c933867/snscrape/modules/twitter.py#L20-L42
# Using TwitterSearchScraper to scrape data and append tweets to list. 
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('vertical farming since:2012-01-01 until:2021-04-05, include:nativeretweets filter:retweets').get_items()):
    if i>150000: #We define the max amount of tweets to scrape
        break
        #We define the meta we want to save from the scraped tweets
    tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.outlinks, tweet.retweetCount, tweet.likeCount, tweet.replyCount,  tweet.user.username, tweet.url, tweet.mentionedUsers])
    
# We create a dataframe from the tweets list above
df_tweets = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Content links', 'Retweet count', 'Likes', 'Replies',  'Username', 'URL', 'Mentions'])

#We save the tweets to a csv file
df_tweets.to_csv('verticalfarming-tweets.csv',index = False, encoding='utf-8')
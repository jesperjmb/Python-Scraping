#Import needed libraries
import pandas as pd
import botometer

#Setup the API keys for Twitter and Botometer
rapidapi_key = "YOUR KEY"
twitter_app_auth = {
    'consumer_key': 'YOUR KEY',
    'consumer_secret': 'YOUR KEY',
    'access_token': 'YOUR KEY',
    'access_token_secret': 'YOUR KEY',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

#Note: the following example uses a predefined list of Twitter usernames scraped from Twitter.
#See the following tutorail if you wish to scrape your own list of usernames: https://github.com/jesperjmb/Python-Scraping/tree/main/scraping-twitter

#We import the list of Twitter usernames
df_twitter = pd.read_csv('twitter-usernames.csv', delimiter=',',encoding='utf-8', header = 0, index_col=None)

#We add @ to all usernames as required by Botometer. Only needed if the usernames list does not already include @
df_twitter['Username'] = '@' + df_twitter['Username'].astype(str)

#We create a new dataframe we wish to populate with the Botometer data (optional)
df = pd.DataFrame(columns=['Username', 'Rating'])

#We create the list to populate with the overall rating
result_lists = []

#We look up each of the usernames in the list
for screen_name, result in bom.check_accounts_in(username_list):
    #We define what stat we want.
    result_list = result #Can be further specified of only some Botometer data is needed. For example if only the overall rating is needed: "result['display_scores']['english']['overall']"
    #We append it to the list
    result_lists.append(result_list)
#We insert the Botometer ratings into the dataframe
for i, row in enumerate(df.itertuples()):
    df['Rating'][i] = result_lists[i]
#We export the Botometer data to a CSV file
df.to_csv('botometer_rating.csv',index = False, encoding='utf-8')

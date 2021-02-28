#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 09:24:07 2021

@author: ladpice
"""

"""
The goal of this script is to identify subscribers of specific page and collect tweets
of these subscribers
"""

## Packages loading

import pandas as pd
import tweepy as tw
import sys, csv


## Personal Tweet Credentials

consumer_key            = "5hiCZC3iSItNH5YkxpW12T8sy"   #"5hiCZC3iSItNH5YkxpW12T8sy"
consumer_secret         = "nkpzKsNU6ZawTxC84oX2VZx1fkaVSP1raPEdhliYL12y6JIqbI"#"nkpzKsNU6ZawTxC84oX2VZx1fkaVSP1raPEdhliYL12y6JIqbI"
access_token            = "1242160228105412614-xKlFF37uGDNZ4KjN1KGYfQCrdPxN6x"#"1242160228105412614-Ov3rk4g9H3Y3NTJRRHRbsdDEO4oslA"
access_token_secret     = "yUuEvf9xvJ2rTDU7m3UEf74h12Kk3J3LhN5Q4mgL2QcTk"#"Rd28Bvo5jf1hdkzcd9W7sWysY6q4wdZQfqRExaqTZdYlG"

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)

KEYWORDS = "covid|coronavirus|cov19|cov-19|2019ncov|ncov2019|ncov19|covid19|corona"

# Get a list of follower ids for the target account
def get_follower_ids(target):
    try:
        return api.followers_ids(target)
    except tw.TweepError:
        print("Failed to run the command on that user, Skipping...")
    

def get_user_objects(follower_ids):
    
    batch_len = 100
    num_batches = len(follower_ids) / 100
    batches = (follower_ids[i:i+batch_len] for i in range(0, len(follower_ids), batch_len))
    followers_screen_name  = []

    for batch_count, batch in enumerate(batches):
        sys.stdout.write("\r")
        sys.stdout.flush()
        sys.stdout.write("Fetching batch: " + str(batch_count) + "/" + str(num_batches))
        sys.stdout.flush()
        users_list = api.lookup_users(user_ids=batch)
        
        screen_name_list = [user.screen_name for user in users_list]
        
        followers_screen_name += screen_name_list

    return followers_screen_name

def get_tweet_by_username(country_screen_name, screen_name):
    
    try:
        alltweets = []  
        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name = screen_name,count=200, tweet_mode="extended")
        if len(new_tweets) > 1:
            #save most recent tweets
            alltweets.extend(new_tweets)
            #save the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
    
            #keep grabbing tweets until there are no tweets left to grab
            while len(new_tweets) > 0:
                #print(f"getting tweets before {oldest}")
        
                #all subsiquent requests use the max_id param to prevent duplicates
                new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest,tweet_mode="extended")
        
                #save most recent tweets
                alltweets.extend(new_tweets)
        
                #update the id of the oldest tweet less one
                oldest = alltweets[-1].id - 1
        
                #print(f"...{len(alltweets)} tweets downloaded so far")
            ## Recuperer les informations dont nous avons besoin
            outtweets = []
            for tweet in alltweets:
                if tweet.full_text.str.contains(KEYWORDS,case=False,na=False):
                    try:
                    
                
            ## Rajout du screen_name
            outtweets = [[country_screen_name,tweet.id_str,tweet.created_at,tweet.full_text,tweet.source, tweet.truncated,\
                  tweet.in_reply_to_user_id,tweet.in_reply_to_status_id_str,tweet.in_reply_to_screen_name,\
                  tweet.retweet_count,tweet.retweeted,tweet.lang] for tweet in alltweets \
                         if tweet.full_text.str.contains(KEYWORDS,case=False,na=False)]
            return outtweets
    except tw.TweepError:
        print("Failed to run the command on that user, Skipping...")
       
for target in pd.read_csv("../Data/countries_tweet_accounts.csv",sep=";")["Account"]:
    print("*"*50)
    print(target)
    print("*"*50)           
    for screen_name in get_user_objects(get_follower_ids(target)):
        data = get_tweet_by_username(target,screen_name)
        if data != None:
            with open("../Data/PublicData.csv",'a') as f:
                writer = csv.writer(f)
                writer.writerows(data)

"""            
output = pd.read_csv("subscribersData.csv",header=None)
output.columns = ["id_str","created_at","text","source","truncated","in_reply_to_status_id",\
                "in_reply_to_status_id_str","in_reply_to_screen_name","retweet_count","retweeted","lang"]

data_mask = output[output.text.str.contains("masque")]   
data_mask.to_csv("EricdataSubscribers.csv", index=False)
"""

"""
data = get_tweet_by_username("francoislegault")
tweet_text = pd.DataFrame(data=data, columns=["id","created_at",
                        "text","source","truncated","in_reply_to_status_id",
                        "in_reply_to_status_id_str","in_reply_to_screen_name",
                        "retweet_count","retweeted","lang"])

data_mask = tweet_text[tweet_text.text.str.contains("masque",case=False)]
data_mask.to_csv("EricdataFinal.csv", index=False)

print("*"*30)
print(data_mask.shape)
print("*"*30)
"""


















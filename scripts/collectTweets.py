## Package Loading
import pandas as pd
import tweepy as tw
import sys, csv



## Personal Tweet Credentials

CONSUMER_KEY            = ""   
CONSUMER_SECRET         = ""
ACCESS_TOKEN            = ""
ACCESS_TOKEN_SECRET     = ""

auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tw.API(auth)


# Get a list of follower ids for the target account
def get_follower_ids(target):
    
    """
    Parameters
    ----------
    target : String
        The user screen name of countries's health ministries .

    Returns
    -------
    List of followers id

    """
    try:
        return api.followers_ids(target)
    except tw.TweepError:
        print("Failed to run the command on that user, Skipping...")
    

def get_user_objects(follower_ids):
    
    """   
    Parameters
    ----------
    follower_ids : String
        Follower's Id.

    Returns
    -------
    followers_screen_name : List of screen_names
        DESCRIPTION.

    """
    
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
                
                subset_tweet = [country_screen_name,tweet.id_str,tweet.created_at,tweet.full_text,tweet.source, tweet.truncated,\
                                tweet.in_reply_to_user_id,tweet.in_reply_to_status_id_str,tweet.in_reply_to_screen_name,\
                                tweet.retweet_count,tweet.retweeted,tweet.lang]
                try:
                    subset_tweet.append(tweet.retweeted_status.id_str)
                    subset_tweet.append(tweet.retweeted_status.full_text)
                except:
                    subset_tweet.append("")
                    subset_tweet.append("")
                        
                outtweets.append(subset_tweet)
 
            return outtweets
    except tw.TweepError:
        print("Failed to run the command on that user, Skipping...")
       
### Save tweets into .csv file
        
for target in pd.read_csv("../Data/countries_tweet_accounts.txt",sep=";")["Account"]:
    print("*"*50)
    print(target)
    print("*"*50)           
    for screen_name in get_user_objects(get_follower_ids(target)):
        data = get_tweet_by_username(target,screen_name)
        if data != None:
            with open("../Data/PublicData.csv",'a') as f:            
                writer = csv.writer(f)
                writer.writerows(data)



















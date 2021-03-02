import pandas as pd
from glob import glob
import datetime

class GetData:
    """
    This class is to collect tweet and save them on csv.files and finally gather them
    """
    
    def __init__(self,path):
        
        self.path = path
        self.keywords = "covid|coronavirus|cov19|cov-19|2019ncov|ncov2019|ncov19|covid19|corona"
    
    
    def retrieve_tweets(self):
        """
        This function gathers different filenames into single dataframe
        and retrieve only tweets related to covid 

        Returns
        -------
        df : TYPE
            DESCRIPTION.

        """
        country_data = pd.read_csv(self.path+"countries_tweet_accounts.txt",sep=";")[["Account","Pays"]]

        data = pd.concat([pd.read_csv(data,header=None) for data in glob(self.path+"*.csv")])
        data.columns = ["Account","id_str","created_at","full_text","source","truncated","in_reply_to_status_id",\
                "in_reply_to_status_id_str","in_reply_to_screen_name","retweet_count","retweeted","lang","original_tweet_id",\
               "original_text"]
            
        df = data.merge(country_data, on=['Account'], how='left')
                
        df = df[df["full_text"].str.contains(self.keywords,case=False,na=False)]
        
        df["date"] = df["created_at"].apply(lambda x: \
                                    datetime.datetime.strptime(x.split(" ")[0],'%Y-%m-%d'))
        
        return df.sort_values(by='date').reset_index()
        
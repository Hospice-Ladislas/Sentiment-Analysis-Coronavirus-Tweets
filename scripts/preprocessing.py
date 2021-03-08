import nltk
from nltk.corpus import stopwords
import string
import pandas as pd
#from google_trans_new import google_translator

class Preprocessing:
    """
    """
    def __init__(self, data, lst_word_to_delete):
        
        self.df = data
        self.lst_words = lst_word_to_delete
        
        
    def remove_words(self,tweet,lang):
        
        
        preliminary_filter = [word for word in tweet.split(" ") if "@" not in word]
        tweet = " ".join(preliminary_filter)
        transformation = str.maketrans('','',string.punctuation)
        lst_words = [word.lower() for word in tweet.translate(transformation).split() \
                     if word.lower() not in stopwords.words(lang)]
        lst_words = [word for word in lst_words if "http" not in word]
        lst_words = [word for word in lst_words if word not in self.lst_words]
        
        return " ".join(lst_words)
    
    def remove_some_words(self):
        
        data_en, data_fr = self.df[self.df["lang"]=="en"], self.df[self.df["lang"]=="fr"]
        
        #translator = google_translator() 
        #data_fr['full_text'] = data_fr['full_text'].apply(translator.translate, lang_src='fr', lang_tgt='en')
        
        
        data_en["full_text"] = data_en["full_text"].map(lambda x: self.remove_words(x,"english"))
        data_fr["full_text"] = data_fr["full_text"].map(lambda x: self.remove_words(x,"french"))      

        return pd.concat([data_en, data_fr])

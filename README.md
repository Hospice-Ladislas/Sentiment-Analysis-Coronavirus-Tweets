# Sentiment-Analysis-Coronavirus-Tweets

This project aims to collect African health ministries and their subscribers tweets related to COVID-19 for analyzing people's sentiments about this disease over time.

# Concepts

This project is a Python project. The structure of this package is :

```
+-- Data/     # Access data for project: It contains health ministries Twitter Account and 
              # credentials.json (to fill by your own credentials) for scraping tweets
              
+-- scripts/  # Contains project scripts
   -- collectTweets.py : Script for collecting tweets via TwitterAPI. Launch it by : python collectTweets.py
   -- get_data.py : Open tweets (output of collectTweets.py) as Pandas DataFrame
   -- graphAnalysis.py : Contains functions about graphmining part 
   -- model.py : This script contains class for Sentiment Prediction by Vader Lexicon
   -- preprocessing.py : Some preprocessing functions as remove stop words, delete some no useful words, ...
   -- visualisation.py : Functions about our visualization
   
+-- Sentiment-Analysis.ipynb : Exploration and results presentation 
``` 

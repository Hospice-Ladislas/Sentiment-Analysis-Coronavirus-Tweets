from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



class SentimentPrediction:
    
    """
    This class is to predict sentiment of each tweet
    """
    
    def __init__(self, data):
        self.df = data
        
        
    def vader_prediction(self):
        
        """
        Vader's Prediction
        """
        
        analyser = SentimentIntensityAnalyzer()
        self.df["compound"] = self.df["full_text"].map(lambda x: \
                                analyser.polarity_scores(x)["compound"])
        self.df["sentiment"] = self.df["compound"].map(lambda x: "Negative" if x<=-0.05 \
                                else ("Neutral" if x<0.05 else "Positive"))
            
        return self.df
        
    
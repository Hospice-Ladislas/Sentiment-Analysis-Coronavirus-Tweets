import matplotlib.pyplot as plt
import seaborn as sbn
sbn.set(style='darkgrid')
from wordcloud import WordCloud
 
class Visualization:
    
    """
    
    """
    def __init__(self, data, lang):
        self.df = data
        self.lang = lang
        
    #def word_cloud(self, lst_word_to_delete):
    def word_cloud(self):
        """
        Generate Word Cloud

        Parameters
        ----------
        lst_word_to_delete : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        lang_data = self.df[self.df["lang"]==self.lang]
        comment_words = ''
        comment_words += " ".join(lang_data["full_text"])+" "
    
        clean_corpus_array = [x for x in comment_words.split(" ") ] #if x not in lst_word_to_delete]
        clean_corpus = " ".join(clean_corpus_array)
    
        wordcloud = WordCloud(width=800,height=800,background_color ='white',min_font_size = 10).generate(clean_corpus)
                       
        plt.figure(figsize = (8, 8), facecolor = None) 
        plt.imshow(wordcloud,interpolation='bilinear') 
        plt.axis("off") 
        plt.tight_layout(pad = 0)
        #plt.savefig("../Graphique/WordCloudUnigram_"+lang+".png")
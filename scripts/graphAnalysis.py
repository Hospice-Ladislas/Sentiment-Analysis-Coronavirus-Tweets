import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


class GraphAnalysis:
    
    """
    This class goal is to do graph analysis.
    Inspired from https://github.com/ugis22/analysing_twitter/blob/master/Jupyter%20Notebook%20files/Interaction%20Network.ipynb
    """
    
    def __init__(self, data):
        self.df = data
        
    def transform_data(self):
        
        df1, df2 = self.df[["id_str","in_reply_to_status_id_str"]].rename(columns={"in_reply_to_status_id_str":"retweet_reply_id"}).dropna(), \
                    self.df[["id_str","original_tweet_id"]].rename(columns={"original_tweet_id":"retweet_reply_id"}).dropna()
        df_graph = pd.concat([df1,df2])
        df_graph['id_str'] = df_graph['id_str'].astype(str)
        df_graph['retweet_reply_id'] = df_graph['retweet_reply_id'].astype(str)
        return df_graph
        

    # Get the interactions between the different users
    def get_interactions(self,row):
        # From every row of the original dataframe
        # First we obtain the 'original tweet id'
        original_tweet = row["retweet_reply_id"]
    
        # The interactions are going to be a set of tuples
        interactions = set()
    
        # Add all interactions 
        # First, we add the interactions corresponding to replies and retweets
        interactions.add(row["id_str"])

        # Return user and interactions
        return original_tweet, interactions
    
    
    def build_graph(self):
        graph = nx.Graph()
        for index, tweet in self.transform_data().iterrows():
            original_tweet, interactions = self.get_interactions(tweet)
            
            for interaction in interactions:
                #int_id = interaction
                graph.add_edge(original_tweet, interaction)
        

                graph.nodes[original_tweet]["name"] = original_tweet
                graph.nodes[interaction]["name"] = interaction
                
        return graph
    
    def graph_viz(self):
        
        """
        Visualize the graph
        """
        
        plt.figure(figsize = (20,20))
        
        graph = self.build_graph()
        pos = nx.spring_layout(graph, k=0.05)
                
        nx.draw(graph, pos=pos,  cmap=plt.cm.PiYG, edge_color="black", \
                linewidths=0.3, node_size=60, alpha=0.6, with_labels=False)
        nx.draw_networkx_nodes(graph, pos=pos, node_size=300)
        plt.show()
        
    
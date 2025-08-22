'''
PART 2: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Build a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is inline with the standards we're using in this class 
'''

import numpy as np
import pandas as pd
import networkx as nx
import json
import os
from datetime import datetime

def nc():
    # Build the graph
    g = nx.Graph()

    with open("imdb_movies_2000to2022.prolific.json", "r", encoding="utf-8") as in_file:
        for line in in_file:
            # Load the movie from this line
            this_movie = json.loads(line)
            
            # Create a node for every actor
            for actor_id, actor_name in this_movie['actors']:
                g.add_node(actor_name)
        
            i = 0 #counter
            for left_actor_id, left_actor_name in this_movie['actors']:
                for right_actor_id, right_actor_name in this_movie['actors'][i+1:]:
                    if g.has_edge(left_actor_name, right_actor_name):
                        g[left_actor_name][right_actor_name]['weight'] += 1
                    else:
                        g.add_edge(left_actor_name, right_actor_name, weight=1)
                i += 1

    # Print the info below
    print("Nodes:", len(g.nodes))

    #Print the 10 the most central nodes
    centrality = nx.degree_centrality(g)
    top10 = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    print("Top 10 central actors:", top10)

    df = pd.DataFrame(top10, columns=["actor","centrality"])
    out_path = os.path.join("data", f"network_centrality_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
    df.to_csv(out_path, index=False)
    return df

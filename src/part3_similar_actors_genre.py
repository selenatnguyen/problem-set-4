'''
PART 2: SIMILAR ACTROS BY GENRE

Using the imbd_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- - As an example, select the row from your data frame associated with Chris Hemsworth, actor ID “nm1165110”, as your “query” actor
- Use sklearn.metrics.DistanceMetric to calculate the euclidean distances between your query actor and all other actors based on their genre appearances
- - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html
- Output a CSV continaing the top ten actors most similar to your query actor using cosine distance 
- - Name it 'similar_actors_genre_{current_datetime}.csv' to `/data`
- - For example, the top 10 for Chris Hemsworth are:  
        nm1165110 Chris Hemsworth
        nm0000129 Tom Cruise
        nm0147147 Henry Cavill
        nm0829032 Ray Stevenson
        nm5899377 Tiger Shroff
        nm1679372 Sudeep
        nm0003244 Jordi Mollà
        nm0636280 Richard Norton
        nm0607884 Mark Mortimer
        nm2018237 Taylor Kitsch
- Describe in a print() statement how this list changes based on Euclidean distance
- Make sure your code is in line with the standards we're using in this class
'''

#Write your code below
import os
import json
import pandas as pd
import numpy as np
from sklearn.metrics import DistanceMetric
from datetime import datetime

def sag():
    rows = []
    file_path = os.path.join(os.path.dirname(__file__), '..', 'imdb_movies_2000to2022.prolific.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            movie = json.loads(line)
            genres = movie.get('genres', [])
            actors = movie.get('actors', [])
            for actor_id, actor_name in actors:
                for genre in genres:
                    rows.append([actor_id, actor_name, genre])

    df = pd.DataFrame(rows, columns=['actor_id','actor_name','genre'])
    actor_genre = df.pivot_table(
        index=['actor_id','actor_name'], 
        columns='genre',
        aggfunc='size',
        fill_value=0
    )

    matrix = actor_genre.values
    actor_index = actor_genre.index

    if "nm1165110" not in actor_index.get_level_values(0):
        print("Chris Hemsworth not found in dataset.")
        return None
    query_position = list(actor_index.get_level_values(0)).index("nm1165110")
    query_vector = matrix[query_position].reshape(1, -1)

    cosine_dist = DistanceMetric.get_metric("cosine").pairwise(query_vector, matrix)[0]
    euclidean_dist = DistanceMetric.get_metric("euclidean").pairwise(query_vector, matrix)[0]

    sorted_cos = np.argsort(cosine_dist)
    sorted_euc = np.argsort(euclidean_dist)

    top10_cos_idx = [i for i in sorted_cos if i != query_position][:10]
    results = [(actor_index[i][0], actor_index[i][1], float(cosine_dist[i])) for i in top10_cos_idx]

    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, f"similar_actors_genre_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
    pd.DataFrame(results, columns=["actor_id","actor_name","cosine_distance"]).to_csv(out_path, index=False)

    top10_euc_idx = [i for i in sorted_euc if i != query_position][:10]
    cos_names = [actor_index[i][1] for i in top10_cos_idx]
    euc_names = [actor_index[i][1] for i in top10_euc_idx]
    print("Top 10 (cosine):", cos_names)
    print("Top 10 (euclidean):", euc_names)

    return results

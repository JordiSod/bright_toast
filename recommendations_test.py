# In[ ]:

import pandas as pd
import numpy as np
from registry import *

wine_word2vec_model = load_word2vec_model()
model_knn = load_knn_model()
dict_of_tfidf_weightings = load_tfidf_weights()
wine_reviews_mincount = load_wine_reviews_mincount()

descriptor_mapping = pd.read_csv('descriptor_mapping.csv').set_index('raw descriptor')


def descriptors_to_best_match_wines(list_of_descriptors, wineset=wine_reviews_mincount, number_of_suggestions=10):
    weighted_review_terms = []
    for term in list_of_descriptors:
        if term not in dict_of_tfidf_weightings:
            if term not in descriptor_mapping.index:
                print('choose a different descriptor from', term)
                continue
            else:
                term = descriptor_mapping['normalized'][term]
        tfidf_weighting = dict_of_tfidf_weightings[term]
        word_vector = wine_word2vec_model.wv.get_vector(term).reshape(1, 300)
        weighted_word_vector = tfidf_weighting * word_vector
        weighted_review_terms.append(weighted_word_vector)
    review_vector = sum(weighted_review_terms)

    distance, indice = model_knn.kneighbors(review_vector, n_neighbors=len(wine_reviews_mincount))
    distance_list = distance[0].tolist()[1:]
    indice_list = indice[0].tolist()[1:]

    n = 1
    for d, i in zip(distance_list, indice_list):
        if i in wineset.index:
            wine_name = wineset['title'][i]
            wine_descriptors = wineset['normalized_descriptors'][i]
            print('Suggestion', str(n), ':', wine_name, 'with a cosine distance of', "{:.3f}".format(d))
            print('This wine has the following descriptors:', wine_descriptors)
            print('')
            n+=1
        if n == number_of_suggestions + 1:
            break

# In[ ]:
descriptors = ['apple','pear','wood']
descriptors_to_best_match_wines(list_of_descriptors=descriptors, number_of_suggestions=5)
# %%

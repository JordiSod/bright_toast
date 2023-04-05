# In[ ]:

import pandas as pd
import numpy as np
from registry import *

wine_word2vec_model = load_word2vec_model()
model_knn = load_knn_model()
dict_of_tfidf_weightings = load_tfidf_weights()
wine_reviews_mincount = load_wine_reviews_mincount()
# wine_word2vec_model, model_knn, dict_of_tfidf_weightings, wine_reviews_mincount = local_load_files()
descriptor_mapping = pd.read_csv('descriptor_mapping.csv').set_index('raw descriptor')


# %%
def separator(text: str):
    '''
    Converts strings from the API input into lists
    '''

    text = text.replace('_',' ').split(' ')
    for i in range(len(text)):
        text[i] = text[i].replace('+',' ')
    return text
# %%

def candidate_selector(countries, varieties, min_price, max_price):
    '''
    Returns a dataframe of wine candidates filtered by the parameters provided
    '''
# candidate_selector(['Spain'],0,10)

    wineset = wine_reviews_mincount.copy()
    wineset = wineset.loc[wineset['country'].isin(countries)]
    wineset = wineset.loc[wineset['variety'].isin(varieties)]

    wineset = wineset[(wineset['price'] >= min_price)
                          & (wineset['price'] <= max_price)]




    return wineset


# %%
def recommendations(list_of_descriptors, wineset=wine_reviews_mincount, number_of_suggestions=10):
    '''
    Returns a dictionary with wine recommendations.
    Output includes the a recommendation number , a wine title,
    and a list of descriptors.
    '''
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

#'country', 'description', 'designation', 'points',
#       'price', 'province', 'region_1', 'title', 'variety', 'winery'

    winedict = {}
    n = 1
    for d, i in zip(distance_list, indice_list):
        if i in wineset.index:

            country = wineset['country'][i]
            description = wineset['description'][i]
            designation = wineset['designation'][i]
            points = wineset['points'][i]
            price = wineset['price'][i]
            province = wineset['province'][i]
            region_1 = wineset['region_1'][i]
            title = wineset['title'][i]
            variety = wineset['variety'][i]
            winery = wineset['winery'][i]
            wine_descriptors = wineset['normalized_descriptors'][i]

            winedict[n] = {'country': country,
#                            'description':description,
#                            'designation': designation,
#                            'points': points,
                            'price': price,
#                            'province': province,
#                            'region_1': region_1,
                            'title': title,
                            'variety': variety,
#                            'winery': winery,
                            'wine_descriptors': wine_descriptors,
#                            'cosine_distance': d
                           }

#            print('Suggestion', str(n), ':', title, 'with a cosine distance of', "{:.3f}".format(d))
#            print('This wine has the following descriptors:', wine_descriptors)
#            print('')
            n+=1
        if n == number_of_suggestions + 1:
            break
    return winedict

# %%
def rec2(list_of_descriptors, countries, min_price, max_price, wineset=wine_reviews_mincount, number_of_suggestions=10):
    '''
    Returns a dictionary with wine recommendations.
    Output includes the a recommendation number , a wine title,
    and a list of descriptors.
    '''
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
    wineset = wineset.loc[indice_list]
# Filter wineset by country, etc.
    if countries != ['All']: wineset = wineset.loc[wineset['country'].isin(countries)]
    wineset = wineset[(wineset['price'] >= min_price)
                        & (wineset['price'] <= max_price)]


#'country', 'description', 'designation', 'points',
#       'price', 'province', 'region_1', 'title', 'variety', 'winery'

    winedict = {}
    n = 1
    for d, i in zip(distance_list, indice_list):
        if i in wineset.index:

            country = wineset['country'][i]
            description = wineset['description'][i]
            designation = wineset['designation'][i]
            points = wineset['points'][i]
            price = wineset['price'][i]
            province = wineset['province'][i]
            region_1 = wineset['region_1'][i]
            title = wineset['title'][i]
            variety = wineset['variety'][i]
            winery = wineset['winery'][i]
            wine_descriptors = wineset['normalized_descriptors'][i]

            winedict[n] = {'country': country,
#                            'description':description,
#                            'designation': designation,
                            'points': int(points),
                            'price': price,
                            'province': province,
                            'region_1': region_1,
                            'title': title,
                            'variety': variety,
                            'winery': winery,
                            'wine_descriptors': wine_descriptors,
#                            'cosine_distance': d
                           }

#            print('Suggestion', str(n), ':', title, 'with a cosine distance of', "{:.3f}".format(d))
#            print('This wine has the following descriptors:', wine_descriptors)
#            print('')
            n+=1
        if n == number_of_suggestions + 1:
            break
    return winedict

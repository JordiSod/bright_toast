#!/usr/bin/env python
# coding: utf-8

# In[2]:


import boto3
import os
import sagemaker
from sagemaker import get_execution_role
import pandas as pd

import numpy as np
import string
from operator import itemgetter
from collections import Counter, OrderedDict

import nltk
# nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
# nltk.download('stopwords')

from gensim.models.phrases import Phrases, Phraser
from gensim.models import Word2Vec

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt


# # .-Cargando los datos

# In[3]:


wine_data = pd.read_csv('./winemag-data-130k-v2.csv')
wine_data.head()


# ##### Quitando las columnas que no agregan informacion

# In[4]:


wine_data = wine_data.drop(columns=['Unnamed: 0','taster_name','taster_twitter_handle','region_2'])


# In[5]:


wine_data


# In[6]:


wine_dataset_relevant = wine_data[['title', 'description']]
wine_dataset_relevant.head(10)


# ##### Extraemos las descripciones y las guardamos en una lista

# In[8]:


reviews_list = list(wine_data['description'])
reviews_list = [str(r) for r in reviews_list]
full_corpus = ' '.join(reviews_list)
sentences_tokenized = sent_tokenize(full_corpus)

print(sentences_tokenized[:5])


# ##### Limpiamos las descripciones

# In[9]:


stop_words = set(stopwords.words('english'))

punctuation_table = str.maketrans({key: None for key in string.punctuation})
sno = SnowballStemmer('english')

def normalize_text(raw_text):
    try:
        word_list = word_tokenize(raw_text)
        normalized_sentence = []
        for w in word_list:
            try:
                w = str(w)
                lower_case_word = str.lower(w)
                stemmed_word = sno.stem(lower_case_word)
                no_punctuation = stemmed_word.translate(punctuation_table)
                if len(no_punctuation) > 1 and no_punctuation not in stop_words:
                    normalized_sentence.append(no_punctuation)
            except:
                continue
        return normalized_sentence
    except:
        return ''

# sentence_sample = sentences_tokenized[:10]
normalized_sentences = []
for s in sentences_tokenized:
    normalized_text = normalize_text(s)
    normalized_sentences.append(normalized_text)


# In[11]:


phrases = Phrases(normalized_sentences)
phrases = Phrases(phrases[normalized_sentences])

ngrams = Phraser(phrases)

phrased_sentences = []
for sent in normalized_sentences:
    phrased_sentence = ngrams[sent]
    phrased_sentences.append(phrased_sentence)

full_list_words = [item for sublist in phrased_sentences for item in sublist]


# In[12]:


word_counts = Counter(full_list_words)
sorted_counts = OrderedDict(word_counts.most_common(5000))
counter_df = pd.DataFrame.from_dict(sorted_counts, orient='index')
# top_5000_words = counter_df.head(5000)
counter_df.to_csv('top_5000_descriptors.csv')


# ##### Tomamos un mapping pre-creado de las principales palabras para vinos

# In[14]:


descriptor_mapping = pd.read_csv('descriptor_mapping.csv').set_index('raw descriptor')
descriptor_mapping.head(10)


# In[15]:


def return_mapped_descriptor(word):
    if word in list(descriptor_mapping.index):
        normalized_word = descriptor_mapping['level_3'][word]
        return normalized_word
    else:
        return word

normalized_sentences = []
for sent in phrased_sentences:
    normalized_sentence = []
    for word in sent:
        normalized_word = return_mapped_descriptor(word)
        normalized_sentence.append(str(normalized_word))
    normalized_sentences.append(normalized_sentence)


# In[17]:


from gensim.models import Word2Vec


# In[21]:


wine_word2vec_model = Word2Vec(normalized_sentences, vector_size=300, min_count=5, epochs=15)
print(wine_word2vec_model)

wine_word2vec_model.save('wine_word2vec_model.bin')


# In[23]:


wine_word2vec_model.wv.most_similar(positive='dry', topn=10)


# In[25]:


wine_reviews = list(wine_data['description'])

def return_descriptor_from_mapping(word):
    if word in list(descriptor_mapping.index):
        descriptor_to_return = descriptor_mapping['level_3'][word]
        return descriptor_to_return

descriptorized_reviews = []
for review in wine_reviews:
    normalized_review = normalize_text(review)
    phrased_review = ngrams[normalized_review]
    descriptors_only = [return_descriptor_from_mapping(word) for word in phrased_review]
    no_nones = [str(d) for d in descriptors_only if d is not None]
    descriptorized_review = ' '.join(no_nones)
    descriptorized_reviews.append(descriptorized_review)


# In[28]:


vectorizer = TfidfVectorizer()
X = vectorizer.fit(descriptorized_reviews)

dict_of_tfidf_weightings = dict(zip(X.get_feature_names_out(), X.idf_))

wine_review_vectors = []
for d in descriptorized_reviews:
    descriptor_count = 0
    weighted_review_terms = []
    terms = d.split(' ')
    for term in terms:
        if term in dict_of_tfidf_weightings.keys():
            tfidf_weighting = dict_of_tfidf_weightings[term]
            word_vector = wine_word2vec_model.wv.get_vector(term).reshape(1, 300)
            weighted_word_vector = tfidf_weighting * word_vector
            weighted_review_terms.append(weighted_word_vector)
            descriptor_count += 1
        else:
            continue
    try:
        review_vector = sum(weighted_review_terms)/len(weighted_review_terms)
    except:
        review_vector = []
    vector_and_count = [terms, review_vector, descriptor_count]
    wine_review_vectors.append(vector_and_count)

wine_data['normalized_descriptors'] = list(map(itemgetter(0), wine_review_vectors))
wine_data['review_vector'] = list(map(itemgetter(1), wine_review_vectors))
wine_data['descriptor_count'] = list(map(itemgetter(2), wine_review_vectors))

wine_data.reset_index(inplace=True)
wine_data.head()


# In[31]:


# first, let's eliminate any review with fewer than 5 descriptors from our dataset
wine_reviews_mincount = wine_data.loc[wine_data['descriptor_count'] > 5]
wine_reviews_mincount.reset_index(inplace=True)

variety_mapping = {'Shiraz': 'Syrah', 'Pinot Gris': 'Pinot Grigio', 'Pinot Grigio/Gris': 'Pinot Grigio',
                   'Garnacha, Grenache': 'Grenache', 'Garnacha': 'Grenache', 'CarmenÃ¨re': 'Carmenere',
                    'GrÃ¼ner Veltliner': 'Gruner Veltliner', 'TorrontÃ©s': 'Torrontes',
                   'RhÃ´ne-style Red Blend': 'Rhone-style Red Blend', 'AlbariÃ±o': 'Albarino',
                  'GewÃ¼rztraminer': 'Gewurztraminer', 'RhÃ´ne-style White Blend': 'Rhone-style White Blend'}

def consolidate_varieties(variety_name):
    if variety_name in variety_mapping:
        return variety_mapping[variety_name]
    else:
        return variety_name

wine_reviews_clean = wine_reviews_mincount.copy()
wine_reviews_clean['variety'] = wine_reviews_clean['variety'].apply(consolidate_varieties)

def subset_wine_vectors(list_of_varieties):
    wine_variety_vectors = []
    for v in list_of_varieties:
        one_var_only = wine_reviews_clean.loc[wine_reviews_clean['variety'] == v]
        review_arrays = one_var_only['review_vector'].apply(lambda x: x[0])
        average_variety_vec = np.average(review_arrays)
        wine_variety_vector = [v, average_variety_vec]
        wine_variety_vectors.append(wine_variety_vector)
    return wine_variety_vectors

def pca_wine_variety(list_of_varieties):
    wine_var_vectors = subset_wine_vectors(list_of_varieties)
    pca = PCA(n_components=2)
    pca.fit([w[1] for w in wine_var_vectors])
    pca_dataset = pca.fit_transform([w[1] for w in wine_var_vectors])
    pca_dataframe = pd.DataFrame(pca_dataset, columns=['pca_1', 'pca_2'])
    pca_dataframe.index = [w[0] for w in wine_var_vectors]
    # print(pca_dataframe)
    return pca_dataframe


# In[35]:


input_vectors = list(wine_reviews_mincount['review_vector'])
input_vectors_listed = [a.tolist() for a in input_vectors]
input_vectors_listed = [a[0] for a in input_vectors_listed]

knn = NearestNeighbors(n_neighbors=10, algorithm= 'brute', metric='cosine')
model_knn = knn.fit(input_vectors_listed)


# In[67]:


name_test = "Nicosia 2013 Vulkà Bianco"
wine_test_vector = wine_reviews_mincount.loc[wine_reviews_mincount['title'].str.contains(name_test)]['review_vector'].to_list()[0]
wine_test_vector


# In[70]:


name_test = "Nicosia 2013 Vulkà Bianco"

wine_test_vector = wine_reviews_mincount.loc[wine_reviews_mincount['title'].str.contains(name_test)]['review_vector'].tolist()[0]
distance, indice = model_knn.kneighbors(wine_test_vector, n_neighbors=9)
distance_list = distance[0].tolist()[1:]
indice_list = indice[0].tolist()[1:]

main_wine = wine_reviews_mincount.loc[wine_reviews_mincount['title'].str.contains(name_test)]

print('Wine to match:', name_test)
print('The original wine has the following descriptors:', list(main_wine['normalized_descriptors'])[0])
print('_________')

n = 1
for d, i in zip(distance_list, indice_list):
    wine_name = wine_reviews_mincount['title'][i]
    wine_descriptors = wine_reviews_mincount['normalized_descriptors'][i]
    print('Suggestion', str(n), ':', wine_name, 'with a cosine distance of', "{:.3f}".format(d))
    print('This wine has the following descriptors:', wine_descriptors)
    print('')
    n+=1


# In[75]:


def descriptors_to_best_match_wines(list_of_descriptors, number_of_suggestions=10):
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

    distance, indice = model_knn.kneighbors(review_vector, n_neighbors=number_of_suggestions+1)
    distance_list = distance[0].tolist()[1:]
    indice_list = indice[0].tolist()[1:]

    n = 1
    for d, i in zip(distance_list, indice_list):
        wine_name = wine_reviews_mincount['title'][i]
        wine_descriptors = wine_reviews_mincount['normalized_descriptors'][i]
        print('Suggestion', str(n), ':', wine_name, 'with a cosine distance of', "{:.3f}".format(d))
        print('This wine has the following descriptors:', wine_descriptors)
        print('')
        n+=1

descriptors = ['apple','pear','wood']
descriptors_to_best_match_wines(list_of_descriptors=descriptors, number_of_suggestions=5)


# In[ ]:

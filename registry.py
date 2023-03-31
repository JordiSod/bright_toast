import glob
import os
import time
import pickle
from params import *
import pandas as pd

from google.cloud import storage

def load_word2vec_model():
    storage_client = storage.Client()

    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob('wine_word2vec_model')
    pickle_in = blob.download_as_string()
    wine_word2vec_model = pickle.loads(pickle_in)
    return  wine_word2vec_model

def load_knn_model():
    storage_client = storage.Client()

    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob('model_knn')
    pickle_in = blob.download_as_string()
    model_knn = pickle.loads(pickle_in)
    return  model_knn

def load_tfidf_weights():
    storage_client = storage.Client()

    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob('dict_of_tfidf_weightings')
    pickle_in = blob.download_as_string()
    dict_of_tfidf_weightings = pickle.loads(pickle_in)
    return  dict_of_tfidf_weightings

def load_wine_reviews_mincount():
    storage_client = storage.Client()

    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob('wine_reviews_mincount')
    pickle_in = blob.download_as_string()
    wine_reviews_mincount = pickle.loads(pickle_in)
    return  wine_reviews_mincount

if __name__ == '__main__':
    load_word2vec_model()
    load_knn_model()
    load_tfidf_weights()
    load_wine_reviews_mincount()

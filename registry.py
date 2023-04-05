import glob
import os
import time
import pickle
from params import *
import pandas as pd
import joblib

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
    blob = bucket.blob('knn_train_model.pkl')
    pickle_in = blob.download_as_string()
#    model_knn = pickle.loads(pickle_in)
    model_knn = joblib.load(pickle_in)

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


def local_load_files():

    # open a file, where you stored the pickled data
    file = open('wine_word2vec_model', 'rb')

    # dump information to that file
    wine_word2vec_model = pickle.load(file)

    # close the file
    file.close()

    # Same for the rest of the files
    file = open('model_knn', 'rb')
    model_knn = pickle.load(file)
    file.close()

    file = open('dict_of_tfidf_weightings', 'rb')
    dict_of_tfidf_weightings = pickle.load(file)
    file.close()

    file = open('wine_reviews_mincount', 'rb')
    wine_reviews_mincount = pickle.load(file)
    file.close()
    return wine_word2vec_model, model_knn, dict_of_tfidf_weightings, wine_reviews_mincount

if __name__ == '__main__':
    #  load_word2vec_model()
    #  load_knn_model()
    #  load_tfidf_weights()
    #  load_wine_reviews_mincount()
    local_load_files()

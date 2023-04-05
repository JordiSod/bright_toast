FROM python:3.10.6-buster
COPY registry.py /registry.py
COPY params.py /params.py
COPY recommender.py /recommender.py
COPY wine_word2vec_model /wine_word2vec_model
COPY model_knn /model_knn
COPY dict_of_tfidf_weightings /dict_of_tfidf_weightings
COPY wine_reviews_mincount /wine_reviews_mincount
COPY descriptor_mapping.csv /descriptor_mapping.csv
COPY api.py /api.py
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn api:app --host 0.0.0.0 --port $PORT

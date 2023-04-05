# In[ ]:

from fastapi import FastAPI
import pandas as pd
from recommender import recommendations,rec2
# In[ ]:

app = FastAPI()

# Some functions to process the input.
def separator(text: str):
    '''
    Converts strings from the API input into lists
    '''

    text = text.replace('_',' ').split(' ')
    for i in range(len(text)):
        text[i] = text[i].replace('+',' ')
    return text


# Define a root `/` endpoint
@app.get('/')
def index():
    return {'ok': True}

@app.get("/predict")
# Define a predictor.
def predict(descriptors: str,
             countries: str,
             min_price: int,
             max_price: int):
    print(descriptors)
    print(countries)

    descriptors = separator(descriptors)
    countries = separator(countries)
    countries = [i.title() for i in countries]

    print(descriptors)
    print(countries)


    #Do all the magic that needs to be done!

    # return {"suggestions": recommendations(descriptors)
    return {"suggestions": rec2(descriptors,countries, min_price, max_price)
    #return {"suggestions": recapi(descriptors)
    }

    # suggestions = descriptors_to_best_match_wines(list_of_descriptors=descriptors, number_of_suggestions=5)
    # return {"suggestions": suggestions}

# http://localhost:8000/predict?descriptors=rose+wood&country=spain

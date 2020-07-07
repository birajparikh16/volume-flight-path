#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author: Biraj Parikh

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uvicorn
from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel
from typing import List, Tuple

#from config import PORT
#from personalized_recsys2 import recommend
import pandas as pd
import json

import psycopg2

# Import the 'config' funtion from the config.py file
from config import config
params = config()
# Connect to the PostgreSQL database
connection = psycopg2.connect(**params)
# Create a new cursor
cursor = connection.cursor()
connection.autocommit = True

from personalized_recsys import recommend

# Initializing an api
app = FastAPI()

# Defining a class corresponding to the consultation form
class Data(BaseModel):
    skin_type: str                      # question 1: which of the following best describes your base skin type?
    conditions: List[str] = None        # question 2: do you experience any of the following conditions?
    characteristics: List[str] = None   # question 3: how about these?
    pimples: int = None                 # question 4: how many pimples did you get in the past week?
    skin_goals: List[str]               # question 5: what are your top three #skingoals?
    category: List[str]                 # question 6: what kind of routine help are you looking for?
    price: str = None                 # question 7: i’d like to keep each product under
    preference: List[str] = None        # question 8: do you have any strong preferences?
    self_routine: List[str] = None      # question 9: do you have specific products you love and want to keep in your routine?
    brand_preference: List[str] = None  # question 10: which kinds of brands speak to you?

@app.get("/")
async def root():
  return {"message": "Apothecary welcomes you!"}
  #filtered_df.to_dict()
  

@app.post("/")
async def recommendations(data: Data):

  try:
    # Conditions
    if not data.conditions:
      conditions = ('Fungal acne', 'Eczema or psoriasis', 'Rosacea', 'Miscellaneous')
    else:
      conditions = str(data.conditions).replace('[','(').replace(']',')')

    # Characteristics
    if not data.characteristics:
      characteristics = ('Whiteheads', 'Blackheads', 'PIE', 'PIH', 'Dry patches', 'Sensitive', 'Very oily', 'Uneven tone', 'Miscellaneous')
    else:
      print(data.characteristics)
      characteristics = str(data.characteristics).replace('[','(').replace(']',')')

    # Pimples
    if not data.pimples:
      print(data.pimples)
      data.pimples = 0

    # Goals
    goals = str(data.skin_goals).replace('[','(').replace(']',')')

    # Category
    if data.category[0] == 'put together a 3-step routine for me':
      routine = ('Second Cleanser', 'SPF', 'Moisturizer')
    elif data.category[0] == 'put together a 5-step routine for me':
      routine = ('First Cleanser', 'Second Cleanser', 'Serum/Treatment', 'Moisturizer', 'SPF','Chemical Exfoliant', 'Physical Exfoliant')
    else:
      routine = str([cat for cat in data.category]).replace('[','(').replace(']',')')

    # Product Price
    if not data.price:
      data.price = '(' + 'SELECT MAX("FullSizePrice") FROM "MasterData"' + ')'

    # Preference
    all_preference = ['clear skincare', 'cruelty-free', 'fragrance-free']
    # If perference is None
    if len(data.preference) == 0:
      personal_preference = " OR ".join(["{0} LIKE '%{1}%'".format('"PreferenceTags"', w) for w in all_preference])
    else:
      personal_preference = " OR ".join(["{0} LIKE '%{1}%'".format('"PreferenceTags"', w) for w in data.preference])
      #'"ProductTags" LIKE %clear skincare% OR "ProductTags" LIKE %cruelty-free% OR "ProductTags" LIKE %fragrance-free%'

    # Brand Preference
    if data.brand_preference[0] == 'Surprise me':
      all_brands = ['prestige', 'pharmacy' , 'clinical', 'indie', 'kj beauty', 'luxury']
      brand_preference = " OR ".join(["{0} LIKE '%{1}%'".format('"BrandCategory"', w) for w in all_brands])
      #'"BrandCategory" LIKE %prestige% OR "BrandCategory" LIKE %pharmacy% OR "BrandCategory" LIKE %clinical% OR "BrandCategory" LIKE %indie% 
      #OR "BrandCategory" LIKE %kj beauty% OR "BrandCategory" LIKE %luxury%'
    else:
      brand_preference = " OR ".join(["{0} LIKE '%{1}%'".format('"BrandCategory"', w) for w in data.brand_preference])
  except:
    pass
  # Query to find set of similar users
  query = f"""SELECT * FROM "MasterData" 
            WHERE "SkinType" = '{data.skin_type}' 
            AND "Condition" IN {conditions} 
            AND "Characteristics" IN {characteristics} 
            AND "AcneSeverity" <= {data.pimples} 
            AND "Goals" IN {goals} 
            AND "Category" IN {routine} 
            AND "FullSizePrice" <= '{data.price}'
            AND "IsRecommended" = 'true' 
            AND ({personal_preference}) 
            AND ({brand_preference})
            ;"""
  
  print(query)
  filtered_df = pd.read_sql_query(query, connection)

  print(filtered_df['Category'].value_counts())
  print("\n")
  #print(filtered_df.columns)

  print(filtered_df.shape)

  df = recommend(filtered_df, connection)

  return df

if __name__ == "__main__":
    uvicorn.run("main:app", host = '127.0.0.1', port = 8001, reload = True, debug = True, workers = 1)
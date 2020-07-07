#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author: Biraj Parikh

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import defaultdict
import pandas as pd
import json

import psycopg2

def recommend(df, connection):
    
    # Removing rows where UserNickname is Null
    df = df[(df['UserNickname'].notna()) & (df['Name'].notna())]

    # Finding a set of unique users similar to the concerned user
    sim_users = str([x for x in df.UserNickname.unique()]).replace('[','(').replace(']',')')
    
    # Query to find Product IDs of the Similar User
    query = f"""SELECT DISTINCT("Product_ID") 
                FROM "CFRecSys" 
                WHERE "UserNickname" IN {sim_users}
                --ORDER BY "Rank";
            """
    # Execute the above query
    rec_df = pd.read_sql_query(query, connection)

    # Columns to display on the recommendations page
    cols = ['Product_ID', 'Name', 'Brand', 'Description', 'ImageUrl', 'ProductPageUrl', 'AverageOverallRating',
            'TotalReviewCount', 'PercentApproval', 'Category', 'FullSizePrice', 'TrialAvailable', 
            'TrialPrice', 'SkinType', 'BrandCategory', 'PreferenceTags', 'Ingredients', 'Blurb']

    # Getting a personalized recommendations dataframe
    personalized_df = pd.merge(left = rec_df, right = df[cols], how= 'left', on= 'Product_ID').\
                        sort_values('AverageOverallRating', ascending = False).drop_duplicates()

    personalized_df = personalized_df[personalized_df['Name'].notna()].reset_index(drop=True)

    # Gettings 3 reviews per product recommendations
    unique_ids = personalized_df.Product_ID.unique().tolist()
    df = df[df["Product_ID"].isin(unique_ids)].groupby(["Product_ID"]).head(3)[["Product_ID", "ReviewText"]].reset_index(drop = True)
    
    temp = dict([(key, []) for key in unique_ids])
    for key, row in df.iterrows():
        product_id = row["Product_ID"]
        temp.get(product_id).append(row["ReviewText"])

    DF = pd.DataFrame.from_dict(temp, orient='index', columns=['Review1', 'Review2', 'Review3'])\
            .reset_index().rename(columns={'index':'Product_ID'})
    
    personalized_df = pd.merge(left = personalized_df, right = DF, how= 'left', on= 'Product_ID').\
                        sort_values('AverageOverallRating', ascending = False).drop_duplicates()

    personalized_df[['Review1' ,'Review2', 'Review3']] = personalized_df[['Review1' ,'Review2', 'Review3']].astype(str)
    print(personalized_df.Category.value_counts())

    # Displaying the response on the API interface
    key_list = personalized_df.Category.unique().tolist()
    print(key_list)
    d = dict([(key, []) for key in key_list])

    # personalized_df.to_csv("personalized_recommendations.csv", index = False)
    for index, row in personalized_df.iterrows():
        Product_ID = row[0]
        Name = row[1]
        Brand = row[2]
        Description = row[3]
        ImageUrl = row[4]
        ProductPageUrl = row[5]
        AverageOverallRating = row[6]
        TotalReviewCount = row[7]
        PercentApproval = row[8]
        Category = row[9]
        FullSizePrice = row[10]
        TrialAvailable = row[11]
        TrialPrice = row[12]
        SkinType = row[13]
        BrandCategory = row[14]
        ProductTags = row[15]
        Ingredients = row[16]
        Blurb = row[17]
        R1 = row[18]
        R2 = row[19]
        R3 = row[20]
        
        if not Category in key_list:
            d[Category] = [{'Product_ID': Product_ID, 'ProductName':Name, 'Brand': Brand, 'ImageUrl': ImageUrl, 
                            'ProductPageUrl': ProductPageUrl, 'AverageOverallRating': str(AverageOverallRating),
                            'TotalReviewCount': str(TotalReviewCount), 'PercentApproval': str(PercentApproval), 
                            'FullSizePrice': str(FullSizePrice),
                            'Is_TrialAvailable': TrialAvailable, 'TrialPrice': str(TrialPrice), 'SkinType': SkinType,
                            'BrandCategory': BrandCategory, 'ProductTags': ProductTags, 'Description': Description,
                            'Ingredients': Ingredients, 'Blurb': Blurb, 'Review1': str(R1), 'Review2': str(R2), 'Review3': str(R3)}]
        # if parent IS a key in flare.json, add a new child to it
        else:
            d.get(Category).append({'Product_ID': Product_ID, 'ProductName':Name, 'Brand': Brand, 'ImageUrl': ImageUrl, 
                            'ProductPageUrl': ProductPageUrl, 'AverageOverallRating': str(AverageOverallRating),
                            'TotalReviewCount': str(TotalReviewCount), 'PercentApproval': str(PercentApproval), 
                            'FullSizePrice': str(FullSizePrice),
                            'Is_TrialAvailable': TrialAvailable, 'TrialPrice': str(TrialPrice), 'SkinType': SkinType,
                            'BrandCategory': BrandCategory, 'ProductTags': ProductTags, 'Description': Description,
                            'Ingredients': Ingredients, 'Blurb': Blurb, 'Review1': str(R1), 'Review2': str(R2), 'Review3': str(R3)})

    return d
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author: Biraj Parikh

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pandas as pd
import numpy as np

import os
import os.path

from CRUD import DatabaseConnection
from preprocessing import *

import psycopg2
import psycopg2.extras as extras
from config import config
params = config()

import warnings
warnings.filterwarnings("ignore")

from datetime import date
CurrentDate = date.today()


class masterData(DatabaseConnection):

    def __init__(self):
        super().__init__()
        
    def createMasterTable(self):
        """ create tables in the PostgreSQL database"""
        command = """ CREATE TABLE IF NOT EXISTS "MasterData" (
                        "Product_ID" TEXT NOT NULL,
                        "Name" TEXT,
                        "Brand" TEXT,
                        "Description" TEXT,
                        "ImageUrl" TEXT,
                        "ProductPageUrl" TEXT,
                        "AverageOverallRating" REAL,
                        "RecommendedCount" INTEGER,
                        "NotRecommendedCount" INTEGER,
                        "TotalReviewCount" INTEGER,
                        "PercentApproval" REAL,
                        "HelpfulVoteCount" INTEGER,
                        "NotHelpfulVoteCount" INTEGER,
                        "TagDistribution" TEXT, 
                        "SkinConcerns" TEXT,
                        "UserNickname" TEXT,
                        "Rating" REAL,
                        "IsRecommended" TEXT,
                        "ReviewText" TEXT,
                        "SkinType" TEXT,
                        "ReviewerSkinconcern" TEXT,
                        "SkinTone" TEXT,
                        "Age" TEXT,
                        "Condition" TEXT,
                        "Characteristics" TEXT,
                        "Goals" TEXT,
                        "AcneSeverity" INTEGER,
                        "Category" TEXT,
                        "ProductBrand" TEXT,
                        "FullSizePrice" TEXT,
                        "TrialAvailable" TEXT,
                        "TrialPrice" TEXT,
                        "BrandCategory" TEXT,
                        "PreferenceTags" TEXT,
                        "ProductTags" TEXT,
                        "Ingredients" TEXT,
                        "Blurb" TEXT,
                        "ProcessedDate" DATE
                        ); 
                  """
        try:
            self.cursor.execute(command)
            print("MasterData Table created successfully in PostgreSQL")
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while creating PostgreSQL table --> ", error)
    
    def dropMasterTable(self):

        try:
            drop_table_command = 'DROP TABLE ' + f'"MasterData"'
            self.cursor.execute(drop_table_command)
            print("Master table has been dropped")
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while droping master table --> ", error)

    def insertMasterRecords(self, df, page_size=1000):
        """
        Using psycopg2.extras.execute_batch() to insert the dataframe
        """
        tablename = "MasterData"
        df["ProcessedDate"] = CurrentDate
        # Create a list of tupples from the dataframe values
        tuples = [tuple(x) for x in df.to_numpy()]
        # Comma-separated dataframe columns
        cols = '","'.join(list(df.columns))
        # SQL quert to execute
        insert_query  =  "INSERT INTO " + f'"{tablename}"' + " ("+ '"' + cols + '"' + ") VALUES (" + "%s,"*(len(cols.split(','))-1) + "%s)"
        cursor = self.cursor
        try:
            #self.cursor.executemany(insert_query, tuples)
            extras.execute_batch(cursor, insert_query, tuples, page_size)
            print("Total", df.shape[0], "Records inserted successfully into review table")
        except (Exception, psycopg2.DatabaseError) as error:
            print ("\nFailed to insert the records --> ", error)

    def readReviewData(self, ProcessedDate=False):

        if ProcessedDate:
            df = pd.read_sql_query("""SELECT * FROM "Reviews" WHERE CAST("SubmissionTime" AS DATE) > '%s' """ % (ProcessedDate), self.connection)
            print("\nOnly records processed for date: ", CurrentDate, " shape: ", df.shape[0])
        else:
            df = self.query_all("Reviews")
            print("\nAll records were queried and the shape: ", df.shape[0])

        return df

    def readProductData(self):
        
        filepath = "./data/"

        
        cols = ['Category', 'Brand', 'Name', 'Full Size Price', 'Trial available? (Y/N)', 'If trial (Y), price', 
                'Brand Category (prestige, pharmacy, clinical, k+j beauty, indie)', 'Ingredients', 'Blurb', 
                'Preference Tags (Fragrance-free, Cruelty-free, Silicone/Paraben/Sulfate-free, Alcohol-free) + should add essential oil-free',
                'Product Tags (product type, base skin type, fungal acne, eczema or psoriasis, rosacea, PIH, PIE, dry patches, sensitive, very oily, uneven tone, mild acne, intermediate acne, severe acne, fade hyperpigmentation, brighten, oil control/pores, hydrate, soothe, clear blackheads, clear whiteheads, protect, fight acne, fragrance-free, cruelty-free']

        # Product database
        #df = pd.read_excel(filepath + 'product/' + 'product database.xlsx', sheet_name= "prod+tags+ingred", usecols = cols)
        df = pd.read_csv(filepath + 'product/' + 'product database.csv', usecols = cols)
        
        df = preprocess_product_db(df)

        return df

    def createMasterData(self, review_df):
        # Listing all the necessary columns
        cols = ['Product_ID', 'Name', 'Brand', 'Description', 'ImageUrl', 'ProductPageUrl', 'AverageOverallRating', 'RecommendedCount',
        'NotRecommendedCount', 'TotalReviewCount', 'PercentApproval', 'HelpfulVoteCount', 'NotHelpfulVoteCount', 'TagDistribution', 
        'SkinConcerns', 'UserNickname', 'Rating', 'IsRecommended', 'ReviewText', 'SkinType', 'ReviewerSkinconcern', 'SkinTone', 'Age']
        
        review_df = review_df[cols]
        review_df = preprocess_review_db(review_df)

        product_df = self.readProductData()

        df = pd.merge(left=review_df, right=product_df, how='left', on='Name')
        df.drop_duplicates(inplace = True)
        print("\nInserting the merged records into the MasterData Table....")
        self.insertMasterRecords(df)

    def main(self, ProcessedDate=False):
        if ProcessedDate:
            review_df = self.readReviewData(ProcessedDate)
            if review_df.shape[0] != 0:
                self.createMasterData(review_df)
            else:
                print("\n MasterData is already upto date")
                sys.exit()
        else:
            review_df = self.readReviewData()
            self.createMasterData(review_df)
            

if __name__ == "__main__":

    m = masterData()

    m.createMasterTable()

    connection = psycopg2.connect(**params)
    connection.autocommit = True
    ProcessedDate = pd.read_sql_query('SELECT MAX("ProcessedDate") FROM "MasterData"', connection).values[0][0]
    if ProcessedDate:
        m.main(ProcessedDate)
    else:
        m.main()

    #m.createMasterTable()
    #m.dropMasterTable()
    
    
"""
-- SIMILAR TO '%(cruelty-free|clean skincare|fragrance-free)%';


-- LIKE any(array['%cruelty-free%','%clean skincare%','%fragrance-free%']);

-- like any(array['%Khairpur%','%clean skincare%','%Karachi%']);

WHERE (Product_Tags LIKE '%cruelty-free%' OR
       name LIKE '%fragrance-free%' OR
       name LIKE '%clean skincare%')

"""
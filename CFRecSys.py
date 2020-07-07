#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author: Biraj Parikh

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pandas as pd
import numpy as np

import psycopg2
import psycopg2.extras as extras

from sklearn.decomposition import TruncatedSVD
import scipy.sparse
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds

import copy

from CRUD import DatabaseConnection

"""
Recommend products to users based on purchase history and similarity of ratings provided by other users who bought items to 
that of a particular customer.

A model based collaborative filtering technique is chosen here as it helps in making predicting unrated products for a 
particular user by identifying patterns based on preferences from multiple user data.

Utility Matrix based on products sold and user reviews

An utlity matrix is consists of all possible user-product preferences (ratings) details represented as a matrix. The utility matrix is 
sparce as none of the users would buy all the items in the list, hence, most of the values are unknown.
"""

class CFRecSys(DatabaseConnection):

    def __init__(self, no_of_recommendations):
        super().__init__()
        self.n = no_of_recommendations

    def createRecSysTable(self):
        """ create tables in the PostgreSQL database"""
        command = """ CREATE TABLE IF NOT EXISTS "CFRecSys" (
                        "UserNickname" TEXT,
                        "Rank" INTEGER,
                        "Product_ID" TEXT
                        ); 
                  """
        try:
            self.cursor.execute(command)
            print("CFRecSys Table created successfully in PostgreSQL")
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while creating PostgreSQL table --> ", error)

    def dropRecSysTable(self):
        try:
            drop_table_command = 'DROP TABLE "CFRecSys"'
            self.cursor.execute(drop_table_command)
            print("CFRecSys table has been dropped")
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while droping master table --> ", error)

    def insertPredictedRatings(self, df, page_size=5000):
        """
        Using psycopg2.extras.execute_batch() to insert the dataframe
        """
        # Create a list of tupples from the dataframe values
        tuples = [tuple(x) for x in df.to_numpy()]
        # Comma-separated dataframe columns
        cols = '","'.join(list(df.columns))
        # SQL quert to execute
        tablename = '"CFRecSys"'
        insert_query =  "INSERT INTO " + tablename + " ("+'"' + cols + '"'+ ") \
                          VALUES (" + "%s,"*(len(cols.split(','))-1) + "%s)"
        cursor = self.cursor
        try:
            #self.cursor.executemany(insert_query, tuples)
            self.cursor.execute("Truncate " + tablename + ";") 
            extras.execute_batch(cursor, insert_query, tuples, page_size)
            print("Total", df.shape[0], "Records inserted successfully into review table")
        except (Exception, psycopg2.DatabaseError) as error:
            print ("\nFailed to insert the records --> ", error)

    def createUtilityMatrix(self, df_rating):
        """ Function to create a utility matrix """
        # pivoting the data with the ratings values
        utility_matrix = df_rating.pivot_table(values='Rating', index='UserNickname', 
                                               columns='Product_ID').fillna(0.0)
        return utility_matrix

    def estimatePredictedRatings(self, utility_matrix):
    
        """ Function to perform SVD and get predicted ratings for unrated products """
        
        # Perform SVD
        # here k = latent factors
        U, sigma, Vt = svds(utility_matrix, k = 10)
        
        # Predicted ratings
        all_user_predicted_ratings = np.dot(np.dot(U, np.diag(sigma)), Vt) 
        
        # Convert predicted ratings to dataframe
        preds_df = pd.DataFrame(all_user_predicted_ratings, columns = utility_matrix.columns)
        
        return preds_df

    def precomputeRecsys(self):
    
        """ Function to get recommendations for the concerned user
        Args:
            users - list: set of similar users
            n - int: Number of recommendations to give
        """

        # Number of recommendations
        n = self.n
    
        # Reading the master data from the database
        df_rating = pd.read_sql_query('SELECT * FROM "MasterData"', self.connection)
        
        # Utility Matrix
        ratings_utility_matrix = self.createUtilityMatrix(df_rating)
        print("\nThe Utility matrix completed.")
        
        # Creating a copy of the ratings_utility_matrix just to get the index of the user
        pivot_df = copy.deepcopy(ratings_utility_matrix).reset_index()
        
        # Get predicted ratings
        preds_df = self.estimatePredictedRatings(ratings_utility_matrix)
        print("\nSVD has been computed.")

        # Create a placeholder items for closes neighbours to an item
        data_neighbours = pd.DataFrame(index = ratings_utility_matrix.index, columns = range(1,n+1))
        
        # Loop through our similarity dataframe and fill in neighbouring item names
        for i in range(0, data_neighbours.shape[0]):
            data_neighbours.iloc[i, :n] = preds_df.iloc[i,:].sort_values(ascending=False)[:n].index
        
        # wide to long format and renaming the column names
        pre_compute_reco_df = pd.melt(data_neighbours.reset_index(), id_vars=['UserNickname'])\
        .rename(columns = {'variable': 'Rank', 'value': 'Product_ID'})
        
        # Saving to the RecSys database
        #pre_compute_reco_df.to_sql('precomputed_recommendations', output_database, if_exists='replace', index = False)
        print("\nInserting the recommendations into the table .....")
        self.insertPredictedRatings(pre_compute_reco_df)
        #print("\nPredicted Ratings has been inserted successfully.")
        return pre_compute_reco_df
    
if __name__ == "__main__":
    
    print("\nEnter the desired number of recommendations:")
    n = int(input())
    
    recsys = CFRecSys(n)
    recsys.createRecSysTable()
    # recsys.dropRecSysTable()
    recsys.precomputeRecsys()
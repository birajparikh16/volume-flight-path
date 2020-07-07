#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author: Biraj Parikh

"""
This scripts does the following:
    1. Create a review and product_id table.
    2. Insert product ids to the product_id table.
    3. Update product_id table once the reviews are scrapped.
    4. Add new product ids to the product_id table.
    5. Drop table functionality
    6. Delete records from the product_id table functionality.
"""

import os
import pandas as pd
import numpy as np

import psycopg2
from pprint import pprint

from config import config
params = config()

class DatabaseConnection:
    
    def __init__(self):
        """ Create a connection to the database"""
        try:
            # Importing all the parameters from the config file
            self.connection = psycopg2.connect(**params)
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            pprint("Cannot connect to database --> ", error)

    def os_dir_search(self, filename):
        """ This method returns the root directory of the given filename"""
    
        for root,dirs,files in os.walk(os.getcwd()):
            for file in files:
                file = str(file)
                if file == filename:
                    filepath = r'{}\{}'.format(root, file)
                    break
        return filepath

    def create_table(self):
        """ create tables in the PostgreSQL database"""
        # Create table query string
        commands = (
            #Create table review - This table will host all the reviews scrapped.
            """
            CREATE TABLE IF NOT EXISTS "Reviews" (
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
                    "Avatar" TEXT,
                    "ReviewText" TEXT,
                    "SkinType" TEXT,
                    "EyeColor" TEXT,
                    "ReviewerSkinconcern" TEXT,
                    "HairColor" TEXT,
                    "SkinTone" TEXT,
                    "Age" TEXT,
                    "SubmissionTime" DATE); 
            """,
            #Create table ProductIDs
            """ 
            CREATE TABLE IF NOT EXISTS "ProductIDs" (
                    "Product_ID" TEXT UNIQUE NOT NULL,
                    "LastProcessedDate" DATE);
            """
        )
        try:
            # create table one by one
            for command in commands:
                self.cursor.execute(command)
            print("Tables created successfully in PostgreSQL")
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while creating PostgreSQL table --> ", error)

    def insert_records(self, filename, tablename):
        """ This function copy product ids csv file to the ProductIDs table"""
        try:
            # find the path for the product id csv file
            csv_file = self.os_dir_search(filename)
            sql = "COPY %s FROM STDIN WITH CSV HEADER DELIMITER AS ','"
            file = open(csv_file, "r")
            tablename = f'"{tablename}"'
            #avoiding uploading duplicate data!
            self.cursor.execute("Truncate " + tablename + ";")  
            self.cursor.copy_expert(sql=sql % tablename, file=file)
            print("Records successfully inserted into the table {}".format(tablename))
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while inserting in the table {} --> ".format(tablename), error)

    def query_all(self, tablename):
        """ This function returns all the columns of the given table """
        tablename = f'"{tablename}"'
        df = pd.read_sql_query('SELECT * FROM ' + tablename, self.connection)
        return df

    def insert_new_prodids(self):
        """ Function to add new product ids to the ProductIDs table. """
        try:
            # Reading the existing product ids
            existing_ids = self.query_all("ProductIDs")['Product_ID'].values

            # Reading new product ids
            new_id_list = pd.read_csv(self.os_dir_search("new_product_ids.csv"), skiprows = True, \
                                  names=["Product_ID"]).values

            # Insert query for updating the ProductIDs table with new product ids
            insert_query  = """INSERT INTO "ProductIDs" ("Product_ID")
                               VALUES(%s);"""

            # Finding the new ids
            diff_ids = new_id_list[~np.isin(new_id_list, existing_ids)]

            # Insert each new product ids
            for ids in diff_ids:
                record_to_insert = (ids,)
                self.cursor.execute(insert_query, record_to_insert)
            print("\nNew {} product ids have been added to the ProductIDs table.".format(len(diff_ids)))
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while inserting new product_ids --> ", error)

    def drop_table(self, tablename):
        """ Drops the given table """
        try:
            drop_table_command = "DROP TABLE " + f'"{tablename}"' 
            self.cursor.execute(drop_table_command)
            print("\nTable {} has been dropped".format(tablename))
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while droping table {} --> ".format(tablename), error)

    def delete_records(self, tablename, product_id):
        """ Delete records from the ProductIDs table for a given product id
        Args:
            tablename
            product_id
        """
        try:
            delete_sql = 'DELETE FROM ' + f'"{tablename}"' + ' WHERE "Product_ID" = %s;'
            self.cursor.execute(delete_sql, (product_id,))
            print("\nRecords has been dropped from the table {}".format(tablename))
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while deleting records --> ", error)

if __name__== '__main__':
    database_connection = DatabaseConnection()
    database_connection.create_table()
    database_connection.insert_records("sephora_product_ids.csv", "ProductIDs")
    #database_connection.update_prod_id_table('2020-07-22', 'P447597')
    #database_connection.drop_table("ProductIDs")
    #database_connection.delete_records("ProductIDs", "P447597")
    #database_connection.insert_new_prodids()
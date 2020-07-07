#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author: Biraj Parikh

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import psycopg2
import pandas as pd

import requests
from datetime import datetime
import json

# Import the 'config' funtion from the config.py file
from config import config

from CRUD import DatabaseConnection

class scrapeSephora(DatabaseConnection):
    
    def __init__(self):
        # Inhereting all the methods and attributes from the DatabaseConnection class
        super().__init__()
        
    def insertScrapeRecords(self, recordList):
    
        try:
            insert_query = """
                            INSERT INTO "Reviews"
                            ("Product_ID", "Name", "Brand", "Description", "ImageUrl", "ProductPageUrl", "AverageOverallRating", "RecommendedCount", 
                            "NotRecommendedCount", "TotalReviewCount", "PercentApproval", "HelpfulVoteCount", "NotHelpfulVoteCount", "TagDistribution", "SkinConcerns", "UserNickname", 
                            "Rating", "IsRecommended", "Avatar", "ReviewText", "SkinType", "EyeColor", "ReviewerSkinconcern", "HairColor", "SkinTone", "Age", "SubmissionTime") 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                            """
            self.cursor.executemany(insert_query, recordList)
            print("Total", self.cursor.rowcount, "Records inserted successfully into review table")
        except (Exception, psycopg2.DatabaseError) as error:
            print ("\nFailed to update PostgreSQL table --> ", error)

    def updateProdIDTable(self, lastprocesseddate, product_id):
        """ Updates the ProductIDs table once the reviews are scrapped for a particular product id"""
        try:
            update_command = """ UPDATE "ProductIDs"
                                 SET "LastProcessedDate" = %s
                                 WHERE "Product_ID" = %s"""
            self.cursor.execute(update_command, (lastprocesseddate, product_id))
            print("\nProductIDs table have been updated for the product id: {0} with date: {1}".format(product_id, lastprocesseddate))
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while updating PostgreSQL ProductIDs table --> ", error)
            
    def fetchReviews(self, product_id, total_reviews, LastProcessedDate):

        limit = 100
        start = 0
        stop = total_reviews + 100
        #numelements = int((stop-start)/float(limit))
        flags = 0
        
        output = []
        
        for i in range(start, stop, limit):

            offset = i
            print("Offset: ", offset)

            url = f'https://api.bazaarvoice.com/data/reviews.json?Filter=contentlocale%3Aen*&Filter=ProductId%3A{product_id}&Sort=SubmissionTime%3Adesc&Limit={limit}&Offset={offset}&Include=Products%2CComments&Stats=Reviews&passkey=rwbw526r2e7spptqd2qzbkp7&apiversion=5.4&Locale=en_US'
            review = requests.get(url).json()
            if len(review['Includes']) != 0:
                try:
                    lookup = review['Includes']['Products'][product_id]

                    Name = lookup['Name']
                    Brand = lookup['Brand']['Name']
                    Description = lookup['Description']
                    ImageUrl = lookup['ImageUrl']
                    ProductPageUrl = lookup['ProductPageUrl']
                    AverageOverallRating = lookup['ReviewStatistics']['AverageOverallRating']

                    RecommendedCount = lookup['ReviewStatistics']['RecommendedCount']
                    NotRecommendedCount = lookup['ReviewStatistics']['NotRecommendedCount']
                    TotalReviewCount = lookup['ReviewStatistics']['TotalReviewCount']
                    PercentApproval = round((RecommendedCount / TotalReviewCount) * 100, 2)

                    HelpfulVoteCount = lookup['ReviewStatistics']['HelpfulVoteCount']
                    NotHelpfulVoteCount = lookup['ReviewStatistics']['NotHelpfulVoteCount']
                    
                    try:
                        TagDistribution = lookup['ReviewStatistics']['TagDistribution']
                        TagDistribution = ','.join([x['Value'] for x in (TagDistribution['Pro']['Values'])])
                    except:
                        TagDistribution = ''
                        
                    try:
                        SkinConcerns = lookup['ReviewStatistics']['skinConcerns']
                        SkinConcerns = ','.join([x['Value'] for x in (skinConcerns['Pro']['Values'])])
                    except:
                        SkinConcerns = ''

                    results = review['Results']

                    for result in results:

                        CurrentSubmissionDate = datetime.strptime(result['SubmissionTime'].split("T")[0], '%Y-%m-%d').date()

                        if CurrentSubmissionDate > LastProcessedDate:
                            try:
                                UserNickname = result['UserNickname']
                            except:
                                UserNickname = ''
                            try: 
                                Rating = result['Rating']
                            except:
                                Rating = ''
                            try:
                                IsRecommended = result['IsRecommended']
                            except:
                                IsRecommended = ''
                            try:                   
                                Avatar = result['AdditionalFields']['sociallockup']['Value'].replace('avatar=', '')
                            except:
                                Avatar = ''
                            try:
                                ReviewText = result['ReviewText']
                            except:
                                ReviewText = ''
                            try:
                                SkinType = result['ContextDataValues']['skinType']['ValueLabel']
                            except:
                                SkinType = ''
                            try:
                                EyeColor = result['ContextDataValues']['eyeColor']['ValueLabel']
                            except:
                                EyeColor = ''             
                            try:
                                ReviewerSkinconcern = result['ContextDataValues']['skinConcerns']['ValueLabel']
                            except:
                                ReviewerSkinconcern = ''
                            try:
                                HairColor = result['ContextDataValues']['hairColor']['ValueLabel']
                            except:
                                HairColor = ''
                            try:
                                SkinTone = result['ContextDataValues']['skinTone']['ValueLabel']
                            except:
                                SkinTone = ''
                            try:
                                Age = result['ContextDataValues']['age']['ValueLabel']
                            except:
                                Age = ''

                            SubmissionTime = datetime.strptime(result['SubmissionTime'].split("T")[0], '%Y-%m-%d').date()


                            output.append((product_id, Name, Brand, Description, ImageUrl, ProductPageUrl, AverageOverallRating, RecommendedCount, 
                                           NotRecommendedCount, TotalReviewCount, PercentApproval, HelpfulVoteCount, NotHelpfulVoteCount, 
                                           TagDistribution, SkinConcerns, UserNickname, Rating, IsRecommended, Avatar, ReviewText, SkinType, EyeColor,
                                           ReviewerSkinconcern, HairColor, SkinTone, Age, SubmissionTime))    
                        else:
                            flags = 1
                            break
                    if flags == 1:
                        print("No more reviews for the product id: ", product_id)
                        break
                except KeyError:
                    print("Product ID does not match for offset: ", offset, " for product id: ", product_id)
            else:
                break 

        return output


    def scrape(self):

        limit = 1
        offset = 0
        # Reading the product_id table
        prod_id_df = self.query_all("ProductIDs")
        
        for idx, row in prod_id_df.iterrows():

            product_id = row['Product_ID']
            LastProcessedDate = row['LastProcessedDate']
            
            print('-'*75)

            print("\nAPI Request for Product ID: ", product_id)
            
            print("\nLastProcessedDate from csv: ", LastProcessedDate)

            # URL for requesting api
            url = f'https://api.bazaarvoice.com/data/reviews.json?Filter=contentlocale%3Aen*&Filter=ProductId%3A{product_id}&Sort=SubmissionTime%3Adesc&Limit={limit}&Offset={offset}&Include=Products%2CComments&Stats=Reviews&passkey=rwbw526r2e7spptqd2qzbkp7&apiversion=5.4&Locale=en_US'
            # api response
            review = requests.get(url).json()
            if len(review['Includes']) != 0:
                try:
                    lookup = review['Includes']['Products'][product_id]

                    # If Null
                    if not LastProcessedDate:
                        LastProcessedDate = datetime.strptime(lookup['ReviewStatistics']['FirstSubmissionTime'].split("T")[0], '%Y-%m-%d').date()
                    else:
                        LastProcessedDate = datetime.strptime(str(LastProcessedDate), '%Y-%m-%d').date()

                    print("LastProcessedDate: ", LastProcessedDate)

                    # Reading LastSubmissionTime and converting to date object
                    CurrentSubmissionDate = datetime.strptime(lookup['ReviewStatistics']['LastSubmissionTime'].split("T")[0], '%Y-%m-%d').date()
                    print("CurrentSubmissionDate: ", CurrentSubmissionDate)

                    # If Current submission is greater than LastProcessedDate then only fetch reviews
                    if CurrentSubmissionDate > LastProcessedDate:
                        # Get Total Reviews
                        total_reviews = review['TotalResults']
                        print("\nThe total number of reviews to be fetched: ", total_reviews)
                        # Get reviews 
                        all_reviews = self.fetchReviews(product_id, total_reviews, LastProcessedDate)
                        print("\nNumber of reviews fetched for Product ID ", product_id, "is :", len(all_reviews))
                        # Insert the scrape records
                        self.insertScrapeRecords(all_reviews)
                        # Updating the product id Table
                        self.updateProdIDTable(CurrentSubmissionDate, product_id)
                    else:
                        print("\nProduct_ID Table upto date for product id: ", product_id)
                except KeyError:
                    print("Product ID does not match for product_id: ", product_id)
            else:
                pass

        updated_prod_id = self.query_all("ProductIDs")
        updated_prod_id.to_csv("./data/sephora_product_ids.csv", index = False)

if __name__== '__main__':
    sc = scrapeSephora()
    sc.scrape()
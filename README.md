# recommender_system
This repository has all the codes and files for recommender system.

**The Pipeline Layer**

1. database.ini - This file will contain the credentials to the database
2. config.py - This script reads in the database.ini file and returns the connection parameters as a dictionary.
3. preprocessing.py - This script does all the preprocessing of the review text.
4. CRUD.py - This script does the CRUD operation. It creates the Reviews and ProductIDs table.
5. scrapeSephora.py - This script scrapes the sephora product reviews for a given product ids in the ProductIDs table and finally insert the records in the Reviews table.
6. master_data.py - This script creates a structured (master) data upon which filtering can be applied based on the consultation questions and inserts the cleaned/structured records on the MasterData table.
7. CFRecSys.py - This script perform the SVD computation for the recommender system and inserts the records in the CFRecSys table.

**API Layer**

1. main.py - This script is the app for the API layer which accepts the consultation questions as request and applies the filtering on the MasterData table to get a set of similar users.
2. personalized_recsys.py - This script customizes the response to be sent via API.
# Volume Python Take-Home Test
This repository has all the codes and files for recommender system.

**Task** 

Story: There are over 100,000 flights a day, with millions of people and cargo being transferred around the world. With so many people, and different carrier/agency groups it can be hard to track where a person might be. In order to determine the flight path of a person, we must sort through all of their flight records.

Goal: To create a microservice API that can help us understand and track how a particular person’s flight path may be queried. The API should accept a request that includes a list of flights, which are defined by a source and destination airport code. These flights may not be listed in order and will need to be sorted to find the total flight paths starting and ending airports.

Examples:

[['SFO', 'EWR']]                                                    => ['SFO', 'EWR']\n
[['ATL', 'EWR'], ['SFO', 'ATL']]                                    => ['SFO', 'EWR']
[['IND', 'EWR'], ['SFO', 'ATL'], ['GSO', 'IND'], ['ATL', 'GSO']]    => ['SFO', 'EWR']


**API Layer**

1. main.py - This script is the app for the API layer which accepts the consultation questions as request and applies the filtering on the MasterData table to get a set of similar users.
2. personalized_recsys.py - This script customizes the response to be sent via API.

#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author: Biraj Parikh

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import AnyStr, List, Tuple, Any

# Initializing an api
app = FastAPI()

# Defining a class to accept the flight paths
class Flight(BaseModel):
    routes: List[List[AnyStr]]

# Index route
@app.get("/")
def root():
  return {"Volume": "Python Take-Home Test"}

# Find Source and Destination of the routes
def findflightPath(routes: List[List]):
    """
    Args:
        Accept flight routes as a list of list strings
        example: ["ATL", "EWR"], ["SFO", "ATL"]
    Return:
        List: [source, destination]
    
    """
    source = []
    destination = []
    source_airport = ""
    destination_airport = ""
    # append all the source and destination in the respective list
    for i in range(len(routes)):
        source.append(routes[i][0])
        destination.append((routes[i][1]))

    for src in source:
        # If source found in destination list than remove the source from the destination list because
        # source cannot be same as destination
        if src in destination:
            destination.remove(src)
            continue
        else:
            source_airport += str(src,'utf-8')
    # the last remaining value in the destination list would be our destination
    destination_airport += str(destination[-1],'utf-8')
    return [source_airport, destination_airport]

@app.post("/flight-path")
def flight_path(flight_path_routes: Flight):
  routes = flight_path_routes.dict()['routes']
  return findflightPath(routes)

# if __name__ == "__main__":
#     uvicorn.run("main:app", host = '127.0.0.1', port = 5000, reload = True)
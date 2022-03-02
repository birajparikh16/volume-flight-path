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

from flight_path_algo import findflightPath

# Initializing an api
app = FastAPI()

# Defining a class to accept the flight paths
class Flight(BaseModel):
    routes: List[List[AnyStr]]

# Index route
@app.get("/")
def root():
  return {"Volume": "Python Take-Home Test"}

@app.post("/flight-path")
def flight_path(flight_path_routes: Flight):
  routes = flight_path_routes.dict()['routes']
  return findflightPath(routes)

# if __name__ == "__main__":
#     uvicorn.run("main:app", host = '127.0.0.1', port = 5000, reload = True)
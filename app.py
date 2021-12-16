import datetime as dt
import numpy as np
import pandas as pd

# dependencies for SQLAlchemy (will help us access our data in the SQLite database)
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# With this code, you will be able to access the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

# create a Flask application called "app"
# all outes should go after this
app = Flask(__name__)

# ROUTE: WELCOME
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# ROUTE: PRECIPITATION
# create a dictionary with the date as the key and the precipitation as the value
# Jsonify() is a function that converts the dictionary to a JSON file
# \used to signify that we want our query to continue on the next line
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# ROUTE: STATIONS
# get all of the stations in our database
# unravel results into a one-dimensional array. Use function np.ravel(), with results as parameter
# This formats our list into JSON (last line)
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# ROUTE: TEMPERATURE OBSERVATIONS
# calculate the date one year ago from the last date in the database
# query the primary station for all the temperature observations
# unravel results into a one-dimensional array and convert that array into a list
# jsonify the temps list and then return it
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# ROUTE: SUMMARY STATISTICS
# add a start parameter and an end parameter to stats() function
# create a query to select the minimum, average, and maximum temperatures from our SQLite database
# add an if-not statement to our code:
#    query our database using the list just made
#    unravel the results into a one-dimensional array
#    convert them to a list
#    jsonify results and return them
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
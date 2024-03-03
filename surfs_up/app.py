# Import the dependencies.

import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources///hawaii.sqlite")


# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and'
measurement = Base.classes.measurement

# the station class to a variable called `Station`
station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
    )


# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Query all precipitation dates
    precipitation_results = session.query(measurement.date,measurement.prcp).filter(measurement.date >= last_year).all()

    session.close()

    # Convert list of tuples into normal list
    precipitation_dict = {date: prcp for date, prcp in precipitation_results}

    return jsonify(precipitation_dict)


# Stations Route

@app.route("/api/v1.0/stations")
def stations():
    

    # Query all precipitation dates
    stations_results = session.query(station.station,station.name).all()

    session.close()

    return jsonify(stations_results)


# Tobs Route

@app.route("/api/v1.0/tobs")
def tobs():
    
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Query all precipitation dates
    tobs_results = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= last_year).all()

    session.close()

    # Convert list of tuples into normal list
    tobs_dict = {date: tobs for date, tobs in tobs_results}

    return jsonify(tobs_dict)

#Start
@app.route("/api/v1.0/temp/start")
def start():
    start_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    start = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date >= start_date).all()
    session.close()
    return jsonify(start)



#Start/end
@app.route("/api/v1.0/temp/start/end")
def startend():   
    end_date = dt.date(2017,8,23)
    startend = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date is end_date).all()
    session.close()
    return jsonify(startend)   


if __name__ == '__main__':
    app.run(debug=True)



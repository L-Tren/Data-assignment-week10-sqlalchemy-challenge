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
engine = create_engine("sqlite:///hawaii.sqlite")


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
    
    # Create our session (link) from Python to the DB
    # session = precipitation(engine)

    # Query all precipitation dates
    precipitation_results = session.query(measurement.date,measurement.precipitation).filter(measurement.date >= last_year)

    session.close()

    # Convert list of tuples into normal list
    precipitation_dict = dict({date},{precipitation})

    return jsonify(precipitation_dict)

if __name__ == '__main__':
    app.run(debug=True)


# Stations Route



# Tobs Route


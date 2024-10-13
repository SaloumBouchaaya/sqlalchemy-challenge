# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify



#################################################
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#################################################


# reflect an existing database into a new model
Base=automap_base()
# reflect the tables
Base.prepare(engine,reflect=True)

# Save references to each table
Station=Base.classes.station
Measurement=Base.classes.measurement

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
climate_app= Flask(__name__)
#################################################




#################################################
# Flask Routes

@app.route("/")

#################################################

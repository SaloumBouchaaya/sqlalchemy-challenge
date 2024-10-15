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
#rout to home page containing all routes created
@climate_app.route("/")
def home():
    """List all available routes."""
    return jsonify({
        "Available Routes": [
            "/api/v1.0/stations",
            "/api/v1.0/measurements",
            "/api/v1.0/precipitation",
            "/api/v1.0/tobs",
            "/api/v1.0/<start>",
            "/api/v1.0/<start>/<end>"]})

#route to precipitation data for the most recent year. 
@climate_app.route("/api/v1.0/precipitation")
def precipitation():
    """Return precipitation data for the last 12 months."""
    most_recent_date_subquery = session.query(func.max(Measurement.date)).scalar() #pulled most recent date from data page
    prcp_scores = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date >= func.date(most_recent_date_subquery, '-12 months')
    ).all()
#create a dictionary for precipitation data and return it in JSON
    precipitation_dict = {date: prcp for date, prcp in prcp_scores}
    return jsonify(precipitation_dict)

#route to list of all stations
#create list and return as JSON
@climate_app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    results = session.query(Station.station, Station.name).all()
    stations_list = [{"station_id": station, "name": name} for station, name in results]
    return jsonify(stations_list)

#route to temperature observations for previous year
@climate_app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the previous year."""
    most_recent_date_subquery = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.strptime(most_recent_date_subquery, '%Y-%m-%d') #pulled data from climate_starter.ipynb
    one_year = most_recent_date.replace(year=most_recent_date.year - 1)
    #grouped stations and placed in descending order
    most_active_station_id = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).\
        first()[0]
    #query tobs data from measurment class and return in JSON
    tobs_data = session.query(Measurement.tobs).filter(
        Measurement.station == most_active_station_id,
        Measurement.date >= one_year
    ).all()
    tobs_list = [tobs[0] for tobs in tobs_data]
    return jsonify(tobs_list)

@climate_app.route('/api/v1.0/<start>')
def get_temperature_start(start):
    session = Session(bind=engine) #join two classes
#get data stats
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close() #close session
    temperature_data = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]}
    return jsonify(temperature_data) #return data in JSON

@climate_app.route('/api/v1.0/<start>/<end>')
def get_temperature_start_end(start, end):
    session = Session(bind=engine) #close session
#get data stats
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
#format how to display data
    temperature_data = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]}
    return jsonify(temperature_data) #return data in JSON



if __name__ == "__main__":
    climate_app.run(debug=True)


#################################################

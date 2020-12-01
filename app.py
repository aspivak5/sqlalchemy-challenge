import numpy as np
import datetime as dt
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

#sqlalchemy
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect = True)
Measurement = Base.classes.measurement 
Station = Base.classes.station




year_ago = dt.date(2017,8,23) - dt.timedelta(days =365)
print(year_ago)

#flask
app = Flask(__name__)

@app.route("/")
def welcome():
    return(
        f"Welcome! Here are the available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>(enter date as YYYY-MM-DD)<br/>"
        f"/api/v1.0/<start>/<end>(enter start and end date as YYYY-MM-DD/YYYY-MM-DD)"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    print(last_date)
    results = session.query(Measurement.date,Measurement.prcp).filter(func.strftime('%Y-%m-%d',Measurement.date) >= year_ago).order_by(Measurement.date).all()
    session.close()
    all_precipitation = []
    for date,prcp in results:
        prcp_dict = {}
        prcp_dict["date"]= date
        prcp_dict["prcp"] = prcp
        all_precipitation.append(prcp_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session =Session(engine)
    results = session.query(Station.id,Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).order_by(Station.id).all()
    session.close()
    all_stations = []
    for id,station,name,latitude,longitude,elevation in results:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)
    return jsonify (all_stations)


if __name__ == "__main__":
    app.run(debug=True)
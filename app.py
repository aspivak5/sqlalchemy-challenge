import numpy as np
import datetime as dt
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
# print(year_ago)

#flask
app = Flask(__name__)

#set up home route
@app.route("/")
def welcome():
    return(
        "Welcome! Here are the available routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/<start>(enter date as YYYY-MM-DD)<br/>"
        "/api/v1.0/<start>/<end>(enter start and end date as YYYY-MM-DD/YYYY-MM-DD)"
    )
#setup precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    print(last_date)
    results = session.query(Measurement.date,Measurement.prcp).filter(func.strftime('%Y-%m-%d',Measurement.date) >= year_ago).order_by(Measurement.date).all()
    session.close()
    prcp_list = []
    for date,prcp in results:
        prcp_dict = {}
        prcp_dict["date"]= date
        prcp_dict["precipitation(inches)"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

#setup stations route
@app.route("/api/v1.0/stations")
def stations():
    session =Session(engine)
    results = session.query(Station.id,Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).order_by(Station.id).all()
    session.close()
    stations_list = []
    for id,station,name,latitude,longitude,elevation in results:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        stations_list.append(station_dict)
    return jsonify (stations_list)

#setup tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    active_stations = session.query(Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    print(active_stations)
    results = session.query(Measurement.station,Measurement.date,Measurement.tobs).filter(Measurement.station =="USC00519281").filter(func.strftime('%Y-%m-%d',Measurement.date) >= year_ago).order_by(Measurement.date).all()
    session.close()
    active_station_list = []
    for station,date,tobs in results:
        active_station_dict = {}
        active_station_dict["station"] = station
        active_station_dict["date"] = date
        active_station_dict["tobs"]= tobs
        active_station_list.append(active_station_dict)
    return jsonify(active_station_list)

#setup start date route for selected date
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    start_date = session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).order_by(Measurement.date).all()
    session.close()
    start_date_list = []
    for date,min_temp,max_temp,avg_temp in start_date:
        start_date_dict = {}
        start_date_dict["Date"] = date
        start_date_dict["Min_temp"] = min_temp
        start_date_dict["Max_temp"] = max_temp
        start_date_dict["Avg_temp"] = round(avg_temp,2)
        start_date_list.append(start_date_dict)
    return jsonify(start_date_list)

#setup start and end date route for selected dates
@app.route("/api/v1.0/<start>/<end>")
def start_end_dates(start,end):
    session = Session(engine)
    start_end_dates = session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).order_by(Measurement.date).all()
    session.close()
    start_end_date_list = []
    for date,min_temp,max_temp,avg_temp in start_end_dates:
        start_end_date_dict = {}
        start_end_date_dict["Date"] = date
        start_end_date_dict["Min_temp"] = min_temp
        start_end_date_dict["Max_temp"] = max_temp
        start_end_date_dict["Avg_temp"] = round(avg_temp,2)
        start_end_date_list.append(start_end_date_dict)
    return jsonify(start_end_date_list)


if __name__ == "__main__":
    app.run(debug=True)

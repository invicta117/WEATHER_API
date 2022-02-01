import sqlalchemy.exc
from flask import Flask, jsonify
from flask import request
from flask import Response
from sqlalchemy import create_engine
import pymysql
app = Flask(__name__)

DB_USER = "root"
DB_PASS = "root"
DB_URL = "database:3306"

class MalformedRequestError(Exception):
    pass

class ExistingValueError(Exception):
    pass

def sql_query(query):
    data = []
    engine = create_engine("mysql+pymysql://{0}:{1}@{2}/weathersensors".format(DB_USER, DB_PASS, DB_URL), echo=True)
    connection = engine.connect()
    rows = engine.execute(query)
    connection.close()
    engine.dispose()
    for row in rows:
        data.append(dict(row))  # inset dict of data into list
        print(row)
    print(data)
    return data

def insert_sql_query(query):
    engine = create_engine("mysql+pymysql://{0}:{1}@{2}/weathersensors".format(DB_USER, DB_PASS, DB_URL), echo=True)
    connection = engine.connect()
    try:
        engine.execute(query)
    except sqlalchemy.exc.IntegrityError as e:
        raise ExistingValueError
    connection.close()
    engine.dispose()
    return

def create_query(request_data, sensor):
    date = request_data.get("date")
    metrics = request_data["metrics"]
    if isinstance(metrics, str):
        metrics = [metrics]
    query = "select "
    if date == None:
        query += "max(date) as datetime, "
    for m in range(len(metrics)):
        if m == len(metrics) - 1:
            query += "avg(" + metrics[m] + ") as " + metrics[m] + " "
        else:
            query += "avg(" + metrics[m] + ") as "+ metrics[m] + ", "
    query += "from weather "
    if date != None:
        query += "where date >= '" + date[0] + "' and date <= '" + date[1] + "'" + " and sensorid = " + str(sensor)
    else:
        query += "where sensorid = " + str(sensor)
    return query

def get_data(request_data):
    data = []
    sensors = request_data["sensors"]
    if isinstance(sensors, int):
        sensors = [sensors]
    for sensor in sensors:
        query = create_query(request_data, sensor)
        print(query)
        result = sql_query(query)
        result[0]["sensorid"] = sensor
        data += result
        print(data)
    return data

def query_insert_sensor(request):
    return "insert into sensor (id, city, country) values ({0}, '{1}', '{2}')".format(request["sensorid"], request["city"], request["country"])

@app.route('/', methods=['POST'])
def register_sensor():
    request_data = request.get_json()
    if not request_data:
        return Response("You have not passed any data", status=400)
    if "sensorid" not in request_data:
        return Response("Require sensorid value", status=400)
    if "country" not in request_data:
        request_data["country"] = None
    if "city" not in request_data:
        request_data["city"] = None
    query = query_insert_sensor(request_data)
    try:
        insert_sql_query(query)
    except ExistingValueError:
        return "Value already exists", 400
    response_data = {"city": request_data.get("city"), "sensorid": request_data.get("sensorid"), "country": request_data.get("country")}
    return jsonify(response_data), 201

@app.route('/', methods=['GET'])
def get_weather_data():
    request_data = request.get_json()
    if not request_data:
        return Response("Require request data", status=400)
    if "metrics" not in request_data:
        return Response("At least one metric required", status=400)
    if "sensors" not in request_data:
        return Response("At least one sensor required", status=400)
    try:
        data = get_data(request_data)
    except MalformedRequestError:
        return "Malformed request", 400
    return jsonify(data), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

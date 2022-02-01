import datetime

from app import app, query_insert_sensor, create_query, get_data
import unittest

class FlaskTest(unittest.TestCase):

    def test_get_status(self):
        with app.test_client() as c:
            rv = c.post('/', json={
                "sensorid": 4,
                "city": "Dublin",
                "country": "Ireland"
                })
            status = rv.status_code
            assert status == 201

    def test_post_json(self):
        with app.test_client() as c:
            rv = c.post('/', json={
                "sensorid": 5,
                "city": "Limerick",
                "country": "Ireland"
                })
            response = rv.get_json()
            print(response)
            assert response == {"sensorid": 5,"city": "Limerick", "country": "Ireland"}

    def test_post_json_not_empty(self):
        with app.test_client() as c:
            rv = c.post('/', json={
                "sensorid": 6,
                "city": "London",
                "country": "UK"
                })
            response = rv.get_json()
            print(response)
            assert response != []


    def test_get_status(self):
        with app.test_client() as c:
            rv = c.get('/', json={
                "metrics": "temperature",
                "sensors": 2
            })
            response = rv.status_code
            assert response == 201

    def test_get_json(self):
        with app.test_client() as c:
            rv = c.get('/', json={
                "metrics": "temperature",
                "sensors": 2
            })
            response = rv.get_json()
            print(response)
            assert response == [{'datetime': 'Fri, 03 Jan 2020 00:00:00 GMT', 'sensorid': 2, 'temperature': 2.0}]

    def test_get_json_not_empty(self):
        with app.test_client() as c:
            rv = c.get('/', json={
                "metrics": "temperature",
                "sensors": 2
            })
            response = rv.get_json()
            print(response)
            assert response != []

    def test_query_insert_sensor(self):
        request = {}
        request["sensorid"], request["city"], request["country"] = 1, "Cork", "Ireland"
        result = query_insert_sensor(request)
        assert result == "insert into sensor (id, city, country) values (1, 'Cork', 'Ireland')"

    def test_create_query(self):
        request = {"metrics": "temperature", "sensors": 1}
        result = create_query(request, 1)
        assert result == "select max(date) as datetime, avg(temperature) as temperature from weather where sensorid = 1"

    def test_get_data(self):
        request = {"metrics": "temperature", "sensors": [2]}
        result = get_data(request)
        assert result == [{'datetime': datetime.datetime(2020, 1, 3, 0, 0), 'temperature': 2.0, 'sensorid': 2}]
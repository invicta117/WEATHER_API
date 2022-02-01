# REST Weather API with Sensors

This is an example of a REST weather API that allows sensors to be registered and weather data to be queried

There are two endpoints available at port 8080

POST:
Sample post request
{
    "sensorid": 10,
    "city": "Vancoover",
    "country": "Canada"
}

GET:
Sample get request
{
    "metrics": "temperature",
    "sensors": [1,2]
    "date": ["2022/01/01", "2022/01/31""]
}

## Setup

To run the project please execute the command:

    docker-compose up

The application will launch and you will be able to access the API via http://localhost:5000/ using GET and POST commands.

## Additional Work

Some additional work that can be done includes:

- Using Flask models to access the data
- Further error checking on input to ensure it is of the correct form
- Custom errors when data is of incorrect format
- Improve test coverage with more unit tests and implementation tests
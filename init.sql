CREATE DATABASE IF NOT EXISTS weathersensors;
CREATE TABLE weathersensors.sensor(
    id bigint,
    country varchar(255),
    city varchar(255),
    primary key (id)
    );
INSERT INTO weathersensors.sensor (id, country, city) VALUES (1, "Ireland", "Cork");
INSERT INTO weathersensors.sensor (id, country, city) VALUES (2, "Ireland", "Galway");
INSERT INTO weathersensors.sensor (id, country, city) VALUES (3, "USA", "New York");
CREATE TABLE weathersensors.weather(
	sensorid bigint NOT NULL,
    `date` timestamp NOT NULL,
    temperature double,
    humidity double,
    windspeed double,
    PRIMARY KEY(sensorid,`date`)
    );
INSERT INTO weathersensors.weather (sensorid, `date`, temperature, humidity, windspeed) VALUES (1, "2020/01/01 00:00:00", 5, 10, 1);
INSERT INTO weathersensors.weather (sensorid, `date`, temperature, humidity, windspeed) VALUES (1, "2020/01/02 00:00:00", 6, 11, 2);
INSERT INTO weathersensors.weather (sensorid, `date`, temperature, humidity, windspeed) VALUES (2, "2020/01/03 00:00:00", 2, 5, 6);
use project;

CREATE TABLE influenza
(
ID int NOT NULL AUTO_INCREMENT,
type varchar(10),
year int,
age varchar(10),
county varchar(10),
week int,
cases int,
PRIMARY KEY (ID)
);

CREATE TABLE enterovirus
(
ID int NOT NULL AUTO_INCREMENT,
type varchar(10),
year int,
age varchar(10),
county varchar(10),
week int,
cases int,
PRIMARY KEY (ID)
);

CREATE TABLE AQI_day
(
ID int NOT NULL AUTO_INCREMENT,
SiteName varchar(10),
MonitorDate date,
AQI int,
PRIMARY KEY (ID)
);


CREATE TABLE AQI_hour
(
ID int NOT NULL AUTO_INCREMENT,
SiteName varchar(10),
County varchar(10),
AQI int, 
# Statu varchar(10),
SO2 decimal(5,2), 
CO decimal(5,2), 
O3 decimal(5,2), 
PM10 decimal(5,2), 
PM25 decimal(5,2), 
NO2 decimal(5,2), 
NOx decimal(5,2), 
NO decimal(5,2), 
WindSpeed decimal(5,2),
WindDirec int, 
DataCreationDate datetime,
Temp decimal(5,2),
Humidity decimal(5,2),
PRIMARY KEY (ID)
);
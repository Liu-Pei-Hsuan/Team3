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

CREATE TABLE COVID19
(
ID int NOT NULL AUTO_INCREMENT,
date date,
city varchar(10),
number int,
PRIMARY KEY (ID)
);

CREATE TABLE COVID19_foreign
(
ID int NOT NULL AUTO_INCREMENT,
date date,
number int,
PRIMARY KEY (ID)
);

CREATE TABLE product
(
ID int NOT NULL AUTO_INCREMENT,
prdClass varchar(45) NULL DEFAULT NULL,
prdName varchar(100) NULL DEFAULT NULL,
prdPrice varchar(45) NULL DEFAULT NULL,
prdUrl varchar(200) NULL DEFAULT NULL,
new_url varchar(4200) NULL DEFAULT NULL,
product_name varchar(200) NULL DEFAULT NULL,
PRIMARY KEY (ID)
);


### 1. 安全護目鏡
CREATE VIEW glass AS
	SELECT *  FROM product WHERE class = "安全護目鏡";
    
### 2. 活性碳口罩
CREATE VIEW mask AS
	SELECT *  FROM product WHERE class = "活性碳口罩";
    
### 3. 活性碳空氣清淨機
CREATE VIEW Air_clean AS
	SELECT *  FROM product WHERE class = "活性碳空氣清淨機";
    
### 4. 防毒面具 (只有一個商品)
CREATE VIEW Gas_mask AS
	SELECT *  FROM product WHERE class = "3M 6200防毒面具";

### 5. 一氧化碳偵測儀
CREATE VIEW CO_Detector AS
	SELECT *  FROM product WHERE class = "一氧化碳偵測儀";

### 6. 瓦斯警報器
CREATE VIEW Gas_alarm AS
	SELECT *  FROM product WHERE class = "瓦斯警報器";

### 7. PM2.5 空氣清淨機
CREATE VIEW PM25_clean AS
	SELECT *  FROM product WHERE class = "PM2.5 空氣清淨機";

### 8. 酒精
CREATE VIEW alcohol AS
	SELECT *  FROM product WHERE class = "酒精";

### 9. 酒精濕紙巾
CREATE VIEW alcohol_wipes AS
	SELECT *  FROM product WHERE class = "酒精濕紙巾";

### 10. 乾洗手
CREATE VIEW Dry_hands AS
	SELECT *  FROM product WHERE class = "乾洗手";

### 11. 不織布口罩
CREATE VIEW mask_il AS
	SELECT *  FROM product WHERE class = "不織布口罩";

### 12. 漂白水
CREATE VIEW bleach AS
	SELECT *  FROM product WHERE class = "漂白水";

### 13. 肥皂
CREATE VIEW soap AS
	SELECT *  FROM product WHERE class = "肥皂";
    
### 1. 桃園
CREATE VIEW Taoyuan AS
	SELECT *  FROM summary_data WHERE SiteName = "桃園";
    
### 2. 中壢
CREATE VIEW Zhongli AS
	SELECT *  FROM summary_data WHERE SiteName = "中壢";
    
### 3. 大園
CREATE VIEW Dayuan AS
	SELECT *  FROM summary_data WHERE SiteName = "大園";
    
### 4. 觀音
CREATE VIEW Guanyin AS
	SELECT *  FROM summary_data WHERE SiteName = "觀音";
    
### 5. 龍潭
CREATE VIEW Longtan AS
	SELECT *  FROM summary_data WHERE SiteName = "龍潭";
    
### 6. 平鎮
CREATE VIEW Pingzhen AS
	SELECT *  FROM summary_data WHERE SiteName = "平鎮";
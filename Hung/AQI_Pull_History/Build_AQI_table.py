# to_mysql
import os
import requests
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
import json
from sqlalchemy import create_engine
import sqlalchemy

#創建Table
engine = create_engine('mysql+pymysql://{}:{}@mqtt2.tibame.cloud/AQI_History'.format('yi','yi'))
engine.execute('CREATE TABLE IF NOT EXISTS `AQI_hour` ('
                '`DataCreationDate` text DEFAULT NULL,'
                '`SiteName` text DEFAULT NULL,'
                '`County` text DEFAULT NULL,'
                '`AQI` double DEFAULT NULL,'
                '`SO2` double DEFAULT NULL,'
                '`CO` double DEFAULT NULL,'
                '`O3` double DEFAULT NULL,'
                '`PM10` double DEFAULT NULL,'
                '`PM2.5` text DEFAULT NULL,'
                '`NO2` double DEFAULT NULL,'
                '`NOx` double DEFAULT NULL,'
                '`NO` double DEFAULT NULL,'
                '`WindSpeed` double DEFAULT NULL,'
                '`WindDirec` double DEFAULT NULL)'
                'ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;')
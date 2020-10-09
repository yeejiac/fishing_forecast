@echo off
mysql -u %1 -p %2 < "weather_Statement.sql"
pip install -r requirements.txt
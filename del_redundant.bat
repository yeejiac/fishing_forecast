@echo off
del "%~dp0\weather_data\%1.zip"
rmdir /s /q "%~dp0\weather_data\%1\"
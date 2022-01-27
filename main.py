#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Systempfad zum Sensor, weitere Systempfade könnten über ein Array
# oder weitere Variablen hier hinzugefügt werden.
sensor = '/sys/bus/w1/devices/'+os.getenv('SENSOR_FOLDER')+'/w1_slave'
api_key = os.getenv('API_KEY')
api_url = os.getenv('API_URL') + '?x-aio-key=' + api_key
request_delay = float(os.getenv('REQUEST_DELAY'))


def readTempSensor(sensorName):
    """Aus dem Systembus lese ich die Temperatur der DS18B20 aus."""
    f = open(sensorName, 'r')
    lines = f.readlines()
    f.close()
    return lines


def readTempLines(sensorName):
    lines = readTempSensor(sensorName)
    # Solange nicht die Daten gelesen werden konnten, bin ich hier in einer Endlosschleife
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = readTempSensor(sensorName)
    temperaturStr = lines[1].find('t=')
    # Ich überprüfe ob die Temperatur gefunden wurde.
    if temperaturStr != -1:
        tempData = lines[1][temperaturStr + 2:]
        tempCelsius = float(tempData) / 1000.0
        tempKelvin = 273 + float(tempData) / 1000
        tempFahrenheit = float(tempData) / 1000 * 9.0 / 5.0 + 32.0
        # Rückgabe als Array - [0] tempCelsius => Celsius...
        return [tempCelsius, tempKelvin, tempFahrenheit]


try:
    while True:
        # Mit einem Timestamp versehe ich meine Messung und lasse mir diese in der Console ausgeben.
        # print("Temperatur um " + time.strftime('%H:%M:%S') + " drinnen: " + str(readTempLines(sensor)[0]) + " °C")
        data = {
            'value': readTempLines(sensor)[0]
        }
        requests.post(api_url, data=data)
        # Nach x Sekunden erfolgt die nächste Messung
        time.sleep(request_delay)
except KeyboardInterrupt:
    # Programm wird beendet wenn CTRL+C gedrückt wird.
    print('Temperaturmessung wird beendet')
except Exception as e:
    print(str(e))
    sys.exit(1)
finally:
    # Das Programm wird hier beendet, sodass kein Fehler in die Console geschrieben wird.
    print('Programm wird beendet.')
    sys.exit(0)

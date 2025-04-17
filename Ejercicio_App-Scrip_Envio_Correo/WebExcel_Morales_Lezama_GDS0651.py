from machine import Pin
from machine import Pin
from time import sleep
from network import WLAN, STA_IF
from urequests import post
import random

WEBAPP_URL = "https://script.google.com/macros/s/AKfycbwFp2KwuBzFVTpYkSZkgrHx0cujbDGNYZyxdmdyXApCxdt7oaCuizD7QX3etRcvdab_/exec"

def connect_wifi():
    sta_if = WLAN(STA_IF)
    if not sta_if.active():
        sta_if.active(True)
    if not sta_if.isconnected():
        sta_if.connect("Megacable_RdLp84U", "99uh6AmygyWEqfKzz2")
        print("Conectando a WiFi", end="")
        while not sta_if.isconnected():
            print(".", end="")
            sleep(0.3)
    print("\nWiFi conectado con IP:", sta_if.ifconfig()[0])
    

def send_to_sheets(temp, hum):
    data = {
        "temp": temp,
        "hum": hum
    }
    try:
        response = post(WEBAPP_URL, json = data)
        print("Respuesta: ", response.text)
        response.close()
    except Exception as e:
        print("Error al enviar a hoja de calculo: ", e)
    
connect_wifi()

while True:
    try:
        temp = 30.01
        hum = random.random()
        print(f"Temperatura: {temp:.1f}°C")
        print (f"Humedad: {hum:.1f}%")
        print("-"*20)
        send_to_sheets(temp, hum)
    except Exception as e:
        print("Error de lectura de sensor: ", e)
    sleep(4);

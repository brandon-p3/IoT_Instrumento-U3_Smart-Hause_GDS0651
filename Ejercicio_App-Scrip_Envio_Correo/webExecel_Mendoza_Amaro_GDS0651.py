from machine import Pin
from time import sleep
from dht import DHT22
from network import WLAN, STA_IF
from urequests import post
import urandom

dht_sensor = DHT22(Pin(17))
WEBAPP_URL = "https://script.google.com/macros/s/AKfycbyLiTg8Ke1p8UusOWc0RiC0Hp7755wxDmIbbB_4UdmLkJdYrykSoY_Pt7UdVZjh-CFk/exec"


def connect_wifi():
    sta_if = WLAN(STA_IF)
    sta_if.active(True)
    sta_if.connect("GUS_LAP 9476", "@95X393b")
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("Wifi OK")

def send_to_sheets(temp, hum):
    data = {
        "temp": temp,
        "hum": hum
    }
    try:
        response = post(WEBAPP_URL, json = data)
        print("Respuesta Guardada: ", response.text)
        response.close()

    except Exception as e:
        print("Error al enviar los datos a la hoja de calculo", e)

connect_wifi()



while True:
    try:
        temp = urandom.uniform(20, 35)  
        hum = urandom.uniform(30, 80)
        
        print(f"Temperatura: {temp:.1f}°C")
        print(f"Humedad: {hum:.1f}%")
        print("-"*20)

        send_to_sheets(temp, hum)

        sleep(2)  

    except Exception as e:
        print("Error al leer el sensor:", e)

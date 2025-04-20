from machine import Pin, PWM, ADC
from network import WLAN, STA_IF
from time import sleep, ticks_us, ticks_diff
from urequests import post
import network
import time
from umqtt.simple import MQTTClient
import ujson 

# -------------------- Configuración WiFi y MQTT --------------------
SSID = "Megacable_RdLp84U"
PASSWORD = "99uh6AmygyWEqfKzz2"
MQTT_BROKER = "192.168.0.36"
MQTT_TOPIC = "smartHause/sensor/humo"
MQTT_TOPIC2 = "smartHause/sensor/ultrasonico"
MQTT_TOPIC3 = "smartHause/sensor/humo/enviar"

WEBAPP_URL = "https://script.google.com/macros/s/AKfycbxquHQl_BTEvyTmLvFuprc6-cgBMk5CS_9Bi1On_ugHJRyU1PBxXZhFdadoQSsPd9cF/exec"

# --- Buzzer ---
buzzer = PWM(Pin(15), freq=1000)
buzzer.duty(0)

# --- Sensor Ultrasonico HC-SR04 ---
trig = Pin(5, Pin.OUT)
echo = Pin(4, Pin.IN)

# --- Sensor de gas MQ-2 (Analógico) ---
mq2 = ADC(Pin(34))
mq2.atten(ADC.ATTN_11DB)
mq2.width(ADC.WIDTH_10BIT)

# --- Botón de reset ---
boton_reset = Pin(12, Pin.IN, Pin.PULL_UP)

# -------------------- Conexión WiFi --------------------
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)

print("✅ Conectado a WiFi!")

# -------------------- Conexión MQTT --------------------
try:
    client = MQTTClient("ESP32", MQTT_BROKER)
    client.connect()
    print("✅ Conectado a MQTT!")
except OSError as e:
    print("❌ Error al conectar a MQTT:", e)
    raise

# -------------------- Funciones --------------------
def enviar_alerta_gas(nivel):
    try:
        data = {
            "sensor": "MQ-2",
            "nivel": nivel
        }
        response = post(WEBAPP_URL, json=data)
        print("📩 Alerta enviada: ", response.text)
        response.close()
    except Exception as e:
        print("❌ Error al enviar alerta:", e)

def medir_distancia():
    trig.value(0)
    sleep(0.002)
    trig.value(1)
    sleep(0.01)
    trig.value(0)

    timeout = 10000
    while echo.value() == 0 and timeout > 0:
        timeout -= 1
    if timeout <= 0:
        return 999

    inicio = ticks_us()

    timeout = 10000
    while echo.value() == 1 and timeout > 0:
        timeout -= 1
    if timeout <= 0:
        return 999

    fin = ticks_us()
    duracion = ticks_diff(fin, inicio)
    distancia = duracion / 58.0
    return distancia

def sonar_timbre():
    tonos = [880, 988, 1047]
    for _ in range(2):
        for tono in tonos:
            buzzer.freq(tono)
            buzzer.duty(512)
            sleep(0.15)
            buzzer.duty(0)
            sleep(0.05)
    sleep(2)

def sonar_alarma():
    buzzer.freq(2000)
    buzzer.duty(512)

def detener_alarma():
    buzzer.duty(0)

# -------------------- Variables de control --------------------
umbral_gas = 1000
alerta_enviada = False
alarma_activa = False
alarma_desactivada_por_usuario = False

# -------------------- Loop principal --------------------
while True:
    # --- Sensor ultrasonico ---
    distancia = medir_distancia()
    if distancia < 999:
        if distancia < 20:
            print("🚪 Hay alguien en la puerta")
            mensaje = ujson.dumps({
                "id_sensor": 4,  
                "mensaje": "Hay alguien en la puerta",
                "valor": distancia
            })
            client.publish(MQTT_TOPIC2, mensaje.encode())
            sonar_timbre()
    else:
        print("⚠ Error al medir distancia")

    # --- Sensor de gas ---
    nivel_gas = mq2.read()

    if nivel_gas > umbral_gas and not alarma_desactivada_por_usuario:
        print("🚨 ¡Gas detectado!")
        if not alerta_enviada:
            enviar_alerta_gas(nivel_gas)
            alerta_enviada = True
            mensaje = ujson.dumps({
                "id_sensor": 4,  
                "mensaje": "Hay una alta concentración de humo dentro de la casa, !!PELIGRO¡¡",
                "valor": nivel_gas
            })
            client.publish(MQTT_TOPIC, mensaje.encode())
            client.publish(MQTT_TOPIC3, str(nivel_gas))

        alarma_activa = True
        inicio = time.time()

        # 🔁 Mantenerse en modo alerta durante 60 segundos
        while time.time() - inicio < 60:
            sonar_alarma()
            if boton_reset.value() == 0:
                print("🔕 Alarma desactivada por el usuario")
                alarma_activa = False
                alarma_desactivada_por_usuario = True
                detener_alarma()
                break
            sleep(0.2)

    else:
        if nivel_gas <= umbral_gas:
            alarma_desactivada_por_usuario = False
            alerta_enviada = False
            alarma_activa = False
            detener_alarma()
            client.publish(MQTT_TOPIC3, str(0))
        else:
            print("✅ Nivel de gas normal")
            sleep(5)

    sleep(0.2)

from machine import Pin, PWM
from time import sleep, ticks_ms
import network
import time
from umqtt.simple import MQTTClient

# -------------------- Configuración WiFi y MQTT --------------------
SSID = "Megacable_RdLp84U"
PASSWORD = "99uh6AmygyWEqfKzz2"
MQTT_BROKER = "192.168.0.40"

MQTT_TOPIC_LUZ = "smartHause/sensor/foto"
MQTT_TOPIC_LLUVIA = "smartHause/sensor/lluvia"
MQTT_TOPIC_CONTROL = "smartHause/sensor/recibir"  # ← desde aquí llega el control manual

# -------------------- Pines --------------------
IN1 = Pin(25, Pin.OUT)
IN2 = Pin(26, Pin.OUT)
IN3 = Pin(33, Pin.OUT)
IN4 = Pin(32, Pin.OUT)
pins = [IN1, IN2, IN3, IN4]

sensor_agua = Pin(14, Pin.IN)
sensor_luz = Pin(16, Pin.IN)

led_rojo = PWM(Pin(5), freq=1000)
led_verde = PWM(Pin(4), freq=1000)
led_azul = PWM(Pin(2), freq=1000)

# -------------------- Motor: Secuencias --------------------
sequence_right = [  # Cerrar techo
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0]
]
sequence_left = sequence_right[::-1]  # Abrir techo

# -------------------- Funciones: Motor y LED --------------------
def step_motor_time(sequence, delay, duration_sec):
    start = ticks_ms()
    while ticks_ms() - start < duration_sec * 1000:
        for step in sequence:
            for i in range(4):
                pins[i].value(step[i])
            sleep(delay)
    apagar_motor()

def apagar_motor():
    for pin in pins:
        pin.value(0)

def abrir_techo():
    print("🔄 Abriendo techo...")
    step_motor_time(sequence_left, delay=0.005, duration_sec=2)

def cerrar_techo():
    print("🔄 Cerrando techo...")
    step_motor_time(sequence_right, delay=0.005, duration_sec=3)

def set_color(r, g, b):
    led_rojo.duty(1023 - r)
    led_verde.duty(1023 - g)
    led_azul.duty(1023 - b)

def encender_rgb_calido():
    set_color(r=1023, g=400, b=0)

def apagar_rgb():
    set_color(0, 0, 0)

# -------------------- Conexión WiFi --------------------
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)
print("✅ Conectado a WiFi!")

# -------------------- MQTT --------------------
def llegada_mensaje(topic, msg):
    mensaje = msg.decode()
    print("📥 Mensaje recibido en", topic.decode(), ":", mensaje)

    if topic.decode() == MQTT_TOPIC_CONTROL:
        if mensaje == "0":
            abrir_techo()
        elif mensaje == "1":
            cerrar_techo()
        else:
            print("⚠ Comando desconocido")

client = MQTTClient("ESP32_SISTEMA", MQTT_BROKER)
client.set_callback(llegada_mensaje)
client.connect()
client.subscribe(MQTT_TOPIC_CONTROL.encode())
print("✅ Suscrito a:", MQTT_TOPIC_CONTROL)

# -------------------- Estado inicial --------------------
print("🛠️ Sistema iniciado. Abriendo techo por seguridad...")
abrir_techo()
estado_anterior_agua = sensor_agua.value()
estado_anterior_luz = sensor_luz.value()
lluvia_en_curso = False
tiempo_inicio_lluvia = 0

# -------------------- Bucle principal --------------------
while True:
    # --- Sensor de agua (modo automático) ---
    estado_actual_agua = sensor_agua.value()
    if estado_actual_agua != estado_anterior_agua:
        if estado_actual_agua == 1:
            print("💧 Agua detectada. Cerrando techo.")
            cerrar_techo()
            mensaje = ujson.dumps({
                "id_sensor": 4,  
                "mensaje": "Agua detectada. Techo cerrado.",
                "valor": 0
            })
            client.publish(MQTT_TOPIC_LLUVIA, mensaje.encode())
            lluvia_en_curso = True
            tiempo_inicio_lluvia = ticks_ms()
        else:
            print("✅ No hay agua. Abriendo techo.")
            abrir_techo()
            if lluvia_en_curso:
                duracion_ms = ticks_ms() - tiempo_inicio_lluvia
                duracion_horas = round(duracion_ms / (1000 * 60 * 60))  # Convertir a horas
                print(f"⏱️ Duración de la lluvia: {duracion_horas} horas")
                mensaje = ujson.dumps({
                    "id_sensor": 4,
                    "mensaje": "Lluvia finalizada. Duración en horas.",
                    "valor": duracion_horas
                })
                client.publish(MQTT_TOPIC_LLUVIA, mensaje.encode())
                lluvia_en_curso = False
        estado_anterior_agua = estado_actual_agua

    # --- Sensor de luz (iluminación nocturna) ---
    estado_actual_luz = sensor_luz.value()
    if estado_actual_luz != estado_anterior_luz:
        if estado_actual_luz == 1:
            print("🌙 Noche detectada. Encendiendo entrada.")
            encender_rgb_calido()
            mensaje = ujson.dumps({
                "id_sensor": 4,  
                "mensaje": "Noche detectada. Luz encendida.",
                "valor": 1
            })
            client.publish(MQTT_TOPIC_LUZ, mensaje.encode())
        else:
            print("☀️ Día detectado. Apagando luces.")
            apagar_rgb()
            mensaje = ujson.dumps({
                "id_sensor": 4,  
                "mensaje": "Día detectado. Luz apagada.",
                "valor": 0
            })
            client.publish(MQTT_TOPIC_LUZ, mensaje.encode())
        estado_anterior_luz = estado_actual_luz
    client.check_msg()  # Recibir mensajes manuales

    sleep(1)

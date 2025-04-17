from machine import Pin, PWM
from time import sleep
import network
from umqtt.simple import MQTTClient

# -------- Pines del motor y servo --------
in1 = Pin(26, Pin.OUT)
in2 = Pin(27, Pin.OUT)
ena = PWM(Pin(25), freq=1000)
servo = PWM(Pin(5), freq=50)

# -------- Funciones para hardware --------
def mover_servo(grados):
    duty = int((grados / 180) * 102 + 26)
    servo.duty(duty)

def encender_motor():
    in1.on()
    in2.off()
    ena.duty(1023)

def apagar_motor():
    in1.off()
    in2.off()
    ena.duty(0)

# -------- Conexión WiFi --------
def conectar_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect("Megacable_RdLp84U", "99uh6AmygyWEqfKzz2")

    while not wifi.isconnected():
        print("Conectando a WiFi...")
        sleep(1)

    print("✅ Conectado a WiFi!")

# -------- Callback MQTT unificada --------
def llegada_mensaje(topic, msg):
    try:
        valor = int(msg.decode())
        topic_str = topic.decode()
        print(f"📥 Mensaje recibido del tópico {topic_str}: {valor}")

        if topic_str == "smartHause/sensor/humo/recibir":
            # --- Lógica para valores mayores a 1000 ---
            if valor > 1000:
                print("✅ Activando: valor mayor a 1000")
                mover_servo(45)
                encender_motor()
                print("📤 Sistema activado")
            else:
                print("❌ Desactivando: valor menor o igual a 1000")
                mover_servo(150)
                apagar_motor()
                print("📤 Sistema desactivado")

        elif topic_str == "smartHause/sensor/recibir":
            # --- Lógica por comandos directos ---
            if valor == 4:
                print("🔁 Encendiendo motor (ventilador)")
                encender_motor()
            elif valor == 5:
                print("🛑 Apagando motor (ventilador)")
                apagar_motor()
            elif valor == 2:
                print("🔓 Abriendo ventana")
                mover_servo(45)
            elif valor == 3:
                print("🔒 Cerrando ventana")
                mover_servo(150)
            else:
                print("⚠ Comando no reconocido:", valor)

    except ValueError:
        print("⚠ Mensaje inválido, no es un número:", msg.decode())

# -------- Conexión MQTT --------
conectar_wifi()
client = MQTTClient("ESP32_SUSCRIPTOR", "192.168.0.40")
client.set_callback(llegada_mensaje)
client.connect()
client.subscribe(b"smartHause/sensor/humo/recibir")
client.subscribe(b"smartHause/sensor/recibir")
print("✅ Suscrito a los tópicos MQTT")

# -------- Loop principal --------
while True:
    client.check_msg()
    sleep(0.1)
# 🏠 SMART-HOME: Sistema Inteligente de Automatización Residencial

## Descripción General

**SMART-HOME** es un sistema de automatización residencial diseñado para cuidar prendas de ropa, optimizar el uso de energía y mejorar la seguridad del hogar mediante sensores y actuadores conectados a través de una red de microcontroladores **ESP32**. Este ecosistema inteligente se coordina mediante **Node-RED** sobre una **máquina virtual en Raspberry Pi**, e incluye visualización gráfica, control manual y almacenamiento de datos en **PostgreSQL**.

El sistema combina sensores de ambiente con controladores mecánicos para realizar acciones automáticas como:
- Proteger la ropa cuando llueve.
- Apagar o encender luces RGB según el nivel de luz natural.
- Detectar humo y actuar en consecuencia.
- Detectar presencia en la puerta principal.
- Controlar actuadores remotamente desde una interfaz gráfica web.

---

## 🎯 Objetivos del Proyecto

- Automatizar procesos domésticos mediante sensores y actuadores.
- Diseñar una solución IoT descentralizada basada en múltiples ESP32.
- Visualizar datos en tiempo real y guardar el histórico en una base de datos PostgreSQL.
- Proporcionar control manual de dispositivos desde una interfaz web construida en Node-RED.
- Crear una maqueta física representativa con componentes impresos en 3D.

---

## ⚙️ Tecnologías Utilizadas

| Tecnología       | Uso Principal                                   |
|------------------|--------------------------------------------------|
| ESP32            | Microcontroladores para manejar sensores/actuadores |
| Node-RED         | Plataforma de control e interfaz web             |
| Raspberry Pi     | Máquina virtual que aloja Node-RED y PostgreSQL  |
| PostgreSQL       | Base de datos relacional para almacenamiento de datos |
| MQTT             | Protocolo de mensajería entre nodos ESP32 y Node-RED |
| Impresión 3D     | Estructuras físicas y mecanismos personalizados   |

---

## 🧠 Arquitectura del Sistema

El sistema está distribuido en **3 placas ESP32**, cada una encargada de distintos sensores y actuadores. La comunicación entre ellas se realiza mediante **MQTT**, utilizando Node-RED como broker e interfaz de control centralizada.

```
        [ESP32-1] ---> Motor Paso, Sensor de Lluvia, LDR
        [ESP32-2] ---> Detector de Humo, Servo, Buzzer, Motor DC
        [ESP32-3] ---> Sensor Ultrasónico, Buzzer

                      ↕  MQTT
                    [Node-RED]
                        ↕
                    [PostgreSQL]
```

---

## 🧹 Tabla de Actuadores

| Nombre           | Tipo                 | Uso                                                 | Imagen |
|------------------|----------------------|------------------------------------------------------|--------|
| Motor Paso       | Motor (Pasos)        | Subir o bajar el techo en caso de lluvia             | ![](img/motor_pasos.jpg) |
| Servo Motor      | Servo                | Abrir la ventana si se detecta humo                  | ![](img/servo.jpg) |
| Buzzer           | Actuador Sonoro      | Sonar en caso de humo o presencia detectada en puerta | ![](img/buzzer.jpg) |
| Leds RGB         | Iluminación RGB      | Encender o apagar según el nivel de luz              | ![](img/led_rgb.jpg) |
| Motor Micro DC   | Motor DC + Driver    | Activar ventilador cuando se detecta humo            | ![](img/motor_dc.jpg) |

---

## 🌧️ Tabla de Sensores

| Nombre                       | Tipo                  | Uso                                                  | Imagen |
|------------------------------|-----------------------|-------------------------------------------------------|--------|
| Sensor Ultrasónico HC-SR04  | Proximidad            | Detectar presencia en la entrada principal           | ![](img/hcsr04.jpg) |
| Detector de Humo MQ-2       | Gas y Humo            | Activar alarma, abrir ventana, y prender ventilador   | ![](img/mq2.jpg) |
| Sensor de Lluvia YL-83      | Humedad superficial   | Detectar lluvia para subir el techo                  | ![](img/yl83.jpg) |
| Sensor de Luz LDR           | Fotoresistencia       | Medir luz natural y controlar luces RGB              | ![](img/ldr.jpg) |

---

## 🛠️ Funcionalidad del Sistema

### ☔ Protección contra Lluvia
Cuando el sensor **YL-83** detecta lluvia, se activa el **motor de pasos**, que sube el techo para proteger la ropa tendida.

### ☀️ Control de Iluminación
El sensor **LDR** mide la luz ambiental. Si hay suficiente luz natural, se apagan las luces **RGB**; si hay poca, se encienden automáticamente.

### 🔥 Detección de Humo
El sensor **MQ-2** detecta humo o gases peligrosos, lo que activa:
- El **buzzer** como alarma.
- El **servo motor** para abrir una ventana.
- El **motor DC** para encender un ventilador que ventile el área.

### 🚪 Detección de Presencia
El **sensor ultrasónico HC-SR04** detecta si alguien se encuentra en la puerta principal. En ese caso, se activa el **buzzer** para notificar presencia.

---

## 💻 Interfaz Gráfica

La interfaz fue desarrollada en **Node-RED** y permite:
- Controlar manualmente el techo, ventilador y ventana.
- Visualizar gráficas en tiempo real de los sensores.
- Encender/apagar los actuadores desde cualquier navegador.

**Ejemplo de interfaz:**

> ![](img/interfaz_nodered.jpg)

---

## 🏠 Maqueta Física

La casa fue creada con materiales comunes de maqueta, pero incorpora piezas funcionales impresas en 3D como:
- El mecanismo del techo móvil.
- Soportes para sensores y actuadores.
- Estructuras para ventanas funcionales.

**Imágenes de la maqueta:**

> ![](img/maqueta_frontal.jpg)  
> ![](img/mecanismo_techo.jpg)

---

## 🧪 Base de Datos y Almacenamiento

El sistema guarda todos los datos generados por los sensores en una base de datos **PostgreSQL**, permitiendo:
- Consultas históricas de temperaturas, humo, lluvia, presencia, etc.
- Análisis estadístico posterior.
- Exportación de datos para informes o visualización externa.

---

## 🔐 Seguridad y Escalabilidad

- El sistema puede ser escalado fácilmente con nuevos sensores o actuadores.
- Se puede configurar para notificaciones por correo o Telegram en caso de emergencias.
- Posibilidad de integrar cámaras IP o autenticación de usuarios en la interfaz web.

---

## 🚀 Conclusión

**SMART-HOME** representa una solución integral de automatización residencial enfocada en el cuidado del hogar y de sus habitantes. Combina electrónica, IoT, desarrollo web y diseño 3D en un proyecto funcional, modular y escalable.

---

## 📂 Estructura del Proyecto

```
/smart-home/
│
├── img/                         # Imágenes para el README
├── docs/                        # Documentación técnica adicional
├── node-red-flows/             # Flujos de Node-RED exportados
├── esp32-codigo/               # Códigos para los ESP32
├── sql/                        # Scripts para PostgreSQL
├── README.md                   # Este archivo
└── ...
```

---

## ✍️ Autores

- **Nombre del equipo**: _[Tu Equipo Smart Home]_
- **Integrantes**:
  - Nombre 1 - [@github_user]
  - Nombre 2 - [@github_user]
  - Nombre 3 - [@github_user]

---

## 📌 Notas Finales

> Este proyecto fue desarrollado como parte de una asignatur

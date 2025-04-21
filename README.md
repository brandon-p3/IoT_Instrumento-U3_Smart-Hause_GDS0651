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

## 🧹 **Tabla de Actuadores**

| **Nombre**         | **Tipo**              | **Uso**                                                    | **Imagen** |
|--------------------|-----------------------|-------------------------------------------------------------|------------|
| **Motor Paso**     | Motor (Pasos)         | Subir o bajar el techo en caso de lluvia                    | <img src="https://github.com/user-attachments/assets/e7c641b1-ff37-40ef-8c2c-9576ee7891ee" width="100"> |
| **Servo Motor**    | Micro ServoMotor      | Abrir la ventana si se detecta humo                         | <img src="https://github.com/user-attachments/assets/ddad088b-02e3-463b-9cb3-6301d5e40070" width="100"> |
| **Buzzer Pasivo**  | Actuador Sonoro       | Sonar en caso de humo o presencia detectada en puerta       | <img src="https://github.com/user-attachments/assets/dfef9d15-3674-43f1-a72b-3b714f6f3f0e" width="100"> |
| **Leds RGB**       | Iluminación RGB       | Encender o apagar según el nivel de luz                     | <img src="https://github.com/user-attachments/assets/9059f6e2-0149-417f-9d82-783c3736f98b" width="100"> |
| **Motor Micro DC** | Motor DC + Driver     | Activar ventilador cuando se detecta humo                   | <img src="https://github.com/user-attachments/assets/3042e365-f1be-4ba3-bcd8-de3d46382f9d" width="100"> |

---

## 🌧️ **Tabla de Sensores**

| **Nombre**                   | **Tipo**              | **Uso**                                                    | **Imagen** |
|------------------------------|-----------------------|-------------------------------------------------------------|------------|
| **Sensor Ultrasónico HC-SR04** | Proximidad          | Detectar presencia en la entrada principal                  | <img src="https://github.com/user-attachments/assets/25fab6bb-46bb-42de-9205-a2f2226286b6" width="100"> |
| **Detector de Humo MQ-2**   | Gas y Humo            | Activar alarma, abrir ventana, y prender ventilador         | <img src="https://github.com/user-attachments/assets/26c3eef8-ee24-44e1-9594-23640b22080c" width="100"> |
| **Sensor de Lluvia YL-83**  | Humedad superficial   | Detectar lluvia para subir el techo                         | <img src="https://github.com/user-attachments/assets/501125ca-f021-49b0-81f4-7571ea8b3cac" width="100"> |
| **Sensor de Luz LDR**       | Fotoresistencia       | Medir luz natural y controlar luces RGB                     | <img src="https://github.com/user-attachments/assets/b8101240-da5d-4628-b200-595423f2ff32" width="100"> |

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
- Visualizar graficas y metricas sobre el estado de las ultimas 10 detecciones por parte del MQ-02
- Visualizar graficas y metricas sobre la duracion (Horas) de las lluvia en las ultimas 10 detecciones de lluvia

**Ejemplo de interfaz:**
<img src="https://github.com/user-attachments/assets/91fc5a65-bb0f-47d3-a1e2-feef6ea24597">

---

## 🏠 Maqueta Física

La casa fue creada con materiales comunes de maqueta, pero incorpora piezas funcionales impresas en 3D como:
- El mecanismo del techo móvil.
- Soportes para sensores y actuadores.
- Estructuras para ventanas funcionales.

**📸 Imágenes de la maqueta del proyecto**
<div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; margin-top: 20px;"> <img src="https://github.com/user-attachments/assets/4df8ea1f-31ee-44a6-a3de-5d4c789c40a6" alt="Imagen 1" style="width: 300px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);"> <img src="https://github.com/user-attachments/assets/ee243578-3fab-410a-8f33-38600f44963d" alt="Imagen 2" style="width: 300px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);"> <img src="https://github.com/user-attachments/assets/42570bd8-5916-4985-ba0b-01f4823fff46" alt="Imagen 3" style="width: 300px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);"> <img src="https://github.com/user-attachments/assets/6ab9da89-50d0-4e04-9206-b45e710d8ad3" alt="Imagen 4" style="width: 300px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);"> </div>

---
## 🏠 Diagramas de las placas
**Placa 1 (MQ-02, BUZZER, DISTANCIA)**
<br>
Link: https://wokwi.com/projects/427323546919923713 
<img src="https://github.com/user-attachments/assets/e294dc95-e62f-449d-bf96-126de5ad4691">
<br>
**Placa 2 (SERVO, MOTOR DC)**
<br>
Link: https://wokwi.com/projects/427323546919923713
<img src="https://github.com/user-attachments/assets/65d1d161-48c8-4386-9c08-3418c299231e">

<br>
**Placa 3 (LLUVIA, LDR, RGB, MOTOR-PASOS)**
<br>
Link: https://app.cirkitdesigner.com/project/b07a5b19-9e06-4433-bb01-3e5187981fbb 
<img src="https://github.com/user-attachments/assets/cbe0dc9b-e2ec-4521-84fb-8ee250ee25aa">
---

## 🧪 Base de Datos y Almacenamiento

El sistema guarda todos los datos generados por los sensores en una base de datos **PostgreSQL**, permitiendo:
- Consultas históricas de temperaturas, humo, lluvia, presencia, etc.
- Análisis estadístico posterior.
- Exportación de datos para informes o visualización externa.

**Funcionamiento envio correo**

<img src="https://github.com/user-attachments/assets/834f0bbf-a2d1-4bad-9daf-bf862f438c6c">

---


## Videos explicando el funcionamiento de cada placa

Link a videos

https://drive.google.com/drive/folders/1Mwg-OasbqF_vHa8ZhzucIkqC5u0zefmu?usp=drive_link

## Videos explicando el funcionamiento general de toda la casa

Link a videos

https://drive.google.com/drive/folders/12ORMXZAib9PHsuYNOvswGEr8jB9Gjxr0?usp=sharing

## Evidencia (Videos) de los clientes que aprueban el proyecto

Link a videos

https://drive.google.com/drive/folders/1yig3J2GGEPOLDp7m1ZyxWFej3fN-4ZA3?usp=sharing

---

## Ejecicios de Clase

Link a videos

https://drive.google.com/drive/folders/1GOXApjWNVipbJKVLVaaz4QoqaaGXq0BR?usp=sharing

## Coevaluación

https://docs.google.com/document/d/1jDS9AxsSn1z5lsY4fK3YzhkUiO5Kk1glECyVzDjCRfc/edit?usp=sharing

---

## ✍️ Autores

- **Nombre del equipo**: SmartHome GDS0651
- **Integrantes**:
  - Mendoza Amaro Brandon Gustavo - brandon-p3
  - Morales Lezama Mirza Natzielly  - Mirza Morales
  - Ramirez Ramirez Lizett 

---

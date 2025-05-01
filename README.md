# Taller-T21-SD
##  Descripción general

Este sistema implementa una arquitectura distribuida basada en el patrón **Publicador-Suscriptor (Pub/Sub)** con un **Broker central** utilizando **ZeroMQ (ZMQ)** como middleware de mensajería. Se simula un flujo de cálculo en dos etapas, procesado por múltiples nodos en distintas máquinas virtuales.

---

##  Componentes y asignación de roles por IP

| Rol                      | IP              | Archivo ejecutable              |
|--------------------------|------------------|----------------------------------|
| Broker principal         | `10.43.103.197`  | `broker.py`                      |
| Cliente                  | `10.43.103.204`  | `cliente.py`                     |
| Servidor de cálculo      | `10.43.103.30`   | `servidor_calculo.py`           |
| Servidor de operación 1  | `10.43.103.30`   | `servidor_operacion1.py`        |
| Servidor de operación 2  | `10.43.103.102`  | `servidor_operacion2.py`        |
| Broker de respaldo       | `10.43.103.30`   | `broker_backup.py`              |

---

##  Flujo de comunicación

1. **Cliente** publica una solicitud con 3 números y 2 operaciones.
2. **Servidor de cálculo** divide el trabajo y publica dos subtareas.
3. **Servidor de operación 1** realiza la primera operación.
4. El resultado parcial es enviado de vuelta al **Servidor de cálculo**.
5. Este lo envía a **Servidor de operación 2** con el segundo número y operación.
6. El resultado final se publica y es recibido por el **cliente**.

---

##  Tópicos utilizados

| Tópico                   | Emisor                         | Receptor                         |
|--------------------------|--------------------------------|----------------------------------|
| `solicitud/calculo_total`| Cliente                        | Servidor de cálculo              |
| `solicitud/parcial1`     | Servidor de cálculo            | Servidor de operación 1          |
| `respuesta/parcial1`     | Servidor de operación 1        | Servidor de cálculo              |
| `solicitud/parcial2`     | Servidor de cálculo            | Servidor de operación 2          |
| `respuesta/final`        | Servidor de operación 2        | Cliente                          |

---

##  Instrucciones de ejecución

> Ejecutar **cada componente en su máquina respectiva**, en el siguiente orden:

### 1. Iniciar broker principal
```bash
python3 broker.py

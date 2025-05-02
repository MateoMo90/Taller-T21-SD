import zmq
import json
import time

def calcular_operacion(num1, num2, op):
    if op == "+": return num1 + num2
    elif op == "-": return num1 - num2
    elif op == "*": return num1 * num2
    elif op == "/": return num1 / num2 if num2 != 0 else 0
    return 0

def servidor_calculo_resiliente():
    context = zmq.Context()

    sub = context.socket(zmq.SUB)
    sub.connect("tcp://10.43.103.197:5556")
    sub.connect("tcp://10.43.103.30:5556")
    sub.setsockopt_string(zmq.SUBSCRIBE, "respuesta/parcial1")
    sub.setsockopt_string(zmq.SUBSCRIBE, "respuesta/final")
    sub.setsockopt_string(zmq.SUBSCRIBE, "solicitud/calculo_total")

    pub = context.socket(zmq.PUB)
    pub.connect("tcp://10.43.103.197:5555")
    pub.connect("tcp://10.43.103.30:5555")

    poller = zmq.Poller()
    poller.register(sub, zmq.POLLIN)

    datos_guardados = None
    resultado1_guardado = None
    estado = "idle"
    tiempo_inicio = 0
    TIMEOUT = 0.5  # medio segundo

    while True:
        now = time.time()
        socks = dict(poller.poll(50))  # espera 50ms

        if sub in socks:
            msg = sub.recv_string()
            topico, data = msg.split(" ", 1)
            contenido = json.loads(data)

            if topico == "solicitud/calculo_total":
                print("➡️ Recibida solicitud de cálculo total")
                datos_guardados = contenido
                resultado1_guardado = None
                estado = "esperando_parcial1"
                tiempo_inicio = now
                pub.send_string("solicitud/parcial1 " + json.dumps(contenido))

            elif topico == "respuesta/parcial1" and estado == "esperando_parcial1":
                print("✅ Recibida respuesta parcial1")
                resultado1 = contenido["resultado"]
                resultado1_guardado = resultado1
                datos_guardados["intermedio"] = resultado1
                estado = "esperando_parcial2"
                tiempo_inicio = now
                pub.send_string("solicitud/parcial2 " + json.dumps(datos_guardados))

            elif topico == "respuesta/final" and estado == "esperando_parcial2":
                print("✅ Recibida respuesta final:", contenido["total"])
                estado = "idle"

        # TIMEOUT esperando parcial1
        if estado == "esperando_parcial1" and (now - tiempo_inicio > TIMEOUT):
            print("⚠️ Timeout esperando parcial1. Ejecutando respaldo local...")
            num1 = datos_guardados["num1"]
            num2 = datos_guardados["num2"]
            op1 = datos_guardados["op1"]
            resultado1_guardado = calcular_operacion(num1, num2, op1)
            datos_guardados["intermedio"] = resultado1_guardado
            estado = "esperando_parcial2"
            tiempo_inicio = time.time()
            pub.send_string("solicitud/parcial2 " + json.dumps(datos_guardados))

        # TIMEOUT esperando parcial2
        elif estado == "esperando_parcial2" and (now - tiempo_inicio > TIMEOUT):
            print("⚠️ Timeout esperando parcial2. Ejecutando respaldo local...")
            intermedio = resultado1_guardado
            num3 = datos_guardados["num3"]
            op2 = datos_guardados["op2"]
            resultado_final = calcular_operacion(intermedio, num3, op2)
            print("✅ Resultado final LOCAL:", resultado_final)
            pub.send_string("solicitud/parcial1 " + json.dumps(contenido))

            estado = "idle"

        time.sleep(0.05)

if __name__ == '__main__':
    servidor_calculo_resiliente()

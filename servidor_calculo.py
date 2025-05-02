import zmq
import json
import time

def calcular_operacion(num1, num2, op):
    if op == "+":
        return num1 + num2
    elif op == "-":
        return num1 - num2
    elif op == "*":
        return num1 * num2
    elif op == "/":
        return num1 / num2 if num2 != 0 else 0
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
    esperando_respuesta1 = False
    esperando_respuesta2 = False

    while True:
        socks = dict(poller.poll(1000))  # Espera hasta 1 segundo
        if sub in socks:
            msg = sub.recv_string()
            topico, data = msg.split(" ", 1)
            contenido = json.loads(data)

            if topico == "solicitud/calculo_total":
                datos_guardados = contenido
                esperando_respuesta1 = True
                esperando_respuesta2 = False
                pub.send_string("solicitud/parcial1 " + json.dumps(contenido))
                continue

            if topico == "respuesta/parcial1":
                resultado1 = contenido["resultado"]
                datos_guardados["intermedio"] = resultado1
                esperando_respuesta1 = False
                esperando_respuesta2 = True
                pub.send_string("solicitud/parcial2 " + json.dumps(datos_guardados))
                continue

            if topico == "respuesta/final":
                print("Resultado final recibido:", contenido["total"])
                esperando_respuesta2 = False
                continue

        # TIMEOUT del parcial1
        if esperando_respuesta1:
            print("Servidor parcial1 no respondió. Ejecutando respaldo local...")
            num1 = datos_guardados["num1"]
            num2 = datos_guardados["num2"]
            op1 = datos_guardados["op1"]
            resultado1 = calcular_operacion(num1, num2, op1)
            datos_guardados["intermedio"] = resultado1
            esperando_respuesta1 = False
            esperando_respuesta2 = True
            pub.send_string("solicitud/parcial2 " + json.dumps(datos_guardados))

        # TIMEOUT del parcial2
        elif esperando_respuesta2:
            print("Servidor parcial2 no respondió. Ejecutando respaldo local...")
            intermedio = datos_guardados["intermedio"]
            num3 = datos_guardados["num3"]
            op2 = datos_guardados["op2"]
            resultado_final = calcular_operacion(intermedio, num3, op2)
            print("Resultado final local:", resultado_final)
            esperando_respuesta2 = False

        time.sleep(0.1)

if __name__ == '__main__':
    servidor_calculo_resiliente()

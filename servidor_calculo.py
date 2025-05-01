# ---------- servidor_calculo.py ----------
import zmq
import json
import time

def servidor_calculo():
    context = zmq.Context()
    sub = context.socket(zmq.SUB)
    sub.connect("tcp://10.43.103.197:5556")
    sub.connect("tcp://10.43.103.30:5556")
    sub.setsockopt_string(zmq.SUBSCRIBE, "respuesta/parcial1")
    sub.setsockopt_string(zmq.SUBSCRIBE, "solicitud/calculo_total")

    pub = context.socket(zmq.PUB)
    pub.connect("tcp://10.43.103.197:5555")
    pub.connect("tcp://10.43.103.30:5555")

    datos_guardados = None

    while True:
        try:
            msg = sub.recv_string(flags=zmq.NOBLOCK)
            topico, data = msg.split(" ", 1)
            contenido = json.loads(data)

            if topico == "solicitud/calculo_total":
                datos_guardados = contenido
                pub.send_string("solicitud/parcial1 " + json.dumps(contenido))

            elif topico == "respuesta/parcial1":
                resultado1 = contenido["resultado"]
                datos_guardados["intermedio"] = resultado1
                pub.send_string("solicitud/parcial2 " + json.dumps(datos_guardados))
        except zmq.Again:
            time.sleep(0.1)

if __name__ == '__main__':
    servidor_calculo()

import zmq
import json
import time

def servidor_operacion(nombre):
    context = zmq.Context()
    sub = context.socket(zmq.SUB)
    sub.connect("tcp://10.43.103.197:5556")
    sub.connect("tcp://10.43.103.30:5556")
    sub.setsockopt_string(zmq.SUBSCRIBE, "solicitud/parcial2")

    pub = context.socket(zmq.PUB)
    pub.connect("tcp://10.43.103.197:5555")
    pub.connect("tcp://10.43.103.30:5555")

    while True:
        try:
            msg = sub.recv_string(flags=zmq.NOBLOCK)
            _, data = msg.split(" ", 1)
            contenido = json.loads(data)
            intermedio, num3 = contenido["intermedio"], contenido["num3"]
            op2 = contenido["op2"]

            if op2 == "+":
                res = intermedio + num3
            elif op2 == "-":
                res = intermedio - num3
            elif op2 == "*":
                res = intermedio * num3
            elif op2 == "/":
                res = intermedio / num3 if num3 != 0 else 0
            else:
                res = 0

            print(f"{nombre} resultado final:", res)
            pub.send_string("respuesta/final " + json.dumps({"total": res}))
        except zmq.Again:
            time.sleep(0.1)

if __name__ == '__main__':
    servidor_operacion("ServidorOperación2")

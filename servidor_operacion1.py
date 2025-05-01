# ---------- servidor_operacion1.py ----------
import zmq
import json
import time

def servidor_operacion(nombre):
    context = zmq.Context()
    sub = context.socket(zmq.SUB)
    sub.connect("tcp://10.43.103.197:5556")
    sub.connect("tcp://10.43.103.30:5556")
    sub.setsockopt_string(zmq.SUBSCRIBE, "solicitud/parcial1")

    pub = context.socket(zmq.PUB)
    pub.connect("tcp://10.43.103.197:5555")
    pub.connect("tcp://10.43.103.30:5555")

    while True:
        try:
            msg = sub.recv_string(flags=zmq.NOBLOCK)
            _, data = msg.split(" ", 1)
            contenido = json.loads(data)
            num1, num2 = contenido["num1"], contenido["num2"]
            op1 = contenido["op1"]

            if op1 == "+":
                res = num1 + num2
            elif op1 == "-":
                res = num1 - num2
            elif op1 == "*":
                res = num1 * num2
            elif op1 == "/":
                res = num1 / num2 if num2 != 0 else 0
            else:
                res = 0

            print(f"{nombre} resultado parcial 1:", res)
            pub.send_string("respuesta/parcial1 " + json.dumps({"resultado": res}))
        except zmq.Again:
            time.sleep(0.1)

if __name__ == '__main__':
    servidor_operacion("ServidorOperación1")

import zmq
import time
import json

def client():
    context = zmq.Context()
    pub = context.socket(zmq.PUB)
    pub.connect("tcp://10.43.103.197:5555")  # Broker principal
    pub.connect("tcp://10.43.103.30:5555")   # Broker de respaldo

    sub = context.socket(zmq.SUB)
    sub.connect("tcp://10.43.103.197:5556")
    sub.connect("tcp://10.43.103.30:5556")
    sub.setsockopt_string(zmq.SUBSCRIBE, "respuesta/final")

    time.sleep(2)

    print("Ingrese tres números y dos operaciones (+, -, *, /):")
    num1 = float(input("Número 1: "))
    num2 = float(input("Número 2: "))
    num3 = float(input("Número 3: "))
    op1 = input("Operación 1 (entre num1 y num2): ")
    op2 = input("Operación 2 (entre resultado1 y num3): ")

    solicitud = {
        "num1": num1,
        "num2": num2,
        "num3": num3,
        "op1": op1,
        "op2": op2
    }
    pub.send_string("solicitud/calculo_total " + json.dumps(solicitud))
    print("Cliente: solicitud enviada")

    try:
        sub.setsockopt(zmq.RCVTIMEO, 20000)
        mensaje = sub.recv_string()
        print("Cliente recibió:", mensaje)
    except zmq.Again:
        print("[ERROR] No se recibió respuesta. Posible fallo en red o nodos.")

if __name__ == '__main__':
    client()

import zmq
import time
import threading

def broker():
    context = zmq.Context()
    frontend = context.socket(zmq.XSUB)
    frontend.bind("tcp://10.43.103.197:5555")

    backend = context.socket(zmq.XPUB)
    backend.bind("tcp://10.43.103.197:5556")

    def heartbeat_monitor():
        while True:
            print("[Broker Principal] En funcionamiento - Latidos OK")
            time.sleep(5)

    threading.Thread(target=heartbeat_monitor, daemon=True).start()
    zmq.proxy(frontend, backend)

if __name__ == '__main__':
    broker()






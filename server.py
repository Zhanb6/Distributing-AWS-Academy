import socket
import json
import uuid
import time
from datetime import datetime

HOST = "0.0.0.0"   # listen on all interfaces
PORT = 5000        # must match security group and client config

def add(a, b):
    return a + b

def handle_request(raw_data):
    try:
        req = json.loads(raw_data.decode("utf-8"))
        request_id = req.get("request_id")
        method = req.get("method")
        params = req.get("params", {})

        print(f"[{datetime.utcnow()}] received request_id={request_id}, method={method}, params={params}")

        if method == "add":
            # artificial delay to trigger client timeouts (failure scenario)
            time.sleep(5)
            result = add(params.get("a", 0), params.get("b", 0))
            resp = {
                "request_id": request_id,
                "result": result,
                "status": "OK"
            }
        else:
            resp = {
                "request_id": request_id,
                "result": None,
                "status": "ERROR",
                "error": f"Unknown method {method}"
            }
    except Exception as e:
        resp = {
            "request_id": str(uuid.uuid4()),
            "result": None,
            "status": "ERROR",
            "error": str(e)
        }

    return (json.dumps(resp) + "\n").encode("utf-8")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"RPC server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(4096)
                if not data:
                    continue
                response = handle_request(data)
                conn.sendall(response)

if __name__ == "__main__":
    main()

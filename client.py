import socket
import json
import uuid
from datetime import datetime

SERVER_HOST = "<SERVER_PUBLIC_IP>"   # public IPv4 of rpc-server-node
SERVER_PORT = 5000
TIMEOUT_SECONDS = 2
MAX_RETRIES = 3

def make_request(a, b):
    return {
        "request_id": str(uuid.uuid4()),
        "method": "add",
        "params": {"a": a, "b": b},
        "timestamp": datetime.utcnow().isoformat()
    }

def send_rpc_request(a, b):
    req = make_request(a, b)
    payload = (json.dumps(req) + "\n").encode("utf-8")

    attempt = 0
    while attempt < MAX_RETRIES:
        attempt += 1
        print(f"[{datetime.utcnow()}] attempt {attempt}, request_id={req['request_id']}")

        try:
            with socket.create_connection((SERVER_HOST, SERVER_PORT), timeout=TIMEOUT_SECONDS) as sock:
                sock.sendall(payload)
                sock.settimeout(TIMEOUT_SECONDS)
                data = sock.recv(4096)
                if not data:
                    raise TimeoutError("empty response")
                resp = json.loads(data.decode("utf-8"))
                print("Response:", resp)
                return resp
        except Exception as e:
            print(f"Error on attempt {attempt}: {e}")

    print("Failed to get response after retries")
    return None

if __name__ == "__main__":
    send_rpc_request(5, 7)

import socket
import threading
import json
import base64
import os

LOG_FILE = 'distributor_log.txt'
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

clients = []
log_lock = threading.Lock()

def log_message(message):
    with log_lock:
        with open(LOG_FILE, 'a') as f:
            f.write(message + '\n')

def forward_to_server(request):
    server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_conn.connect((SERVER_HOST, SERVER_PORT))
    server_conn.send(json.dumps(request).encode('utf-8'))
    response = server_conn.recv(1024).decode('utf-8')
    server_conn.close()
    return json.loads(response)

def handle_client(conn, addr):
    try:
        data = conn.recv(1024).decode('utf-8')
        request = json.loads(data)
        if request['action'] == 'authenticate':
            response = forward_to_server(request)
            conn.send(json.dumps(response).encode('utf-8'))
            if response['status'] == 'success':
                clients.append((conn, request['username']))
                broadcast_message(f"{request['username']} has joined the chat.")
                log_message(f"{request['username']} authenticated and joined from {addr}.")
                while True:
                    message = conn.recv(1024).decode('utf-8')
                    if message:
                        decoded_message = base64.b64decode(message.encode('utf-8')).decode('utf-8')
                        broadcast_message(f"{request['username']}: {decoded_message}")
                    else:
                        break
        log_message(f"Client {addr} disconnected.")
    except Exception as e:
        log_message(f"Error handling client {addr}: {str(e)}")
    finally:
        conn.close()
        for client in clients:
            if client[0] == conn:
                clients.remove(client)
                broadcast_message(f"{client[1]} has left the chat.")
                break

def broadcast_message(message):
    encoded_message = base64.b64encode(message.encode('utf-8')).decode('utf-8')
    for client in clients:
        try:
            client[0].send(encoded_message.encode('utf-8'))
        except:
            clients.remove(client)

def start_distributor():
    distributor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    distributor.bind(('0.0.0.0', 23456))
    distributor.listen(5)
    print("Distributor started.")
    log_message("Distributor started.")
    try:
        while True:
            conn, addr = distributor.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    except KeyboardInterrupt:
        print("Shutting down distributor...")
        log_message("Distributor shut down.")
    finally:
        distributor.close()

if __name__ == "__main__":
    start_distributor()

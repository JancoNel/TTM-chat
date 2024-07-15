"""
Server.py
The king of the chatroom

By Janco

https://github.com/JancoNel-dev

"""


import socket
import threading
import json
import base64
import os

ACCOUNTS_FILE = 'accounts.json'
LOG_FILE = 'server_log.txt'

accounts = {}
log_lock = threading.Lock()

def load_accounts():
    global accounts
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as f:
            accounts = json.load(f)
    else:
        accounts = {}

def save_accounts():
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(accounts, f)

def log_message(message):
    with log_lock:
        with open(LOG_FILE, 'a') as f:
            f.write(message + '\n')

def handle_client(conn, addr):
    try:
        data = conn.recv(1024).decode('utf-8')
        request = json.loads(data)
        if request['action'] == 'authenticate':
            username = request['username']
            password = request['password']
            response = {'status': 'fail'}
            if username in accounts and accounts[username] == password:
                response['status'] = 'success'
            conn.send(json.dumps(response).encode('utf-8'))
            log_message(f"Authentication attempt from {addr}: {response['status']}")
    except Exception as e:
        log_message(f"Error handling client {addr}: {str(e)}")
    finally:
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    load_accounts()
    print("Server started.")
    log_message("Server started.")
    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    except KeyboardInterrupt:
        print("Shutting down server...")
        log_message("Server shut down.")
    finally:
        server.close()
        save_accounts()

def create_account(username, password):
    accounts[username] = password
    save_accounts()
    log_message(f"Account created: {username}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3 and sys.argv[1] == 'create_account':
        create_account(sys.argv[2], sys.argv[3])
    else:
        start_server()

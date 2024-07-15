import socket
import threading
import json
import base64
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

DISTRIBUTOR_HOST = '127.0.0.1'
DISTRIBUTOR_PORT = 23456

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatroom")
        self.twilight_theme()
        self.login_screen()

    def twilight_theme(self):
        self.bg_color = '#2E3440'
        self.text_color = '#D8DEE9'
        self.entry_bg = '#4C566A'
        self.entry_fg = '#D8DEE9'
        self.button_bg = '#5E81AC'
        self.button_fg = '#D8DEE9'

        self.root.configure(bg=self.bg_color)

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Username:", bg=self.bg_color, fg=self.text_color).grid(row=0, column=0)
        self.username_entry = tk.Entry(self.root, bg=self.entry_bg, fg=self.entry_fg)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Password:", bg=self.bg_color, fg=self.text_color).grid(row=1, column=0)
        self.password_entry = tk.Entry(self.root, show="*", bg=self.entry_bg, fg=self.entry_fg)
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Login", command=self.login, bg=self.button_bg, fg=self.button_fg).grid(row=2, column=0, columnspan=2)

    def chat_screen(self):
        self.clear_screen()
        self.chat_box = scrolledtext.ScrolledText(self.root, state='disabled', bg=self.entry_bg, fg=self.text_color)
        self.chat_box.grid(row=0, column=0, columnspan=2)
        self.message_entry = tk.Entry(self.root, bg=self.entry_bg, fg=self.entry_fg)
        self.message_entry.grid(row=1, column=0)
        self.message_entry.bind("<Return>", self.send_message_event)
        tk.Button(self.root, text="Send", command=self.send_message, bg=self.button_bg, fg=self.button_fg).grid(row=1, column=1)

        threading.Thread(target=self.receive_messages).start()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((DISTRIBUTOR_HOST, DISTRIBUTOR_PORT))
        request = {'action': 'authenticate', 'username': username, 'password': password}
        self.conn.send(json.dumps(request).encode('utf-8'))
        response = json.loads(self.conn.recv(1024).decode('utf-8'))
        if response['status'] == 'success':
            self.username = username
            self.chat_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def send_message(self):
        message = self.message_entry.get()
        if message:
            encoded_message = base64.b64encode(message.encode('utf-8')).decode('utf-8')
            self.conn.send(encoded_message.encode('utf-8'))
            self.message_entry.delete(0, tk.END)

    def send_message_event(self, event):
        self.send_message()

    def receive_messages(self):
        while True:
            try:
                message = self.conn.recv(1024).decode('utf-8')
                if message:
                    decoded_message = base64.b64decode(message.encode('utf-8')).decode('utf-8')
                    self.chat_box.configure(state='normal')
                    self.chat_box.insert(tk.END, decoded_message + '\n')
                    self.chat_box.configure(state='disabled')
                    self.chat_box.yview(tk.END)
                else:
                    break
            except:
                break

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()

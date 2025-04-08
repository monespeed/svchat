import socket
import threading
import time
import os
import json
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

class ChatServer:
    def __init__(self):
        self.HOST = '0.0.0.0'
        self.PORT = 9090
        self.FILE_PORT = 9091
        self.clients = {}
        self.MAX_FILE_SIZE = 100 * 1024 * 1024 * 1024  # 100 GB
        self.TEMP_DIR = "server_files"
        self.message_queue = Queue()
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.server_socket = None
        self.file_socket = None
        self.running = False

    def ensure_temp_dir(self):
        Path(self.TEMP_DIR).mkdir(exist_ok=True)

    def broadcast(self, message, sender_socket=None):
        """Асинхронная рассылка сообщений с использованием пула потоков"""
        def send_to_client(client, msg):
            try:
                client.send(msg)
            except:
                client.close()
                if client in self.clients:
                    del self.clients[client]

        for client in list(self.clients.keys()):
            if client != sender_socket:
                self.executor.submit(send_to_client, client, message)

    # ... (остальные методы класса остаются аналогичными, но с оптимизациями)

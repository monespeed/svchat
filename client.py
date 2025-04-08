import socket
import threading
import os
import json
import time
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

class ChatClient:
    def __init__(self):
        self.host = input("IP сервера: ")
        self.port = 9090
        self.file_port = 9091
        self.nickname = input("Ваш ник: ")
        self.client = None
        self.file_client = None
        self.running = False
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.download_dir = "downloads"
        self.ensure_download_dir()

    def ensure_download_dir(self):
        Path(self.download_dir).mkdir(exist_ok=True)

    # ... (другие методы с оптимизациями)

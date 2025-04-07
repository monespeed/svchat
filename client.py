import socket
import threading

HOST = input("IP сервера: ")
PORT = 9090

nickname = input("Ваш ник: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Ошибка соединения...")
            client.close()
            break

def write():
    while True:
        msg = input()
        client.send(msg.encode('utf-8'))
        if msg == '/exit':
            break

client.send(nickname.encode('utf-8'))

threading.Thread(target=receive).start()
threading.Thread(target=write).start()

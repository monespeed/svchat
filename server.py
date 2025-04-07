import socket
import threading
import time

HOST = '0.0.0.0'
PORT = 9090
clients = {}

def broadcast(message, sender_socket=None):
    for client, nickname in clients.items():
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                del clients[client]

def handle_client(client_socket):
    nickname = client_socket.recv(1024).decode('utf-8')
    clients[client_socket] = nickname
    print(f"[+] {nickname} подключился.")

    broadcast(f"*** {nickname} вошёл в чат ***".encode('utf-8'))

    while True:
        try:
            msg = client_socket.recv(1024)
            if msg.decode('utf-8') == '/exit':
                client_socket.send('Вы покинули чат.'.encode('utf-8'))
                client_socket.close()
                broadcast(f"*** {nickname} вышел из чата ***".encode('utf-8'))
                del clients[client_socket]
                break
            elif msg.decode('utf-8') == '/users':
                online = ', '.join(clients.values())
                client_socket.send(f"Сейчас в чате: {online}".encode('utf-8'))
            elif msg.decode('utf-8') == '/help':
                help_text = "/users — кто онлайн\n/exit — выйти\n/help — помощь"
                client_socket.send(help_text.encode('utf-8'))
            else:
                timestamp = time.strftime("[%H:%M:%S]", time.localtime())
                full_msg = f"{timestamp} {nickname}: {msg.decode('utf-8')}"
                print(full_msg)
                broadcast(full_msg.encode('utf-8'), sender_socket=client_socket)
        except:
            client_socket.close()
            del clients[client_socket]
            break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        client_socket.send("Введите ваш ник: ".encode('utf-8'))
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    main()

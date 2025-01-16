import socket
import threading

clients = []

def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    clients.append(client_socket)
    
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Received from {client_address}: {message}")
            broadcast(message, client_socket)
    except Exception as e:
        print(f"[ERROR] {client_address}: {e}")
    finally:
        print(f"[DISCONNECT] {client_address} disconnected.")
        clients.remove(client_socket)
        client_socket.close()

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(f"[Broadcast] {message}".encode('utf-8'))
            except Exception as e:
                print(f"[ERROR] Failed to send to client: {e}")
                clients.remove(client)
                client.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0' # why no work
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[STARTED] Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    main()

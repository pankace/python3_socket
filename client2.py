import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                print(f"\nServer: {data.decode('utf-8')}\nEnter your message: ", end="")
            else:
                break
        except:
            print("Disconnected from server.")
            break

def send_messages(client_socket):
    while True:
        try:
            message = input("Enter your message: ")
            if message.lower() == "exit":
                client_socket.close()
                break
            client_socket.sendall(message.encode('utf-8'))
        except:
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '10.237.1.149'  
    port = 1234
    client_socket.connect((host, port))
    print("Connected to the server.")

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    send_messages(client_socket)

if __name__ == "__main__":
    main()

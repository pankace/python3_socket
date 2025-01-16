import socket
import threading

HOST = '10.237.1.149'  # Server IP
PORT = 21002           # Server Port
MESSAGE_COUNT = 10000   # Number of messages to send

def send_messages_fast(client_socket):
    try:
        for i in range(MESSAGE_COUNT):
            message = f"Message {i+1}"
            client_socket.sendall((message + "\n").encode())
            print(f"Sent: {message}")
    except Exception as e:
        print(f"Error while sending: {e}")
    finally:
        client_socket.close()
        print("Finished sending messages.")

def receive_messages(client_socket):
    buffer = ""
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("Server closed the connection.")
                break

            buffer += data.decode()
            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                print(f"Received: {message}")
        except Exception as e:
            print(f"Error while receiving: {e}")
            break

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"Connected to server at {HOST}:{PORT}")

            threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

            send_messages_fast(s)

    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    main()



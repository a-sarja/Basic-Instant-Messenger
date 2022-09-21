import socket
import argparse
from _thread import *

host = "127.0.0.1"  # Server IP
port = 1234  # Server Port


def print_server_response(client_socket):
    response = client_socket.recv(2048).decode()
    print(response)
    return response


def create_client_server(my_port):

    client_socket2 = socket.socket()
    client_socket2.bind(("127.0.0.1", my_port + 1))
    client_socket2.listen()
    conn, address = client_socket2.accept()
    print("\n[CLIENT-SERVER-DEBUG] Connected to " + str(address[0]) + ":" + str(address[1]))

    template = "<FROM " + str(address[0]) + ":" + str(address[1]) + ">"

    while True:
        message_data = conn.recv(2048).decode()
        if message_data:
            print(template + str(message_data) + "\n")


def client_program(user_name):
    welcome_message = True
    client_socket = socket.socket()

    client_socket.connect((host, port))

    # Send client's username to the server
    client_socket.send(user_name.encode())

    # Trying this out - to accept any new connections from other clients
    my_hostmame = client_socket.getsockname()
    my_port = my_hostmame[1]
    print("[CLIENT DEBUG]" + str(my_hostmame) + " " + str(my_port) + " " + str(type(my_port)))
    # client_socket.bind(('0.0.0.0', my_port))
    start_new_thread(create_client_server, (my_port, ))

    while True:

        if welcome_message:
            # Read and print welcome message
            print_server_response(client_socket)
            welcome_message = False

        message = input(user_name + "> ")
        if not message:
            continue

        if message.lower().strip() == "bye":
            break

        if message.lower().strip() == "list":
            client_socket.send(message.encode())
            print_server_response(client_socket)

        if message.lower().startswith("send"):
            dest_username = message.split(" ")[1]
            dest_message = message.split(" ")[2]
            message = "send " + dest_username

            client_socket.send(message.encode())
            dest_ip_port = print_server_response(client_socket)

            dest_ip, dest_port = dest_ip_port.split(":")
            print("[CLIENT DEBUG]" + dest_ip + " -:- " + dest_port)
            dest_port = int(dest_port)
            print("[CLIENT DEBUG]" + str(dest_port))

            client_socket.close()

            client_socket = socket.socket()
            client_socket.connect(("127.0.0.1", dest_port + 1))
            client_socket.send(dest_message.encode())

    client_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", type=str, required=True, help="Username must be specified")
    args = parser.parse_args()

    username = args.username

    client_program(user_name=username)

    print("Client terminated..")

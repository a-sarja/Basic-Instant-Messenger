import socket
from _thread import *

host = "127.0.0.1"
port = 1234
clients_list = {}  # This will be a dictionary with username as Key and IP:PORT will be the value


def get_connected_clients():
    return " ".join(clients_list.keys())


def get_ip_port_info(username):

    if username in clients_list:
        return clients_list[username]

    return None


def client_handler(connection, username):

    while True:
        response = "server>"

        message_data = connection.recv(2048).decode()
        if message_data.lower().strip() == "bye":
            del clients_list[username]
            break

        if message_data.lower().strip() == "list":
            response = "server>" + get_connected_clients()

        if message_data.lower().split(" ")[0] == "send":  # the syntax would be `send <username>`
            destination_username = message_data.split()[1]
            response = "server>" + get_ip_port_info(destination_username)

        # connection.sendall(response.encode())
        connection.send(response.encode())

    connection.close()


def accept_connections(server_socket):
    client, address = server_socket.accept()
    print("[DEBUG] Connected to " + str(address[0]) + ":" + str(address[1]))

    welcome_message = "<Server> Welcome to CY6740 Chatroom!\n"
    client.sendall(welcome_message.encode())

    # Capture the username and add the info to the clients_list before spawning a new thread
    username = client.recv(2048).decode()
    clients_list[username] = str(address[0]) + ":" + str(address[1])

    start_new_thread(client_handler, (client, username, ))


def start_server(server_host, server_port):
    server_socket = socket.socket()
    server_socket.bind((server_host, server_port))
    server_socket.listen()
    print("Server Initialized... Server is left running ")

    while True:
        accept_connections(server_socket)


if __name__ == "__main__":
    start_server(server_host=host, server_port=port)

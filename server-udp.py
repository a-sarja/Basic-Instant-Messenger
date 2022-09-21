import socket
import argparse


class my_server:

    def __init__(self, server_host, server_port):
        self.host = server_host
        self.port = server_port
        self.clients_list = {}
        self.server_socket = None

    def initialise_server_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))

    def add_user_to_clients_list(self, username, address_information):
        complete_url = str(address_information[0]) + ":" + str(address_information[1])
        self.clients_list[username] = complete_url

    def fetch_available_clients(self):
        return str(self.clients_list)

    def remove_user_from_list(self, username):
        del self.clients_list[username]

    def process_connections(self):

        while True:
            response_message = ""
            address = self.server_socket.recvfrom(2048)
            message = address[0].decode()
            message_source = address[1]
            print("<SERVER-DEBUG> " + str(message_source) + " > " + str(message))

            if message.lower().strip().startswith("signin"):  # signin request must be of this format - signin username
                response_message = "Welcome to CY6740 Chat Room!"
                temp_username = message.split(" ")[1]
                self.add_user_to_clients_list(temp_username, message_source)
            elif message.lower().strip() == "list":
                response_message = "LIST" + self.fetch_available_clients()
            elif message.lower().strip().startswith("bye"):
                temp_username = message.split(" ")[1]
                self.remove_user_from_list(username=temp_username)
            else:
                continue

            self.server_socket.sendto(response_message.encode(), message_source)

    def start_server(self):
        self.initialise_server_socket()
        print("Server Initialized.. Server is left running..")

        while True:
            self.process_connections()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-sp", "--serverport", type=int, required=True, help="Server's Port number is missing.")
    args = parser.parse_args()

    # Reading values from the arguments
    s_port = args.serverport

    server = my_server(server_host="127.0.0.1", server_port=s_port)
    server.start_server()

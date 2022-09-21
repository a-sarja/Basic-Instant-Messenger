import json
import socket
import argparse
import select
import sys


def read_input():
    i, o, e = select.select([sys.stdin], [], [], 1)
    for s in i:
        if s == sys.stdin:
            input_text = sys.stdin.readline()
            return input_text

    return False


class client:

    def __init__(self, server_info, user_name):
        self.client_socket = None
        self.server_info = server_info
        self.username = user_name
        self.clients_info = {}
        self.my_ip = ""
        self.my_port = 0

    def initialise_client_socket(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_socket.setblocking(False)
        self.client_socket = client_socket

    def client_signin(self):
        signin_message = "SIGNIN " + self.username
        self.client_socket.sendto(signin_message.encode(), self.server_info)

    def print_available_clients(self):
        result = ""
        for key, value in self.clients_info.items():
            result += str(key) + "; "

        print("Signed In Users - " + result)

    def client_processing(self):
        # Set up the client socket and make a signin request to the server
        self.initialise_client_socket()
        self.client_signin()

        # Collecting information about the IP and PORT Numbers where this process is running
        my_host_address = self.client_socket.getsockname()
        self.my_ip = my_host_address[0]
        self.my_port = my_host_address[1]

        while True:
            target_node = self.server_info  # The target node will be the server by default
            try:
                remote_message, remote_addr = self.client_socket.recvfrom(2048)

                if remote_message:  # messages from remote nodes will be displayed based on some conditions
                    if not remote_message.decode().strip().startswith("LIST"):
                        print(str(remote_message.decode()))
                    elif remote_message.decode().strip().startswith("LIST"):
                        temp = remote_message.decode().replace("LIST", "").replace("'", '"')
                        self.clients_info = json.loads(temp)
                        self.print_available_clients()

            except socket.error:
                pass

            user_input = read_input()
            if user_input:

                if user_input.lower().strip() == "bye":  # bye command should terminate the entire client application - sending sign-out request to server upon executing bye
                    bye_msg = "bye " + self.username
                    self.client_socket.sendto(bye_msg.encode(), target_node)
                    break

                if user_input.lower().strip().startswith("send"):
                    target_client_username = user_input.strip().split(" ")[1]
                    if target_client_username not in self.clients_info:
                        print("[CLIENT-ERROR] Target Client username not found!")
                        continue

                    temp = self.clients_info[target_client_username]
                    target_node = (temp.split(":")[0], int(temp.split(":")[1]))
                    user_input = user_input.strip().replace("send", "").replace("SEND", "").replace(str(target_client_username), "")  # Replace the first two words in the Send command so that only message reaches the client

                if target_node != self.server_info:
                    user_input = "<FROM [" + self.my_ip + "]:[" + str(self.my_port) + "]:" + self.username + "> " + user_input  # Format the outgoing messages only if they are not going to the server. Server must receive the exact user inputs - not formatted text

                self.client_socket.sendto(user_input.encode(), target_node)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", type=str, required=True, help="Username is required. It is the unique name that you identify yourself with.")
    parser.add_argument("-sip", "--serverip", type=str, required=True, help="Server IP is required. Please reach out to system admin if you do not know the Server IP Address.")
    parser.add_argument("-sp", "--serverport", type=int, required=True, help="Server's Port number is missing.")
    args = parser.parse_args()

    # Reading values from the arguments
    username = args.username
    server_ip = args.serverip
    server_port = args.serverport

    client = client(server_info=(server_ip, server_port), user_name=username)
    client.client_processing()

    print("Client terminated..")

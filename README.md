
# Basic Chat Application

    A basic chat application written in Python where clients can connect to the server by sending SIGNIN request.
    
    Once connected, they can chat with the other available connected clients in real time.

### Author Information 

- Abhiram Sarja 
- sarja.a@northeastern.edu
- 002116883 (NUID)

### Requirements

- Python 3.10 or later
- Pip 22.0.2 or later (Installed from python 3)
- Packages - argparse, json, select and socket

### Running Instructions

Run the server using the following command:

```
./server.py -sp <port_number>
```

Run the clients using the following command:

```
./client.py -u <user_name> -sip <server_ip> -sp <port_number>
```

Commands available to the clients:

```text
SIGNIN <user-name>

LIST

SEND <target-username> MESSAGE
```
### Assumptions

- `LIST` command stores the online clients information locally on the client. Hence, before making any new `send` request, we should call ``LIST`` to fetch the latest information

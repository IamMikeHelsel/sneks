import socket
import pickle
import struct
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HEADER_LENGTH = 4  # 4 bytes for message length (unsigned int)

def send_message(sock, message):
    """
    Pickles a message, prepends its length, and sends it.
    Returns True on success, False on failure.
    """
    try:
        pickled_data = pickle.dumps(message)
        message_length = len(pickled_data)
        header = struct.pack('>I', message_length)
        sock.sendall(header + pickled_data)
        return True
    except socket.error as e:
        logging.error(f"Socket error while sending: {e} on {sock.getsockname() if sock.fileno() != -1 else 'closed socket'}")
        return False
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return False

def receive_message(sock, recv_buffer_map, client_ident):
    """
    Receives a length-prefixed message from the socket.
    Manages a buffer for partial receives.
    Returns the unpickled message, or None if no complete message is received yet,
    or False if an error/disconnection occurs.
    `client_ident` is used for logging and buffer management.
    `recv_buffer_map` is a dictionary {client_ident: b''} to store buffer per client.
    """
    if client_ident not in recv_buffer_map:
        recv_buffer_map[client_ident] = b''
    
    buffer = recv_buffer_map[client_ident]

    try:
        # 1. Try to read the header if not fully received yet
        if len(buffer) < HEADER_LENGTH:
            bytes_needed = HEADER_LENGTH - len(buffer)
            chunk = sock.recv(bytes_needed)
            if not chunk:
                logging.info(f"Client {client_ident} disconnected (header recv).")
                return False  # Connection closed
            buffer += chunk
            if len(buffer) < HEADER_LENGTH:
                recv_buffer_map[client_ident] = buffer
                return None  # Still waiting for full header

        msg_len = struct.unpack('>I', buffer[:HEADER_LENGTH])[0]
        
        # 2. Try to read the message body if not fully received yet
        if len(buffer) < HEADER_LENGTH + msg_len:
            bytes_needed = HEADER_LENGTH + msg_len - len(buffer)
            chunk = sock.recv(bytes_needed)
            if not chunk:
                logging.info(f"Client {client_ident} disconnected (body recv).")
                # Potentially an incomplete message, might need cleanup or error reporting
                return False # Connection closed
            buffer += chunk
            if len(buffer) < HEADER_LENGTH + msg_len:
                recv_buffer_map[client_ident] = buffer
                return None # Still waiting for full message body

        # Message fully received
        pickled_msg = buffer[HEADER_LENGTH : HEADER_LENGTH + msg_len]
        message = pickle.loads(pickled_msg)
        
        # Update buffer with any excess data
        recv_buffer_map[client_ident] = buffer[HEADER_LENGTH + msg_len:]
        return message

    except BlockingIOError:
        recv_buffer_map[client_ident] = buffer # Save progress
        return None  # No data available right now
    except (socket.error, struct.error, pickle.UnpicklingError) as e:
        logging.error(f"Error receiving/processing message from {client_ident}: {e}")
        return False # Indicate an error or disconnection
    except Exception as e:
        logging.error(f"Unexpected error receiving message from {client_ident}: {e}")
        return False


class Server:
    def __init__(self, host, port, max_clients=1):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        self.socket.bind((host, port))
        self.socket.listen(max_clients + 1) # Listen for a bit more than max_clients
        self.clients = {}  # {client_socket: {'addr': address, 'id': client_id_str}}
        self.client_recv_buffers = {} # {client_id_str: b''}
        self.client_id_counter = 0
        logging.info(f"Server initialized on {host}:{port}, max_clients={max_clients}")

    def accept_connections(self):
        newly_connected_ids = []
        if len(self.clients) >= self.max_clients:
            return newly_connected_ids

        try:
            while len(self.clients) < self.max_clients:
                conn, addr = self.socket.accept()
                conn.setblocking(False)
                client_id = f"client_{self.client_id_counter}"
                self.client_id_counter += 1
                self.clients[conn] = {'addr': addr, 'id': client_id}
                self.client_recv_buffers[client_id] = b'' # Initialize buffer for new client
                newly_connected_ids.append(client_id)
                logging.info(f"Accepted connection from {addr} as {client_id}")
        except BlockingIOError:
            pass  # No new connections waiting
        except Exception as e:
            logging.error(f"Error accepting connections: {e}")
        return newly_connected_ids

    def receive_data(self):
        received_messages = []
        clients_to_remove = []

        for client_sock, client_info in list(self.clients.items()): # list() for safe removal
            client_id = client_info['id']
            message = receive_message(client_sock, self.client_recv_buffers, client_id)

            if message is False:  # Error or disconnection
                clients_to_remove.append(client_sock)
                logging.info(f"Client {client_id} ({client_info['addr']}) marked for removal.")
            elif message is not None: # Successfully received a complete message
                received_messages.append((client_id, message))
                logging.debug(f"Received from {client_id}: {message}")
        
        for sock in clients_to_remove:
            client_info = self.clients.pop(sock, None)
            if client_info:
                del self.client_recv_buffers[client_info['id']]
                logging.info(f"Removed client {client_info['id']} ({client_info['addr']}).")
            try:
                sock.close()
            except socket.error as e:
                logging.error(f"Error closing socket for removed client: {e}")
        
        return received_messages

    def broadcast_data(self, data):
        clients_to_remove = []
        if not self.clients:
            # logging.info("Broadcast: No clients connected.") # Can be noisy
            return

        logging.debug(f"Broadcasting data: {data}")
        for client_sock, client_info in list(self.clients.items()):
            if not send_message(client_sock, data):
                logging.warning(f"Failed to send data to {client_info['id']}. Marking for removal.")
                clients_to_remove.append(client_sock)
        
        for sock in clients_to_remove:
            client_info = self.clients.pop(sock, None)
            if client_info:
                del self.client_recv_buffers[client_info['id']]
                logging.info(f"Removed client {client_info['id']} due to send failure.")
            try:
                sock.close()
            except socket.error as e:
                logging.error(f"Error closing socket for client removed during broadcast: {e}")

    def send_to_client(self, client_id, data):
        """ Sends data to a specific client by client_id. """
        target_socket = None
        for sock, info in self.clients.items():
            if info['id'] == client_id:
                target_socket = sock
                break
        
        if target_socket:
            if not send_message(target_socket, data):
                logging.warning(f"Failed to send data to specific client {client_id}. Removing.")
                # Perform removal similar to broadcast_data
                client_info = self.clients.pop(target_socket, None)
                if client_info:
                    del self.client_recv_buffers[client_info['id']]
                    logging.info(f"Removed client {client_info['id']} due to specific send failure.")
                try:
                    target_socket.close()
                except socket.error as e:
                    logging.error(f"Error closing socket for {client_id} after send failure: {e}")
                return False
            return True
        else:
            logging.warning(f"Client {client_id} not found for sending data.")
            return False

    def close(self):
        logging.info("Closing server...")
        for client_sock, client_info in list(self.clients.items()):
            logging.info(f"Closing connection to {client_info['id']} ({client_info['addr']})")
            try:
                client_sock.close()
            except socket.error as e:
                logging.error(f"Error closing client socket {client_info['id']}: {e}")
        self.clients.clear()
        self.client_recv_buffers.clear()
        try:
            self.socket.close()
        except socket.error as e:
            logging.error(f"Error closing server socket: {e}")
        logging.info("Server closed.")


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_buffer = { 'client_socket': b'' } # Use a map for receive_message compatibility
        self.connected = False
        logging.info(f"Client initialized for {host}:{port}")

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            self.socket.setblocking(False)
            self.connected = True
            logging.info(f"Successfully connected to server {self.host}:{self.port}")
            return True
        except socket.error as e:
            # For non-blocking, connect() might raise an error immediately.
            # WSAEWOULDBLOCK (Windows) or EINPROGRESS (Linux) indicates connection is in progress.
            # However, the prompt asked to set non-blocking *after* connection.
            # So, a direct connect fail here is a genuine error.
            logging.error(f"Failed to connect to server {self.host}:{self.port}: {e}")
            self.connected = False
            return False
        except Exception as e:
            logging.error(f"Unexpected error during connect: {e}")
            self.connected = False
            return False


    def send_data(self, data):
        if not self.connected:
            logging.warning("Client not connected. Cannot send data.")
            return False
        logging.debug(f"Client sending data: {data}")
        if not send_message(self.socket, data):
            self.connected = False # Assume disconnection on send failure
            logging.error("Failed to send data. Disconnecting client.")
            return False
        return True

    def receive_data(self):
        if not self.connected:
            # logging.warning("Client not connected. Cannot receive data.") # Can be noisy
            return None 

        message = receive_message(self.socket, self.recv_buffer, 'client_socket')
        
        if message is False: # Error or disconnection
            logging.info("Disconnected from server or error receiving data.")
            self.connected = False
            self.close() # Clean up socket
            return False # Indicate disconnection
        
        if message is not None:
            logging.debug(f"Client received data: {message}")
        
        return message # Returns message or None if still waiting

    def close(self):
        logging.info("Closing client connection...")
        self.connected = False
        try:
            self.socket.close()
        except socket.error as e:
            logging.error(f"Error closing client socket: {e}")
        logging.info("Client connection closed.")

if __name__ == '__main__':
    # Example Usage (for testing purposes, can be removed later)
    import time

    # Server Test
    def server_test():
        server = Server("localhost", 12345, max_clients=1)
        last_broadcast_time = time.time()
        try:
            while True:
                server.accept_connections()
                received = server.receive_data()
                for client_id, data in received:
                    print(f"[Server] Received from {client_id}: {data}")
                    if data == "ping":
                        server.send_to_client(client_id, "pong")
                
                if time.time() - last_broadcast_time > 5:
                    server.broadcast_data({"timestamp": time.time(), "message": "Server heartbeat"})
                    last_broadcast_time = time.time()
                
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("[Server] Shutting down...")
        finally:
            server.close()

    # Client Test
    def client_test():
        client = Client("localhost", 12345)
        if not client.connect():
            print("[Client] Could not connect.")
            return

        try:
            client.send_data("ping")
            for _ in range(20): # Try receiving for a few seconds
                data = client.receive_data()
                if data is False: # Disconnected
                    print("[Client] Disconnected by server or error.")
                    break
                if data:
                    print(f"[Client] Received: {data}")
                    if isinstance(data, dict) and "message" in data and data["message"] == "Server heartbeat":
                        print("[Client] Heartbeat received. Sending another ping.")
                        client.send_data("ping_response")
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("[Client] Shutting down...")
        finally:
            client.close()

    print("Running network tests. Start server_test in one terminal and client_test in another.")
    # To run:
    # Terminal 1: python snake_game/core/network.py server
    # Terminal 2: python snake_game/core/network.py client
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == 'server':
            server_test()
        elif sys.argv[1] == 'client':
            client_test()
    else:
        print("Add 'server' or 'client' as argument to run tests.")

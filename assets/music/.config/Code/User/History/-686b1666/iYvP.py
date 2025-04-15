import socket
import threading

def start_server(server_ip="0.0.0.0", server_port=7500, client_port=7501):
    """Start the UDP server."""
    buffer_size = 1024

    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, server_port))

    print(f"Server listening on {server_ip}:{server_port}")

    while True:
        # Receive data from the client
        data, client_address = server_socket.recvfrom(buffer_size)
        message = data.decode('utf-8')
        print(f"Received from client: {message}")

        if message == "202":
            # Start signal, no need to handle equip ID
            response = "202"
        else:
            # Assume the message is an equipment ID
            response = f"ACK:{message}"

        # Send the response back to the client
        server_socket.sendto(response.encode('utf-8'), (client_address[0], client_port))
        print(f"Sent response to client: {response}")

# Example usage
if __name__ == "__main__":
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Keep the main thread alive to keep the server running
    server_thread.join()

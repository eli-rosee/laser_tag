import socket
import threading
import time

msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 7501)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])

print(msg)

    def send_start_signal(self):
        """Send the start signal ("202") to the game software."""
        message = "202".encode()
        self.broadcast_socket.sendto(message, self.serverAddressPort)
        print("Sent start signal: 202")

    def equipID(self, equip_id):
        """Send the equipment ID to the server."""
        message = equip_id.encode()
        self.broadcast_socket.sendto(message, self.serverAddressPort)
        print(f"{equip_id}")

    def listen_for_responses(self):
        """Continuously listen for incoming data on the receive socket."""
        while self._running:
            try:
                data, _ = self.receive_socket.recvfrom(1024)
                message = data.decode('utf-8')
                print(f"Received from game software: {message}")
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error receiving data: {e}")
                break

    def close(self):
        """Close both UDP sockets and stop the receive thread."""
        self._running = False
        self.broadcast_socket.close()
        self.receive_socket.close()
        print("Photon network connections closed.")

# Example usage
if __name__ == "__main__":
    # Start the client
    server_ip = input("Enter server IP (default is 127.0.0.1): ") or "127.0.0.1"
    photon_network = PhotonNetwork(server_ip=server_ip)

    try:
        # Send the start signal to the game software
        photon_network.send_start_signal()
        time.sleep(1)  # Wait for the game software to be ready

    except KeyboardInterrupt:
        photon_network.close()
        print("Photon network terminated.")

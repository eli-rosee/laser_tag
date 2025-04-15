from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QApplication
from PyQt6.QtCore import QTimer, Qt
import sys
import random
import socket
import threading
import time

#run server then client
#works w/ player_entry_screen
class PhotonNetwork:
    def __init__(self, server_ip="127.0.0.1", server_port=7500, client_ip="127.0.0.1", client_port=7501):
        self.server_ip = server_ip  
        self.server_port = server_port
        self.client_ip = client_ip
        self.client_port = client_port
        
        self.serverAddressPort = (server_ip, server_port)
        self.clientAddressPort = (client_ip, client_port)

        # Set up the broadcast socket
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.broadcast_socket.bind((self.client_ip, self.client_port))

        # Set up the receive socket
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.bind(self.clientAddressPort)
        self.receive_socket.settimeout(1.0)  # 1-second timeout

        # Thread control
        self._running = True
        self.receive_thread = threading.Thread(target=self.listen_for_responses, daemon=True)
        self.receive_thread.start()

    def send_start_signal(self):
        """Send the start signal ("202") to the game software."""
        message = "202".encode()
        self.broadcast_socket.sendto(message, self.serverAddressPort)
        #print("202")

    def equipID(self, equip_id):
        """Send the equipment ID to the server."""
        message = equip_id.encode()
        self.broadcast_socket.sendto(message, self.serverAddressPort)        


    def listen_for_responses(self):
        """Continuously listen for incoming data on the receive socket."""
        while self._running:
            try:
                data, _ = self.receive_socket.recvfrom(1024)
                message = data.decode('utf-8')
                print(f"{message}")
                if message == "202":
                    # self.getPlayers()
                    pass
                
            except socket.timeout:
                continue
            except Exception as e:
                print(f"{e}")
                break

    def close(self):
        """Close both UDP sockets and stop the receive thread."""
        self._running = False
        self.broadcast_socket.close()
        self.receive_socket.close()
        print("Photon network connections closed.")

    def update_ip(self, new_ip):
        self.server_ip = new_ip.strip()
        self.serverAddressPort = (self.server_ip, self.server_port)

        self._running = False  # Stop receive thread

        def safe_close(sock):
            if sock:
                try:
                    sock.shutdown(socket.SHUT_RDWR)  
                except OSError:
                    pass  
                sock.close()

        safe_close(self.receive_socket)
        safe_close(self.broadcast_socket)

        time.sleep(1)

        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.receive_socket.bind(self.clientAddressPort)
        self.receive_socket.settimeout(1.0)

        self._running = True
        self.receive_thread = threading.Thread(target=self.listen_for_responses, daemon=True)
        self.receive_thread.start()
        

class PlayActionScreen(QWidget):
    def __init__(self, red_players, green_players, photon_network, player_entry_screen_instance, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Play Action Screen")
        self.showMaximized()
        self.setStyleSheet("background-color: black; color: white;")

        # Store players with their equipment IDs
        self.red_players = red_players
        self.green_players = green_players
        self.photon_network = photon_network
        self.player_entry_screen = player_entry_screen_instance 

        self.red_player_labels = {}
        self.green_player_labels = {}

        main_layout = QHBoxLayout()

        # Red team layout
        red_team_layout = QVBoxLayout()
        red_team_label = QLabel("RED TEAM")
        red_team_label.setStyleSheet("font-size: 20px; font-weight: bold; color: red;")
        red_team_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        red_team_layout.addWidget(red_team_label)

        # Add Red Team players
        for player_id, player_name, equip_id in red_players:
            player_label = QLabel(f"{player_id} - {player_name} (Equipment: {equip_id})")
            player_label.setStyleSheet("font-size: 16px; color: white;")
            player_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)  
            red_team_layout.addWidget(player_label)

            self.red_player_labels[f'{player_id}'] = player_label
            print(self.red_players)


        main_layout.addLayout(red_team_layout, stretch=1)

        current_action_layout = QVBoxLayout()

        # Game timer display
        self.game_timer_label = QLabel("06:00")
        self.game_timer_label.setStyleSheet("font-size: 40px; font-weight: bold; color: yellow;")
        self.game_timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_action_layout.addWidget(self.game_timer_label)

        current_action_label = QLabel("Current Game Action")
        current_action_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        current_action_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_action_layout.addWidget(current_action_label)

        self.current_action_text = QTextEdit()
        self.current_action_text.setReadOnly(True)
        self.current_action_text.setStyleSheet("background-color: black; color: lime; font-size: 16px;")
        self.current_action_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_action_layout.addWidget(self.current_action_text, stretch=1)

        return_button = QPushButton("Return to Player Entry Screen")
        return_button.setStyleSheet("background-color: white; color: black;")
        return_button.clicked.connect(self.return_to_entry_screen)
        current_action_layout.addWidget(return_button)

        main_layout.addLayout(current_action_layout, stretch=1)

        # Green team layout
        green_team_layout = QVBoxLayout()
        green_team_label = QLabel("GREEN TEAM")
        green_team_label.setStyleSheet("font-size: 20px; font-weight: bold; color: green;")
        green_team_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        green_team_layout.addWidget(green_team_label)

        # Add Green Team players 
        for player_id, player_name, equip_id in green_players:
            player_label = QLabel(f"{player_id} - {player_name} (Equipment: {equip_id})")
            player_label.setStyleSheet("font-size: 16px; color: white;")
            player_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)  
            green_team_layout.addWidget(player_label)

            self.green_player_labels[f'{player_id}'] = player_label
            print(self.green_players)

        main_layout.addLayout(green_team_layout, stretch=1)

        self.setLayout(main_layout)

        # Initialize and start game timer (6 minutes)
        self.game_time_remaining = 6 * 60  # 6 minutes in seconds
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_game_timer)
        self.game_timer.start(1000)  # Update every second

        # # Start traffic generator
        # self._running = True
        # self.traffic_thread = threading.Thread(target=self.generate_traffic, daemon=True)
        # self.traffic_thread.start()

    def update_game_timer(self):
        """Update the game timer display every second."""
        self.game_time_remaining -= 1
        
        if self.game_time_remaining <= 0:
            self.game_timer.stop()
            self.game_timer_label.setText("00:00")
            self.append_to_current_action("<div style='text-align: center; color: red;'>GAME OVER!</div>")
            # Stop traffic generator
            self._running = False
            # Return to player entry screen after brief delay
            QTimer.singleShot(2000, self.return_to_entry_screen)
        else:
            minutes = self.game_time_remaining // 60
            seconds = self.game_time_remaining % 60
            self.game_timer_label.setText(f"{minutes:02d}:{seconds:02d}")


    def closeEvent(self, event):
        from music import music_player
        music_player.stop_music()
        event.accept()

    def append_to_current_action(self, text):
        """Append text to the current action box and ensure it scrolls down."""
        self.current_action_text.append(text) 
        self.current_action_text.ensureCursorVisible()  
        cursor = self.current_action_text.textCursor()  
        cursor.movePosition(cursor.MoveOperation.End)  
        self.current_action_text.setTextCursor(cursor)  

    def return_to_entry_screen(self):
        """Stop the traffic generator and return to the player entry screen."""
        from player_entry_screen import PlayerEntryScreen  
        self._running = False
        self.game_timer.stop()  # Stop the game timer
        self.close()  

        self.player_entry_screen.showMaximized() 


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

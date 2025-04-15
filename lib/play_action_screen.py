from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QApplication
from PyQt6.QtCore import QTimer, Qt
import sys
from music import music_player
import socket

from database import Database

class PlayActionScreen(QWidget):
    def __init__(self, ip_address, red_players, green_players, on_exit):
        super().__init__()

        # Server information
        self.serverAddressPort = (ip_address, 7500)
        self.clientAddressPort = (ip_address, 7501)

        self.bufferSize  = 1024

        # Store players with their equipment IDs
        self.red_players = red_players
        self.green_players = green_players
        self.ip_address = ip_address

        self.exit = on_exit
        self.setWindowTitle("Play Action Screen")
        self.showMaximized()
        self.setStyleSheet("background-color: black; color: white;")

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
        # return_button.clicked.connect(self.return_to_entry_screen)
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

        main_layout.addLayout(green_team_layout, stretch=1)

        self.setLayout(main_layout)

        # Initialize game timer (6 minutes)
        self.game_time_remaining = 6 * 60
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_game_timer)

        # Create datagram sockets
        self.UDPClientSocketReceive = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocketTransmit = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        self.UDPClientSocketReceive.bind(self.clientAddressPort)
        self.UDPClientSocketReceive.setblocking(False)

        self.server_timer = QTimer(self)
        self.server_timer.timeout.connect(self.server_listener)

        self.server_timer.start(100)
        self.game_timer.start(1000)

        self.UDPServerSocketTransmit.sendto(str.encode(str(202)), self.serverAddressPort)

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

    def server_listener(self):
        try:
            raw_data = self.UDPClientSocketReceive.recvfrom(self.bufferSize)
            raw_player_data = raw_data[0]
            player_data = raw_player_data.decode('utf-8')
            print(f'Transmitted: {player_data}')

            parts = player_data.split(':')
            shooting_player = parts[0]
            shot_player = parts[1]

            print(f'Player with equip ID {shooting_player} has shot {shot_player}')

        except BlockingIOError:
            pass

    def closeEvent(self, event):
        music_player.stop_music()
        event.accept()

    def append_to_current_action(self, text):
        """Append text to the current action box and ensure it scrolls down."""
        self.current_action_text.append(text) 
        self.current_action_text.ensureCursorVisible()  
        cursor = self.current_action_text.textCursor()  
        cursor.movePosition(cursor.MoveOperation.End)  
        self.current_action_text.setTextCursor(cursor)  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    red_players = [("6005", "Player 1", "111"), ("5000", "Player 2", "112")]
    green_players = [("6005", "Player 3", "221"), ("5000", "Player 4", "222")]
    screen = PlayActionScreen(red_players, green_players, None, None)
    screen.show()
    sys.exit(app.exec())

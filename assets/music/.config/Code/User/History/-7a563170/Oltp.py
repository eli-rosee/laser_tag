from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QApplication
from PyQt6.QtCore import QTimer, Qt
import sys

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

        main_layout.addLayout(green_team_layout, stretch=1)

        self.setLayout(main_layout)

        # Initialize and start game timer (6 minutes)
        self.game_time_remaining = 6 * 60  # 6 minutes in seconds
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_game_timer)
        self.game_timer.start(1000)  # Update every second

        # Start traffic generator
        self._running = True
        self.traffic_thread = threading.Thread(target=self.generate_traffic, daemon=True)
        self.traffic_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    red_players = [("6005", "Player 1", "111"), ("5000", "Player 2", "112")]
    green_players = [("6005", "Player 3", "221"), ("5000", "Player 4", "222")]
    screen = PlayActionScreen(red_players, green_players, None, None)
    screen.show()
    sys.exit(app.exec())
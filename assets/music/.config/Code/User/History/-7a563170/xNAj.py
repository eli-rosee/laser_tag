from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QApplication
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
import sys

class PlayActionScreen(QWidget):
    action_signal = pyqtSignal(str)
    score_signal = pyqtSignal(str, str)  
    team_score_signal = pyqtSignal(str)

    def __init__(self, red_players, green_players, photon_network, player_entry_screen_instance, parent=None):
        super().__init__(parent)

        self.red_player_scores = {player_id: 0 for player_id, _, _ in red_players}
        self.green_player_scores = {player_id: 0 for player_id, _, _ in green_players}
        self.flash_timer = QTimer(self)
        self.flash_timer.timeout.connect(self.flash_high_team_score)
        self.flash_state = True
        self.flash_timer.start(500)
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

        red_team_layout = QVBoxLayout()
        red_team_label = QLabel("RED TEAM")
        red_team_score = QLabel("0")
        red_team_label.setStyleSheet("font-size: 20px; font-weight: bold; color: red;")
        red_team_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        red_team_score.setStyleSheet("font-size: 50px; font-weight: bold; color: red;")
        red_team_score.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        red_team_layout.addWidget(red_team_label)
        red_team_layout.addWidget(red_team_score)

        self.red_team_score_label = red_team_score
        self.red_team_score = 0

        self.red_player_layout = QVBoxLayout()
        red_players_count = len(red_players)
        for i, (player_id, player_name, equip_id) in enumerate(red_players):
            score = 0

            if i < red_players_count - 1 or i == 0:
               self.red_player_layout.addStretch(1)
    
            player_label = QLabel(f"{player_id} - {player_name} (Equipment: {equip_id}) Score: {score}")
            player_label.setStyleSheet("font-size: 16px; color: white;")
            player_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

            self.red_player_layout.addWidget(player_label)

            self.red_player_labels[f'{player_id}'] = player_label

        red_team_layout.addLayout(self.red_player_layout)

        red_team_layout.addStretch()

        main_layout.addLayout(red_team_layout)
        self.setLayout(main_layout)

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

        green_team_layout = QVBoxLayout()
        green_team_label = QLabel("GREEN TEAM")
        green_team_score = QLabel("0")
        green_team_label.setStyleSheet("font-size: 20px; font-weight: bold; color: green;")
        green_team_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        green_team_score.setStyleSheet("font-size: 50px; font-weight: bold; color: green;")
        green_team_score.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        green_team_layout.addWidget(green_team_label)
        green_team_layout.addWidget(green_team_score)

        self.green_team_score_label = green_team_score
        self.green_team_score = 0

        self.green_player_layout = QVBoxLayout()
        green_players_count = len(green_players)
        for i, (player_id, player_name, equip_id) in enumerate(green_players):
            score = 0

            if i < green_players_count - 1 or i == 0:
               self.green_player_layout.addStretch(1)
    
            player_label = QLabel(f"{player_id} - {player_name} (Equipment: {equip_id}) Score: {score}")
            player_label.setStyleSheet("font-size: 16px; color: white;")
            player_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

            self.green_player_layout.addWidget(player_label)

            self.green_player_labels[f'{player_id}'] = player_label

        green_team_layout.addLayout(self.green_player_layout)

        green_team_layout.addStretch()

        main_layout.addLayout(green_team_layout)
        self.setLayout(main_layout)

        # Initialize and start game timer (6 minutes)
        self.game_time_remaining = 6 * 60  # 6 minutes in seconds
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_game_timer)
        self.game_timer.start(1000)  # Update every second

if __name__ == "__main__":
    app = QApplication(sys.argv)
    red_players = [("6005", "Player 1", "111"), ("5000", "Player 2", "112")]
    green_players = [("6005", "Player 3", "221"), ("5000", "Player 4", "222")]
    screen = PlayActionScreen(red_players, green_players, None, None)
    screen.show()
    sys.exit(app.exec())
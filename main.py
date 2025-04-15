from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
import sys
import time

from ui.splash import SplashScreen
from ui.player_entry_screen import PlayerEntryScreen
from core.database import Database

main_window = None
countdown_window = None
splash_window = None
player_entry_screen = None
play_action_screen = None

def player_entry_transition():
    global player_entry_screen
    splash_window.close()
    player_entry_screen = PlayerEntryScreen()
    player_entry_screen.showMaximized()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash_window = SplashScreen()
    splash_window.showMaximized()

    QTimer.singleShot(2000, player_entry_transition)

    sys.exit(app.exec())
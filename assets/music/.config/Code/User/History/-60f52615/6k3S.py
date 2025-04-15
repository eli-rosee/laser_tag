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
player_entry_screen_window = None  
play_action_screen_window = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash_window = SplashScreen()
    splash_window.show()

    time.sleep(2)

        app = QApplication(sys.argv)
    self = PlayerEntryScreen()
    self.show()
    sys.exit(app.exec())
    sys.exit(app.exec())
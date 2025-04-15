from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
import sys
import time

from ui.splash import SplashScreen
from ui.player_entry_screen import PlayerEntryScreen
from core.database import Database


if __name__ == "__main__":
    try:
        splash_window = SplashScreen()
        splash_window.show()
    except Exception as e:
        print(f"Error initializing splash screen: {e}")
        sys.exit(1) 

    transition_timer = QTimer()
    time.sleep(100000)
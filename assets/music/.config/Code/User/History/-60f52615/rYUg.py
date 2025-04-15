from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
import sys
import time

from ui.splash import SplashScreen
from ui.player_entry_screen import PlayerEntryScreen
from core.database import Database


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()

    for i in range(1000):
        print("yep")
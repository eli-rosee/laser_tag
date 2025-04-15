from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
import sys

from ui.splash import SplashScreen
from ui.player_entry_screen import PlayerEntryScreen


if __name__ == "__main__":
    app = QApplication(sys.argv)
    countdown_handler = CountdownHandler()
    play_action_handler = PlayActionHandler()

    try:
        splash_window = splash.MainWindow()
        splash_window.show()
    except Exception as e:
        print(f"Error initializing splash screen: {e}")
        sys.exit(1) 

    transition_timer = QTimer()

    def transition_to_player_entry():
        global main_window, player_entry_screen_window
        transition_timer.stop()
        
        if splash_window:
            splash_window.close()

        try:
            player_entry_screen_window = player_entry_screen.PlayerEntryScreen() 
            main_window = player_entry_screen_window  
            main_window.showMaximized()
            QMetaObject.invokeMethod(
                main_window.red_row[0][3], "setFocus", Qt.ConnectionType.QueuedConnection
            )
        except Exception as e:
            print(f"Error initializing Player Entry Screen: {e}")
            sys.exit(1) 
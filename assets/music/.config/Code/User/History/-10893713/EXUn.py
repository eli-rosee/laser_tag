from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QSizePolicy, QLabel, QLineEdit
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt, QMetaObject
import sys
import time
import socket
from pynput import keyboard
import psycopg2

class PlayerEntryScreen(QWidget):
    
    def __init__(self):

        # Declare and initiate some basic attributes of the Player Entry Screen Window
        super().__init__()
        self.setWindowTitle("Player Entry Screen")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: black;")
        self.popup_active = False 
        main_layout = QVBoxLayout()
        QApplication.setStyle("windows")
        
        # Large amount of nonfunctional UI code
        self.title_label = QLabel("Player Entry Screen")
        self.directions = QLabel("Enter a NEW PLAYER ID:")
        
        self.directions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.directions.setStyleSheet("background-color: black; color: white; height: 10px;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 50px; font-weight: bold; color: blue;")

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.directions)
        
        teams_layout = QHBoxLayout()
        self.red_team_layout = QVBoxLayout()

        self.red_team_title = QLabel("RED TEAM")
        self.red_team_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.red_team_title.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: darkred;")
        self.red_team_layout.addWidget(self.red_team_title)

        self.red_team_info_layout = QHBoxLayout()

        self.add_label = QLabel("")
        self.add_label.setFixedWidth(37)
        self.add_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: darkred;")
        self.add_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.red_team_info_layout.addWidget(self.add_label,0)

        self.player_id_label = QLabel("PLAYER ID")
        self.player_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.player_id_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: darkred;")
        self.player_id_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.red_team_info_layout.addWidget(self.player_id_label,2)

        self.equipment_id_label = QLabel("CODE NAME")
        self.equipment_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.equipment_id_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: darkred;")
        self.equipment_id_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.red_team_info_layout.addWidget(self.equipment_id_label,2)

        self.equipment_id_label = QLabel("EQUIPMENT ID")
        self.equipment_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.equipment_id_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: darkred;")
        self.equipment_id_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.red_team_info_layout.addWidget(self.equipment_id_label,2)


        self.red_team_layout.addLayout(self.red_team_info_layout)
        
        self.red_team_list = QGridLayout()
        self.red_row = []

        for i in range(15):
            num_label = QLabel(f"{i}")
            num_label.setStyleSheet("color: white;")
            input_field1 = QLineEdit()
            input_field2 = QLineEdit()
            input_field3 = QLineEdit()

            input_field1.setStyleSheet("background-color: white; color: black;")
            input_field2.setStyleSheet("background-color: white; color: black;")
            input_field3.setStyleSheet("background-color: white; color: black;")

            input_field2.setReadOnly(True)
            input_field3.setReadOnly(True)

            arrow_label = QLabel(">>")  
            arrow_label.setStyleSheet("font-weight: bold; color: white;")
            
            arrow_label.setVisible(False)

            # Adds row to the red_row list and to the GUI
            self.red_row.append((arrow_label, num_label, input_field1, input_field2, input_field3))
            self.red_team_list.addWidget(arrow_label, i, 0)
            self.red_team_list.addWidget(num_label, i, 1)
            self.red_team_list.addWidget(input_field1, i, 2)
            self.red_team_list.addWidget(input_field2, i, 3)
            self.red_team_list.addWidget(input_field3, i, 4)
        
        self.red_team_layout.addLayout(self.red_team_list)
        teams_layout.addLayout(self.red_team_layout)
        
        self.green_team_layout = QVBoxLayout()

        self.green_team_title = QLabel("Green TEAM")
        self.green_team_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.green_team_title.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: Green;")
        self.green_team_layout.addWidget(self.green_team_title)

        self.green_team_info_layout = QHBoxLayout()

        self.player_id_label = QLabel("")
        self.player_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.player_id_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: Green;")
        self.player_id_label.setFixedWidth(37)
        self.green_team_info_layout.addWidget(self.player_id_label,0)

        self.player_id_label = QLabel("PLAYER ID")
        self.player_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.player_id_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: Green;")
        self.green_team_info_layout.addWidget(self.player_id_label,2)

        self.equipment_id_label = QLabel("CODE NAME")
        self.equipment_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.equipment_id_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: Green;")
        self.green_team_info_layout.addWidget(self.equipment_id_label,2)

        self.equipment_id_label = QLabel("EQUIPMENT ID")
        self.equipment_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.equipment_id_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: Green;")
        self.green_team_info_layout.addWidget(self.equipment_id_label,2)

        self.green_team_layout.addLayout(self.green_team_info_layout)
        
        self.green_team_list = QGridLayout()
        self.green_row = []
        for i in range(15):
            num_label = QLabel(f"{i}")
            num_label.setStyleSheet("color: white;")
            input_field1 = QLineEdit()
            input_field2 = QLineEdit()
            input_field3 = QLineEdit()

            input_field1.setStyleSheet("background-color: white; color: black;")
            input_field2.setStyleSheet("background-color: white; color: black;")
            input_field3.setStyleSheet("background-color: white; color: black;")

            input_field2.setReadOnly(True)
            input_field3.setReadOnly(True)

            arrow_label = QLabel(">>")  
            arrow_label.setStyleSheet("font-weight: bold; color: white;")
            arrow_label.setVisible(False)

            # Adds row to the red_row list and to the GUI
            self.green_row.append((arrow_label, num_label, input_field1, input_field2, input_field3))
            self.green_team_list.addWidget(arrow_label, i, 0)
            self.green_team_list.addWidget(num_label, i, 1)
            self.green_team_list.addWidget(input_field1, i, 2)
            self.green_team_list.addWidget(input_field2, i, 3)
            self.green_team_list.addWidget(input_field3, i, 4)

        self.green_team_layout.addLayout(self.green_team_list)
        teams_layout.addLayout(self.green_team_layout)
        
        main_layout.addLayout(teams_layout)
        main_layout.addWidget(self.directions)
        
        self.button_layout = QHBoxLayout()
        self.buttons = {}

        button_labels = {
                    30: "F1: Clear Game",
                    31: "F2: Change IP",
                    32: "F3: Start Game"
                }
        
        for index, label in button_labels.items():
            button = QPushButton(label)
            button.setStyleSheet("background-color: white; color: green; font-size: 12px;")
            button.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            self.button_layout.addWidget(button)
            self.buttons[index] = button 
        
        main_layout.addLayout(self.button_layout)
        self.setLayout(main_layout)


    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        print(key)

        # Handler for the F1 key press
        if key == 16777264:
            self.clear_game()
        # Handler for the F2 key press
        elif key == 16777265:
            self.change_ip()
        # Handler for the F3 key press
        elif key == 16777266:
            self.start_game()
        # Handler for the Enter key press
        elif key == 16777220 or key == 16777221:
            enter_field1 = None
            enter_field2 = None
            enter_field3 = None

            # Iterates through the red rows to look for cursor focus
            for arrow_label, num_label, field1, field2, field3 in self.red_row:
                if(field1.hasFocus() or field2.hasFocus() or field3.hasFocus()):
                    enter_field1 = field1
                    enter_field2 = field2
                    enter_field3 = field3

            # Iterates through the green rows to look for cursor focus
            for arrow_label, num_label, field1, field2, field3 in self.green_row:
                if(field1.hasFocus() or field2.hasFocus() or field3.hasFocus()):
                    enter_field1 = field1
                    enter_field2 = field2
                    enter_field3 = field3

            self.enter_handler(enter_field1, enter_field2, enter_field3)
            

        super().keyPressEvent(event)

    # Handles the clear game button functionality
    def clear_game(self):
        print("Clearing Game!")

    # Handles the change IP button functionality
    def change_ip(self):
        print("Changing IP Address")

    # Handles the start game button functionality
    def start_game(self):
        print("Starting Game")
    
    def enter_handler(self, field1, field2, field3, player_num, team, state):
        player_id = field1.text().strip()
        code_name = field2.text().strip()
        equip_id = field3.text().strip()

        if not player_id:
            self.directions.setText("Player ID cannot be empty")
            return None

        try:
            int_player_id = int(player_id)
        except ValueError:
            self.directions.setText("Player ID must be an integer")
            return None

        if equip_id:
            try:
                int_equip_id = int(equip_id)
            except ValueError:
                self.directions.setText("Equipment ID must be an integer")
                return None
        else:
            int_equip_id = None  
   
        DB_NAME = "photon"
        DB_HOST = "127.0.0.1"
        DB_PORT = "5432"

        def connect():
            try:
                conn = psycopg2.connect(
                    dbname=DB_NAME,
                    host=DB_HOST,
                    user="student",
                    password="student",
                    port=DB_PORT
                )
                return conn
            except psycopg2.Error as e:
                print("Database connection failed:", e)
                return None

        def get_player_by_id(conn, player_id):
            if conn:
                cursor = conn.cursor()
                player_id = int(player_id)
                cursor.execute("SELECT codename FROM players WHERE id = %s;", (player_id,))
                result = cursor.fetchone()
                cursor.close()
                return result[0] if result else None  
            return None

        def add_new_player(conn, player_id, codename):
            if conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO players (id, codename) VALUES (%s, %s);", (player_id, codename))
                conn.commit()
                cursor.close()


        def get_all_players():
            conn = connect()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM players;")
                players = cursor.fetchall()
                cursor.close()
                conn.close()
                return players  
            return []


        text = self.directions.text()
        number = text.replace("Enter ", "").replace("'s CODE NAME:", "")
       
        if "CODE NAME:" in self.directions.text() and field1.text() != number:
                field1.setText("")
                return
        elif player_id == "":
                self.directions.setText("Player Does not have an ID")
                return

        elif code_name == "" and player_id!="":
                conn = connect()
                if conn:
                        player = get_player_by_id(conn, player_id)
                        if player:  
                            field2.setText(player)
                            field2.setReadOnly(True)
                            self.directions.setText(f"Enter {player_id} equipment ID") 
                            field3.setcursor()
                            field3.setReadOnly(False)
                            QApplication.processEvents()

                            return
                        else: 
                            field2.setText("")

                        conn.close()  

                field1.setReadOnly(True)
                self.directions.setText(f"Enter {player_id}'s CODE NAME:")
                QApplication.processEvents()
                field2.setCursor()
                QApplication.processEvents()
                field2.setReadOnly(False)
                return
        elif (equip_id=="" and code_name!="" and player_id!=""):
                conn = connect()
                if conn:
                    player = get_player_by_id(conn, player_id)                            
                    if player:  
                        field2.setText(player)
                    else: 
                        add_new_player(conn, player_id, code_name)

                conn.close()  

                field2.setReadOnly(True)
                self.directions.setText(f"Enter {player_id} equipment ID") 
                field3.setCursor()
                field3.setReadOnly(False)
                return
        else:
            self.directions.setText(f"Enter a NEW PLAYER ID:") 
            
            # Handle tab change i think eventually

    # Returns all player data, should be run at the end of program
    def get_player_data(self):
        red_players = []
        green_players = []

        for row in self.red_row:
            player_id = row[3].text().strip()
            code_name = row[4].text().strip()
            equip_id = row[5].text().strip()

            if player_id and code_name and equip_id: 
                red_players.append((player_id, code_name, equip_id))

        for row in self.green_row:
            player_id = row[3].text().strip()
            code_name = row[4].text().strip()
            equip_id = row[5].text().strip()
            if player_id and code_name and equip_id: 
                green_players.append((player_id, code_name, equip_id))

        return red_players, green_players



if __name__ == "__main__":
    app = QApplication(sys.argv)
    self = PlayerEntryScreen()
    self.show()
    sys.exit(app.exec())
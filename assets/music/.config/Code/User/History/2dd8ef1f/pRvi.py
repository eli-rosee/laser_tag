from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QMetaObject
from PyQt6.QtGui import QCursor
import psycopg2

class Database:
    def handle_player(self, field, field2, field3, player_num, team, state):
        player_id = field.text().strip()
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
       
        if "CODE NAME:" in self.directions.text() and field.text() != number:
                field.setText("")
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
                            self.count +=1
                            QApplication.processEvents()

                            return
                        else: 
                            field2.setText("")

                        conn.close()  

                field.setReadOnly(True)
                self.directions.setText(f"Enter {player_id}'s CODE NAME:")
                QApplication.processEvents()
                field2.setCursor()
                QApplication.processEvents()
                field2.setReadOnly(False)
                self.count +=1
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
                QMetaObject.invokeMethod(field3, "setFocus", Qt.ConnectionType.QueuedConnection)
                field3.setReadOnly(False)
                self.count +=1
                return
        else:
            self.directions.setText(f"Enter a NEW PLAYER ID:") 
            if hasattr(self, "worker") and self.worker.isRunning():
                return

            self.worker = sortPlayers(self)
            self.worker.start()
            
            field2.setReadOnly(True)
            field3.setReadOnly(True)
            self.change_tab_thread.start()
            self.popup_active = False
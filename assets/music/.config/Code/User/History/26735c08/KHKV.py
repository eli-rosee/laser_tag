from PyQt6.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt6.QtGui import QPixmap
import sys

class Splash(QMainWindow):
    def __init__(self):
        # Calls super constructor for QMainWindow to initiate
        super().__init__()

        # Sets some basic elements of the window
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: black;")

        # Establishes the label and fills it in with the logo image
        self.label = QLabel(self)
        self.pixmap = QPixmap("../images/logo.jpg")
        self.label.setPixmap(self.pixmap)

        # Ensure the image scales with the label and maximizes it
        self.label.setScaledContents(True)
        self.showMaximized()

    def resizeEvent(self, event):
        # Adjust label size when window is resized
        self.label.setGeometry(0, 0, self.width(), self.height())
        event.accept()

if __name__ == "__main__":
    # Initializes and runs the MainWindow class
    app = QApplication(sys.argv)
    window = Splash()
    window.show()
    sys.exit(app.exec())
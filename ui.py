import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QMessageBox,
    QProgressBar, QVBoxLayout, QHBoxLayout,
    QSpacerItem, QSizePolicy
)
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path

logo_path = resource_path("assets/logo.png")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PROLOX - Chargement")
        self.setWindowIcon(QIcon(logo_path))
        
        self.setFixedSize(300, 300)

        main_layout = QVBoxLayout(self)

        # Spacer en haut pour centrer verticalement
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Texte "PROLOX" centré
        self.title = QLabel("PROLOX")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 28px; font-weight: bold; font-family: 'Arial Black', sans-serif; letter-spacing: 3px;")
        main_layout.addWidget(self.title)

        # Logo PNG centré
        self.logo = QLabel()
        pix = QPixmap(logo_path)
        self.logo.setPixmap(pix.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.logo)

        # Layout horizontal pour la barre de progression avec spacers
        h_layout = QHBoxLayout()
        h_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.spinner = QProgressBar()
        self.spinner.setAlignment(Qt.AlignCenter)
        self.spinner.setRange(0, 0)  # mode indéterminé
        self.spinner.setFixedSize(100, 20)
        h_layout.addWidget(self.spinner)
        
        h_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        main_layout.addLayout(h_layout)

        # Spacer en bas pour centrer verticalement
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Timer pour afficher l'erreur après 5 secondes
        QTimer.singleShot(5000, self.show_error)

    def show_error(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Erreur")
        msg.setText("Nous avons rencontré une erreur pendant le chargement. Code erreur #196769")
        msg.exec()
        QApplication.instance().quit()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

class FloatingWindow(QWidget):
    def _init_(self):
        super()._init_()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelesswindowHint | Qt.WindDwStaysOnTopHint)
        self.setGeometry(100, 100, 200,100)
        self.setWindowTitle('Floating Window')
        label = QLabel('Hello, world!', self)
        label.move(50, 20)
        button = QPushButton('Close', self)
        button.clicked.connect(self.close)
        button.move(50, 50)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FloatingWindow()
    window.show()
    sys.exit(app.exec_())

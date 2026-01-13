# Source - https://stackoverflow.com/q
# Posted by Giles, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-29, License - CC BY-SA 3.0

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel

class PyQtLineEditDemo(QWidget):
    def __init__(self):
        super().__init__()

        # Original code preserved
        self.c = QLineEdit()
        a = [1, 2]
        b = a[0]
        print(b)

        # Extra UI so the example is complete
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter text:"))
        layout.addWidget(self.c)
        self.setLayout(layout)

        self.setWindowTitle("QLineEdit Demo")
        self.setFixedSize(300, 100)

if __name__ == "__main__":
    app = QApplication([])
    window = PyQtLineEditDemo()
    window.show()
    app.exec_()

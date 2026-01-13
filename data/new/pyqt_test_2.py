# Source - https://stackoverflow.com/a
# Posted by furas, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-29, License - CC BY-SA 3.0

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel
import sys

app = QApplication(sys.argv)

# Original new-version code preserved
c = QLineEdit()
a = [1, 2]
b = a[0]
print(b)

# Added minimal window so code is complete
window = QWidget()
layout = QVBoxLayout()

layout.addWidget(QLabel("Enter text:"))
layout.addWidget(c)

window.setLayout(layout)
window.setWindowTitle("QLineEdit Demo (New Version)")
window.setFixedSize(300, 100)
window.show()

sys.exit(app.exec_())

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDialog
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QApplication


class VirtualKeyboard(QWidget):
    def __init__(self, line_edit, parent=None):
        super().__init__(parent)
        self.line_edit = line_edit
        self.parent = parent  
        self.setWindowFlags(Qt.WindowType.Popup)  
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)  

        
        self.setFixedSize(300, 400)  
        screen_geometry = QApplication.primaryScreen().availableGeometry()  
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        self.move(0, (screen_height - 300) // 2)  
        self.drag_position = None

        layout = QVBoxLayout(self)


        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()

        buttons = [
            ("1", row1), ("2", row1), ("3", row1),
            ("4", row2), ("5", row2), ("6", row2),
            ("7", row3), ("8", row3), ("9", row3),
            ("0", row4)
        ]

        for text, row in buttons:
            button = QPushButton(text, self)
            button.clicked.connect(self.on_button_clicked)
            row.addWidget(button)

        # Create the backspace button
        backspace_button = QPushButton("\u2190", self)
        backspace_button.clicked.connect(self.on_backspace_clicked)
        row4.addWidget(backspace_button)

        # Create the close button
        close_button = QPushButton("确认", self)
        close_button.clicked.connect(self.close_keyboard)
        row4.addWidget(close_button)

        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        layout.addLayout(row4)

        self.setLayout(layout)

    def on_button_clicked(self):
        sender = self.sender()
        text = sender.text()
        current_text = self.line_edit.text()
        self.line_edit.setText(current_text + text)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.drag_position:
            delta = event.globalPosition().toPoint() - self.drag_position
            # Adjust the delta to control the speed of dragging
            delta = delta / 2  # This limits the movement, making it smoother
            new_pos = self.pos() + delta
            # Limit the position to keep it within the screen bounds
            screen_geometry = QApplication.primaryScreen().availableGeometry()
            new_pos.setX(max(0, min(new_pos.x(), screen_geometry.width() - self.width())))
            new_pos.setY(max(0, min(new_pos.y(), screen_geometry.height() - self.height())))
            self.move(new_pos)
            self.drag_position = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.drag_position = None

    def on_backspace_clicked(self):
        """Handle the backspace (delete) button click."""
        current_text = self.line_edit.text()
        if current_text:
            self.line_edit.setText(current_text[:-1])  # Remove the last character

    def close_keyboard(self):
        self.close()  # Close and destroy the keyboard
        self.parent.virtual_keyboard = None
        self.parent.clearFocus()
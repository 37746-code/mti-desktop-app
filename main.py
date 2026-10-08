import sys
from abc import ABC, abstractmethod
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                             QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, 
                             QListWidget, QFrame, QMessageBox)
from PyQt6.QtCore import Qt


class AbstractEntity(ABC):
    @abstractmethod
    def get_info(self):
        pass


class User(AbstractEntity):
    def __init__(self, username, role="student"):
        self._username = username
        self._role = role

    
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    def get_info(self):
        return f"{self._username} ({self._role})"

    
    def __eq__(self, other):
        if not isinstance(other, User): return False
        return self._username == other._username

    def __repr__(self):
        return f"User('{self._username}')"

    def __str__(self):
        return self._username

   
    def __lt__(self, other):  
        return self._username < other._username

    def __gt__(self, other):
        return self._username > other._username

    def __len__(self):
        return len(self._username)


class CustomMap:
    def __init__(self):
        self._keys = []
        self._values = []

    def put(self, key, value):
        if key in self._keys:
            idx = self._keys.index(key)
            self._values[idx] = value
        else:
            self._keys.append(key)
            self._values.append(value)

    def get(self, key):
        if key in self._keys:
            idx = self._keys.index(key)
            return self._values[idx]
        return None

# 4. Переопределение 10 компонентов окна (UI)
class CustomMainWindow(QMainWindow): pass
class CustomWidget(QWidget): pass
class CustomButton(QPushButton): pass
class CustomLabel(QLabel): pass
class CustomLineEdit(QLineEdit): pass
class CustomVBox(QVBoxLayout): pass
class CustomHBox(QHBoxLayout): pass
class CustomListWidget(QListWidget): pass
class CustomFrame(QFrame): pass
class CustomMessageBox(QMessageBox): pass


class AppWindow(CustomMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MTI Desktop App")
        self.resize(400, 300)
        
       
        self.time_in = datetime.now()
        self.current_login = "Vadim_F"

        
        self.session_data = CustomMap()
        self.session_data.put("login", self.current_login)

        
        self.users_collection = [
            User(f"Student_{i}") for i in range(1, 11)
        ]

        self.init_ui()

    def init_ui(self):
        central_widget = CustomWidget()
        self.setCentralWidget(central_widget)

        
        main_layout = CustomVBox()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_label = CustomLabel("Управление пользователями")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)

        self.list_widget = CustomListWidget()
        for user in self.users_collection:
            self.list_widget.addItem(user.get_info())
        main_layout.addWidget(self.list_widget)

        input_layout = CustomHBox()
        self.input_field = CustomLineEdit()
        self.input_field.setPlaceholderText("Имя нового пользователя")
        self.add_button = CustomButton("Добавить")
        
       
        self.add_button.clicked.connect(self.add_user)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.add_button)
        
        main_layout.addLayout(input_layout)

        separator = CustomFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        main_layout.addWidget(separator)

        central_widget.setLayout(main_layout)

    def add_user(self):
        new_name = self.input_field.text()
        if new_name:
            new_user = User(new_name)
            self.users_collection.append(new_user)
            self.list_widget.addItem(new_user.get_info())
            self.input_field.clear()

    
    def closeEvent(self, event):
        time_out = datetime.now()
        login = self.session_data.get("login")
        
        time_format = "%d.%m.%Y %H:%M:%S"
        t_in_str = self.time_in.strftime(time_format)
        t_out_str = time_out.strftime(time_format)

        report_content = (
            "+----------+---------------------+---------------------+\n"
            "| login    | time_in             | time_out            |\n"
            "+----------+---------------------+---------------------+\n"
            f"| {login:<8} | {t_in_str} | {t_out_str} |\n"
            "+----------+---------------------+---------------------+\n"
        )

        with open("session_report.txt", "w", encoding="utf-8") as file:
            file.write(report_content)

        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec())
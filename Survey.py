from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QDateEdit,QCheckBox, QRadioButton, QPushButton, QGroupBox, QButtonGroup, QMessageBox)
import mysql.connector
from results_window import ResultsWindow  # Import the second window

class SurveyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Survey")
        self.setGeometry(200, 200, 400, 500)

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        # Full Name
        layout.addWidget(QLabel("Full Name:"))
        self.fullname_input = QLineEdit()
        layout.addWidget(self.fullname_input)

        # Email
        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        layout.addWidget(self.email_input)

        # Date of Birth
        layout.addWidget(QLabel("Date of Birth:"))
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        layout.addWidget(self.dob_input)

        # Phone Number
        layout.addWidget(QLabel("Phone Number:"))
        self.phone_input = QLineEdit()
        layout.addWidget(self.phone_input)

        # Age Input
        layout.addWidget(QLabel("Age:"))
        self.age_input = QLineEdit()
        layout.addWidget(self.age_input)

        # Favourite Food Checkboxes
        layout.addWidget(QLabel("Favourite Food:"))
        self.food_options = {
            "Pizza": QCheckBox("Pizza"),
            "Pasta": QCheckBox("Pasta"),
            "Papa and Wors": QCheckBox("Papa and Wors"),
            "Other": QCheckBox("Other")
        }
        for checkbox in self.food_options.values():
            layout.addWidget(checkbox)

        # TV Rating Radio Buttons
        layout.addWidget(QLabel("Rate People Who Watch TV:"))
        self.rating_group = QGroupBox("Rating Criteria")
        rating_layout = QVBoxLayout()

        self.rating_buttons = {
            1: QRadioButton("Strongly Disagree"),
            2: QRadioButton("Disagree"),
            3: QRadioButton("Neutral"),
            4: QRadioButton("Agree"),
            5: QRadioButton("Strongly Agree")
        }

        self.radio_group = QButtonGroup()
        for value, radio_btn in self.rating_buttons.items():
            rating_layout.addWidget(radio_btn)
            self.radio_group.addButton(radio_btn, value)

        self.rating_group.setLayout(rating_layout)
        layout.addWidget(self.rating_group)

        # Submit Button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.validate_and_insert)
        layout.addWidget(self.submit_button)

        self.central_widget.setLayout(layout)

    def validate_and_insert(self):
        # Collect user data
        fullname = self.fullname_input.text().strip()
        email = self.email_input.text().strip()
        dob = self.dob_input.date().toString("yyyy-MM-dd")
        phone = self.phone_input.text().strip()
        age = self.age_input.text().strip()

        # Validation checks
        if not fullname or not email or not phone or not age:
            QMessageBox.warning(self, "Validation Error", "All fields must be filled.")
            return

        if not age.isdigit() or int(age) < 5 or int(age) > 120:
            QMessageBox.warning(self, "Validation Error", "Age must be between 5 and 120.")
            return

        selected_food = ", ".join([food for food, checkbox in self.food_options.items() if checkbox.isChecked()])
        if not selected_food:
            QMessageBox.warning(self, "Validation Error", "Select at least one favorite food.")
            return

        selected_rating = self.radio_group.checkedId()
        if selected_rating == -1:
            QMessageBox.warning(self, "Validation Error", "Select a TV rating.")
            return

        # Database connection
        try:
            db = mysql.connector.connect(host="localhost", user="root", password="", database="user_data")
            cursor = db.cursor()

            sql = """INSERT INTO users (fullname, email, date_of_birth, phone_number, age, favourite_food, tv_rating)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (fullname, email, dob, phone, int(age), selected_food, selected_rating)

            cursor.execute(sql, values)
            db.commit()
            cursor.close()
            db.close()

            QMessageBox.information(self, "Success", "Survey submitted successfully!")

            # Open results window
            self.results_window = ResultsWindow()
            self.results_window.show()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")

if __name__ == "__main__":
    app = QApplication([])
    window = SurveyWindow()
    window.show()
    app.exec_()

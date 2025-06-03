import mysql.connector
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel

#connect to wamp MySQL database
db = mysql.connector.connect(
    host="localhost", #this is the default WAMPserver hostname
    user="root",      #this the database user in server
    password="",      #password is empty
    database="_Survey" #shows my database
)
cursor = db.cursor()


# Main Window
class Survey(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 400, 300)

        # Button to open the second window
        self.button = QPushButton("Open Second Window", self)
        self.button.setGeometry(100, 100, 200, 50)
        self.button.clicked.connect(self.open_second_window)

        self.second_window = None  # Placeholder for the second window

    def open_results(self):
        if self.results is None:  # Create the second window if it doesn't exist
        self.results = Results()
        self.results.show()  # Show the second window

# Second Window
class ResultsS(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Second Window")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()
        label = QLabel("This is the second window!")
        layout.addWidget(label)
        self.setLayout(layout)

# Main application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
'''

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QDateEdit, QCheckBox, QRadioButton, QPushButton, QGroupBox, QButtonGroup
import mysql.connector

class UserForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Information Form")
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
            "Strongly Agree": QRadioButton("Strongly Agree"),
            "Agree": QRadioButton("Agree"),
            "Neutral": QRadioButton("Neutral"),
            "Disagree": QRadioButton("Disagree"),
            "Strongly Disagree": QRadioButton("Strongly Disagree")
        }

        self.radio_group = QButtonGroup()
        for btn_text, radio_btn in self.rating_buttons.items():
            rating_layout.addWidget(radio_btn)
            self.radio_group.addButton(radio_btn)

        self.rating_group.setLayout(rating_layout)
        layout.addWidget(self.rating_group)

        # Submit Button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.insert_data)
        layout.addWidget(self.submit_button)

        self.central_widget.setLayout(layout)

    def insert_data(self):
        # Collect user data
        fullname = self.fullname_input.text()
        email = self.email_input.text()
        dob = self.dob_input.date().toString("yyyy-MM-dd")
        phone = self.phone_input.text()

        # Collect selected food options
        selected_food = ", ".join([food for food, checkbox in self.food_options.items() if checkbox.isChecked()])

        # Collect selected rating
        selected_rating = next((rating for rating, btn in self.rating_buttons.items() if btn.isChecked()), None)

        # Database connection
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Adjust if needed
                database="user_data"
            )
            cursor = db.cursor()

            # Insert data into MySQL
            sql = "INSERT INTO users (fullname, email, date_of_birth, phone_number, favourite_food, tv_rating) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (fullname, email, dob, phone, selected_food, selected_rating)

            cursor.execute(sql, values)
            db.commit()

            print("Data inserted successfully!")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            cursor.close()
            db.close()

if __name__ == "__main__":
    app = QApplication([])
    window = UserForm()
    window.show()
    app.exec_()
    '''
# Main application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    survey = MainWindow()
    survey.show()
    sys.exit(app.exec_())

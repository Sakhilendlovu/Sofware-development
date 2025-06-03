from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
import mysql.connector

class ResultsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Survey Results")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connect to database and fetch statistics
        db = mysql.connector.connect(host="localhost", user="root", password="", database="user_data")
        cursor = db.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        total_surveys = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(age) FROM users")
        average_age = round(cursor.fetchone()[0], 1)

        cursor.execute("SELECT MAX(age) FROM users")
        oldest = cursor.fetchone()[0]

        cursor.execute("SELECT MIN(age) FROM users")
        youngest = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM users WHERE favourite_food LIKE '%Pizza%'")
        pizza_lovers = cursor.fetchone()[0]
        pizza_percentage = round((pizza_lovers / total_surveys) * 100, 1)

        layout.addWidget(QLabel(f"Total Surveys Completed: {total_surveys}"))
        layout.addWidget(QLabel(f"Average Age: {average_age}"))
        layout.addWidget(QLabel(f"Oldest Participant: {oldest}"))
        layout.addWidget(QLabel(f"Youngest Participant: {youngest}"))
        layout.addWidget(QLabel(f"Pizza Lovers: {pizza_percentage}%"))

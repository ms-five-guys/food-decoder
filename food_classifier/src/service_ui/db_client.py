import mysql.connector
from datetime import datetime, timedelta

class DatabaseClient:
    def __init__(self, host, user, password, database):
        """
        Initialize the database client with connection parameters.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """
        Establish a connection to the MySQL database.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as err:
            print("Error connecting to database:", str(err))
            self.connection = None

    def close(self):
        """
        Close the database connection.
        """
        if self.connection:
            self.connection.close()

    def get_patient_info(self, patient_code):
        """
        Query the database for patient information, including photo, basic info,
        and recent 5 days nutritional intake.
        """
        if not self.connection:
            print("No database connection.")
            return None

        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Query for patient basic information and photo URL
            cursor.execute("SELECT *, photo_url FROM patients WHERE patient_code = %s", (patient_code,))
            patient_info = cursor.fetchone()
            
            if not patient_info:
                return None
            
            # Query for recent 5 days nutritional intake
            five_days_ago = datetime.now() - timedelta(days=5)
            cursor.execute("""
                SELECT date, SUM(calories) as total_calories, SUM(carbohydrates) as total_carbohydrates,
                       SUM(protein) as total_protein, SUM(fat) as total_fat, SUM(sodium) as total_sodium,
                       SUM(sugar) as total_sugar
                FROM patient_diets
                WHERE patient_code = %s AND date >= %s
                GROUP BY date
                ORDER BY date DESC
            """, (patient_code, five_days_ago))
            recent_nutrition = cursor.fetchall()
            
            cursor.close()
            
            return {
                "basic_info": patient_info,
                "recent_nutrition": recent_nutrition
            }
            
        except mysql.connector.Error as err:
            print("Database error:", str(err))
            return None

    def get_food_info_from_db(self, food_name):
        """
        Query the nutrition database for food information based on the food name.
        """
        if not self.connection:
            print("No database connection.")
            return None

        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Query for food information
            cursor.execute("SELECT * FROM nutrition_info WHERE food_name = %s", (food_name,))
            food_info = cursor.fetchone()
            
            cursor.close()
            
            return food_info
            
        except mysql.connector.Error as err:
            print("Database error:", str(err))
            return None

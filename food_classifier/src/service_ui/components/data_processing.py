import sys
import os

# Add the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(parent_dir)

import cv2
import numpy as np
import requests
import matplotlib.pyplot as plt
from clients.ml_client import MLClient
from clients.db_client import DatabaseClient

plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

# Initialize the ML client
ml_client = MLClient(
    server_url='custom-vision-server-url',  # Custom Vision Server URL
    prediction_key='prediction-key'         # prediction key
)

# Initialize the database client
db_client = DatabaseClient(
    host='azure-mysql-host',  # Azure MySQL host
    user='username',          # MySQL username
    password='password',      # MySQL password
    database='database-name'  # database name
)

def get_customer_info(customer_code):
    """
    Get customer information from the database using the customer code.
    """
    if not customer_code:
        return None, "Please enter a customer code.", None, None
    
    try:
        # Connect to the database
        db_client.connect()
        
        # Query the database for customer information
        customer_info = db_client.get_customer_info(customer_code)
        
        # Close the database connection
        db_client.close()
        
        if not customer_info:
            return None, "No customer information found for the given code.", None, None
        
        # Format the customer info with HTML and CSS
        customer_info_text = "<div style='border: 1px solid #ccc; padding: 10px; border-radius: 5px;'>"
        customer_info_text += "<strong>Customer Information</strong><br><br>"  # Add label as HTML
        customer_info_text += "<table style='width:100%;'>"
        customer_info_text += f"<tr><td><strong>성함</strong></td><td>{customer_info['basic_info']['name']}</td></tr>"
        customer_info_text += f"<tr><td><strong>생년월일</strong></td><td>{customer_info['basic_info'].get('id_number', 'N/A')}</td></tr>"
        customer_info_text += f"<tr><td><strong>성별</strong></td><td>{customer_info['basic_info'].get('gender', 'N/A')}</td></tr>"
        customer_info_text += f"<tr><td><strong>키</strong></td><td>{customer_info['basic_info'].get('height', 'N/A')} cm</td></tr>"
        customer_info_text += f"<tr><td><strong>몸무게</strong></td><td>{customer_info['basic_info'].get('weight', 'N/A')} kg</td></tr>"
        customer_info_text += f"<tr><td><strong>특이사항</strong></td><td>{customer_info['basic_info'].get('special_conditions', 'N/A')}</td></tr>"
        customer_info_text += "</table>"
        customer_info_text += "</div>"
        
        # Create a text summary of recent nutrition with colored text
        nutrition_summary = "<div style='border: 1px solid #ccc; padding: 10px; border-radius: 5px;'>"
        nutrition_summary += "<strong>Recent Nutrition Summary</strong><br><br>"  # Add label as HTML
        nutrition_summary += "<br>".join(
            f"날짜: <span style='color:blue;'>{nutrition['date']}</span><br>"
            f"  - 칼로리: <span style='color:red;'>{nutrition['total_calories']} kcal</span><br>"
            f"  - 수분: <span style='color:green;'>{nutrition['total_water']}g</span><br>"
            f"  - 단백질: <span style='color:orange;'>{nutrition['total_protein']}g</span><br>"
            f"  - 지방: <span style='color:purple;'>{nutrition['total_fat']}g</span><br>"
            f"  - 탄수화물: <span style='color:brown;'>{nutrition['total_carbohydrates']}g</span><br>"
            f"  - 당류: <span style='color:pink;'>{nutrition['total_sugar']}g</span><br>"
            for nutrition in customer_info['recent_nutrition']
        )
        nutrition_summary += "</div>"
        
        # Create a plot for recent nutrition
        dates = [nutrition['date'] for nutrition in customer_info['recent_nutrition']]
        calories = [nutrition['total_calories'] for nutrition in customer_info['recent_nutrition']]
        water = [nutrition['total_water'] for nutrition in customer_info['recent_nutrition']]
        protein = [nutrition['total_protein'] for nutrition in customer_info['recent_nutrition']]
        fat = [nutrition['total_fat'] for nutrition in customer_info['recent_nutrition']]
        carbohydrates = [nutrition['total_carbohydrates'] for nutrition in customer_info['recent_nutrition']]
        sugar = [nutrition['total_sugar'] for nutrition in customer_info['recent_nutrition']]
        
        # Create separate plots for each nutritional component
        fig, axs = plt.subplots(3, 2, figsize=(12, 10))  # 3 rows, 2 columns

        # Plot Calories
        axs[0, 0].plot(dates, calories, marker='o', label='Calories (kcal)', color='r')
        axs[0, 0].set_title('Calories')
        axs[0, 0].set_xlabel('Date')
        axs[0, 0].set_ylabel('kcal')
        axs[0, 0].tick_params(axis='x', rotation=45)

        # Plot Water
        axs[0, 1].plot(dates, water, marker='o', label='Water (g)', color='b')
        axs[0, 1].set_title('Water')
        axs[0, 1].set_xlabel('Date')
        axs[0, 1].set_ylabel('g')
        axs[0, 1].tick_params(axis='x', rotation=45)

        # Plot Protein
        axs[1, 0].plot(dates, protein, marker='o', label='Protein (g)', color='g')
        axs[1, 0].set_title('Protein')
        axs[1, 0].set_xlabel('Date')
        axs[1, 0].set_ylabel('g')
        axs[1, 0].tick_params(axis='x', rotation=45)

        # Plot Fat
        axs[1, 1].plot(dates, fat, marker='o', label='Fat (g)', color='m')
        axs[1, 1].set_title('Fat')
        axs[1, 1].set_xlabel('Date')
        axs[1, 1].set_ylabel('g')
        axs[1, 1].tick_params(axis='x', rotation=45)

        # Plot Carbohydrates
        axs[2, 0].plot(dates, carbohydrates, marker='o', label='Carbohydrates (g)', color='c')
        axs[2, 0].set_title('Carbohydrates')
        axs[2, 0].set_xlabel('Date')
        axs[2, 0].set_ylabel('g')
        axs[2, 0].tick_params(axis='x', rotation=45)

        # Plot Sugar
        axs[2, 1].plot(dates, sugar, marker='o', label='Sugar (g)', color='y')
        axs[2, 1].set_title('Sugar')
        axs[2, 1].set_xlabel('Date')
        axs[2, 1].set_ylabel('g')
        axs[2, 1].tick_params(axis='x', rotation=45)

        plt.tight_layout()

        # Load the image from the URL
        image_url = customer_info['basic_info']['photo_url']
        response = requests.get(image_url)
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        # Resize the image to the desired size
        resized_image = cv2.resize(image, (300, 300))  # Resize to 300x300 pixels

        return resized_image, customer_info_text, nutrition_summary, fig
        
    except Exception as e:
        return None, f"Error retrieving customer information: {str(e)}", None, None

def get_nutritional_info(image):
    """
    Process the captured image and get nutritional information.
    """
    if image is None:
        return "No image captured"
    
    try:
        # print("Image shape:", image.shape)  # Debug log
        
        # Convert image to bytes
        _, img_encoded = cv2.imencode('.jpg', image)
        img_bytes = img_encoded.tobytes()
        print("Image converted to bytes successfully")  # Debug log
        
        # Get food prediction from Custom Vision Server
        food_name, confidence = ml_client.get_food_prediction(img_bytes)
        
        # Connect to the database
        db_client.connect()
        
        # Query the database for food information
        food_info = db_client.get_food_info_from_db(food_name)
        
        # Close the database connection
        db_client.close()
        
        if not food_info:
            return "No nutritional information found for the given food."
        
        # Format the nutritional info
        return f"""음식: {food_info['food_name']}
확률: {confidence:.1f}%
1회 제공량: {food_info['serving_size']}

영양성분:
• 에너지(kcal): {food_info['calories']}
• 수분(g): {food_info['water']}
• 단백질(g): {food_info['protein']}
• 지방(g): {food_info['fat']}
• 탄수화물(g): {food_info['carbohydrates']}
• 당류(g): {food_info['sugar']}"""
            
    except Exception as e:
        # print("Error:", str(e))  # Debug log
        return f"Error processing image: {str(e)}"

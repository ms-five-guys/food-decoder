import gradio as gr
import cv2
import numpy as np
import matplotlib.pyplot as plt
from unittest.mock import patch  # TODO(GideokKim): Remove this import when ML server is ready
from ml_client import MLClient
from db_client import DatabaseClient
from matplotlib import font_manager, rc

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
        
        # Format the customer info
        customer_info_text = f"""이름: {customer_info['basic_info']['name']}
나이(주민번호 앞자리 6개): {customer_info['basic_info'].get('id_number', 'N/A')}
성별: {customer_info['basic_info'].get('gender', 'N/A')}
키: {customer_info['basic_info'].get('height', 'N/A')} cm
몸무게: {customer_info['basic_info'].get('weight', 'N/A')} kg
특이사항: {customer_info['basic_info'].get('special_conditions', 'N/A')}"""
        
        # Create a text summary of recent nutrition
        nutrition_summary = "\n".join(
            f"{nutrition['date']}: 에너지 {nutrition['total_calories']} kcal, "
            f"수분 {nutrition['total_water']}g, 단백질 {nutrition['total_protein']}g, "
            f"지방 {nutrition['total_fat']}g, 탄수화물 {nutrition['total_carbohydrates']}g, "
            f"당류 {nutrition['total_sugar']}g"
            for nutrition in customer_info['recent_nutrition']
        )
        
        # Create a plot for recent nutrition
        dates = [nutrition['date'] for nutrition in customer_info['recent_nutrition']]
        calories = [nutrition['total_calories'] for nutrition in customer_info['recent_nutrition']]
        water = [nutrition['total_water'] for nutrition in customer_info['recent_nutrition']]
        protein = [nutrition['total_protein'] for nutrition in customer_info['recent_nutrition']]
        fat = [nutrition['total_fat'] for nutrition in customer_info['recent_nutrition']]
        carbohydrates = [nutrition['total_carbohydrates'] for nutrition in customer_info['recent_nutrition']]
        sugar = [nutrition['total_sugar'] for nutrition in customer_info['recent_nutrition']]
        
        plt.figure(figsize=(10, 5))
        plt.plot(dates, calories, marker='o', label='Calories (kcal)')
        plt.plot(dates, water, marker='o', label='Water (g)')
        plt.plot(dates, protein, marker='o', label='Protein (g)')
        plt.plot(dates, fat, marker='o', label='Fat (g)')
        plt.plot(dates, carbohydrates, marker='o', label='Carbohydrates (g)')
        plt.plot(dates, sugar, marker='o', label='Sugar (g)')
        plt.title('Nutritional Intake Over the Last 5 Days')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        
        return customer_info['basic_info']['photo_url'], customer_info_text, nutrition_summary, plt
        
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

# Create Gradio interfaces
customer_info_interface = gr.Interface(
    fn=get_customer_info,
    inputs=gr.Textbox(label="Customer Code"),  # Add a textbox for customer code input
    outputs=[
        gr.Image(label="Customer Photo"),  # Display customer photo
        gr.Textbox(label="Customer Information"),  # Display customer information
        gr.Textbox(label="Recent Nutrition Summary"),  # Display recent nutrition summary
        gr.Plot(label="Recent Nutrition Graph")  # Display recent nutrition graph
    ],
    title="📱 Customer Information",
    description="Enter customer code to get customer information",
    theme="default"
)

nutritional_info_interface = gr.Interface(
    fn=get_nutritional_info,
    inputs=gr.Image(
        sources=["webcam"],
        type="numpy",
        label="Camera"
    ),
    outputs=gr.Textbox(label="Nutritional Information"),
    title="📱 Nutritional Information",
    description="Take a photo of food to get nutritional information",
    theme="default"
)

# Combine interfaces
demo = gr.TabbedInterface(
    [customer_info_interface, nutritional_info_interface],
    ["Customer Info", "Nutritional Info"]
)

# Run server
if __name__ == "__main__":
    # TODO(GideokKim): Remove this patch when ML server and database are ready
    # Mock the database and ML server functions for testing
    with patch('db_client.DatabaseClient.connect', return_value=None), \
         patch('db_client.DatabaseClient.close', return_value=None), \
         patch('db_client.DatabaseClient.get_customer_info', return_value={
             "basic_info": {
                 "name": "아프냥",
                 "photo_url": "https://github.com/user-attachments/assets/39f8ce21-a0d3-4878-8b98-5d02f99ac62c",
                 "id_number": "990101",
                 "gender": "여성",
                 "height": 160,
                 "weight": 50,
                 "special_conditions": "감기"
             },
             "recent_nutrition": [
                 {"date": "2025-02-11", "total_calories": 1800, "total_water": 500, "total_protein": 80, "total_fat": 70, "total_carbohydrates": 200, "total_sugar": 50},
                 {"date": "2025-02-12", "total_calories": 2200, "total_water": 550, "total_protein": 90, "total_fat": 80, "total_carbohydrates": 250, "total_sugar": 60},
                 {"date": "2025-02-13", "total_calories": 2000, "total_water": 530, "total_protein": 85, "total_fat": 75, "total_carbohydrates": 230, "total_sugar": 55},
                 {"date": "2025-02-14", "total_calories": 2100, "total_water": 540, "total_protein": 88, "total_fat": 78, "total_carbohydrates": 240, "total_sugar": 58},
                 {"date": "2025-02-15", "total_calories": 1900, "total_water": 520, "total_protein": 82, "total_fat": 72, "total_carbohydrates": 220, "total_sugar": 52}
             ]
         }), patch('db_client.DatabaseClient.get_food_info_from_db', return_value={
             "food_name": "김치찌개",
             "serving_size": "1인분 (300g)",
             "calories": "180kcal",
             "water": "50g",
             "protein": "12g",
             "fat": "8g",
             "carbohydrates": "15g",
             "sugar": "3g"
         }), patch('ml_client.MLClient.get_food_prediction', return_value=("김치찌개", 95.7)):
        demo.launch(
            server_name="0.0.0.0",  # Allow external connections
            server_port=7860,       # Specify port
            share=True              # Generate public URL
        )

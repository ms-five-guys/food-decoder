import gradio as gr
import cv2
import numpy as np
from unittest.mock import patch  # TODO(GideokKim): Remove this import when ML server and database are ready
from ml_client import MLClient
from db_client import DatabaseClient

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

def process_image(image):
    """
    Process the captured image and get nutritional information
    """
    # print("Received image:", type(image))  # Debug log
    
    if image is None:
        # print("No image received")  # Debug log
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
        
        # Format the result
        return f"""음식: {food_info['food_name']}
확률: {confidence:.1f}%
1회 제공량: {food_info['serving_size']}

영양성분:
• 열량: {food_info['calories']}
• 탄수화물: {food_info['carbohydrates']}
• 단백질: {food_info['protein']}
• 지방: {food_info['fat']}
• 나트륨: {food_info['sodium']}
• 당류: {food_info['sugar']}"""
            
    except Exception as e:
        # print("Error:", str(e))  # Debug log
        return f"Error processing image: {str(e)}"

# Create Gradio interface
demo = gr.Interface(
    fn=process_image,
    inputs=gr.Image(
        sources=["webcam"],
        type="numpy",
        label="Camera"
    ),
    outputs=gr.Textbox(label="Nutritional Information"),
    title="📱 Food Nutrition Analyzer",
    description="Take a photo of food to get nutritional information",
    theme="default",
    css="""
        #component-0 { max-width: 500px; margin: 0 auto; }
        .gradio-container { max-width: 550px; margin: 0 auto; }
    """
)

# Run server
if __name__ == "__main__":
    # TODO(GideokKim): Remove this patch when ML server and database are ready
    # Mock the database and ML server functions for testing
    with patch('db_client.DatabaseClient.connect', return_value=None), \
         patch('db_client.DatabaseClient.close', return_value=None), \
         patch('db_client.DatabaseClient.get_food_info_from_db', return_value={
             "food_name": "김치찌개",
             "serving_size": "1인분 (300g)",
             "calories": "180kcal",
             "carbohydrates": "15g",
             "protein": "12g",
             "fat": "8g",
             "sodium": "1500mg",
             "sugar": "3g"
         }), patch('ml_client.MLClient.get_food_prediction', return_value=("김치찌개", 95.7)):
        demo.launch(
            server_name="0.0.0.0",  # Allow external connections
            server_port=7860,       # Specify port
            share=True              # Generate public URL
        )

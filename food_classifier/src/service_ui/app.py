import gradio as gr
import cv2
import numpy as np
import requests
import json

def get_food_info_from_db(food_name):
    """
    Query the nutrition database for food information based on the food name.
    TODO(GideokKim): Connect to Azure Database for MySQL server
    """
    # Mocked database response
    mock_db_response = {
        "김치찌개": {
            "food_name": "김치찌개",
            "serving_size": "1인분 (300g)",
            "nutrition": {
                "calories": "180kcal",
                "carbohydrates": "15g",
                "protein": "12g",
                "fat": "8g",
                "sodium": "1500mg",
                "sugar": "3g"
            }
        }
    }
    
    return mock_db_response.get(food_name, None)

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
        
        # TODO(GideokKim): Uncomment when ML server is ready
        # # Send image to ML model server
        # response = requests.post(
        #     "http://localhost:8000/predict",  # Your model server endpoint
        #     files={"file": img_bytes},
        #     timeout=30
        # )
        
        # if response.status_code == 200:
        #     result = response.json()
        #     food_name = result.get("food_name", "Unknown")
        #     confidence = result.get("confidence", 0.0)
        
        # Temporary test response
        food_name = "김치찌개"
        confidence = 95.7
        
        # Query the database for food information
        food_info = get_food_info_from_db(food_name)
        
        if not food_info:
            return "No nutritional information found for the given food."
        
        # Format the result
        return f"""음식: {food_info['food_name']}
확률: {confidence:.1f}%
1회 제공량: {food_info['serving_size']}

영양성분:
• 열량: {food_info['nutrition']['calories']}
• 탄수화물: {food_info['nutrition']['carbohydrates']}
• 단백질: {food_info['nutrition']['protein']}
• 지방: {food_info['nutrition']['fat']}
• 나트륨: {food_info['nutrition']['sodium']}
• 당류: {food_info['nutrition']['sugar']}"""
            
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
    demo.launch(
        server_name="0.0.0.0",  # Allow external connections
        server_port=7860,       # Specify port
        share=True              # Generate public URL
    )

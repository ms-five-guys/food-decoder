import gradio as gr
from unittest.mock import patch  # TODO(GideokKim): Remove this import when ML server is ready
from components.ui_components import create_interfaces

# Create Gradio interfaces
customer_info_interface, nutritional_info_interface = create_interfaces()

# Combine interfaces
demo = gr.TabbedInterface(
    [customer_info_interface, nutritional_info_interface],
    ["Customer Info", "Nutritional Info"]
)

# Run server
if __name__ == "__main__":
    # TODO(GideokKim): Remove this patch when ML server and database are ready
    # Mock the database and ML server functions for testing
    with patch('clients.db_client.DatabaseClient.connect', return_value=None), \
         patch('clients.db_client.DatabaseClient.close', return_value=None), \
         patch('clients.db_client.DatabaseClient.get_customer_info', return_value={
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
         }), patch('clients.db_client.DatabaseClient.get_food_info_from_db', return_value={
             "food_name": "김치찌개",
             "calories": "180kcal",
             "water": "50g",
             "protein": "12g",
             "fat": "8g",
             "carbohydrates": "15g",
             "sugar": "3g"
         }), patch('clients.ml_client.MLClient.get_food_prediction', return_value=("김치찌개", 95.7)):
        demo.launch(
            server_name="0.0.0.0",  # Allow external connections
            server_port=7860,       # Specify port
            share=True              # Generate public URL
        )

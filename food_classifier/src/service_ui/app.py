import gradio as gr
from unittest.mock import patch  # TODO(GideokKim): Remove this import when ML server is ready
from components.create_interfaces import create_interfaces
from datetime import datetime # TODO(GideokKim): Remove this import when ML server is ready

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
    with patch('clients.db_client.DatabaseClient.get_customer_nutrition_info', return_value={
             "recent_nutrition": [
                 {"date": "2025-02-11", "total_calories": 1800, "total_carbohydrates": 200, "total_protein": 80, "total_fat": 70, "total_fiber": 25, "total_sodium": 2000},
                 {"date": "2025-02-12", "total_calories": 2200, "total_carbohydrates": 250, "total_protein": 90, "total_fat": 80, "total_fiber": 28, "total_sodium": 2200},
                 {"date": "2025-02-13", "total_calories": 2000, "total_carbohydrates": 230, "total_protein": 85, "total_fat": 75, "total_fiber": 26, "total_sodium": 2100},
                 {"date": "2025-02-14", "total_calories": 2100, "total_carbohydrates": 240, "total_protein": 88, "total_fat": 78, "total_fiber": 27, "total_sodium": 2150},
                 {"date": "2025-02-15", "total_calories": 1900, "total_carbohydrates": 220, "total_protein": 82, "total_fat": 72, "total_fiber": 24, "total_sodium": 2050}
             ],
             "recommended_nutrition": {
                 "calories": {"min": 1800, "max": 2200},
                 "carbohydrates": {"min": 200, "max": 260},
                 "protein": {"min": 75, "max": 95},
                 "fat": {"min": 65, "max": 85},
                 "fiber": {"min": 20, "max": 30},
                 "sodium": {"min": 1500, "max": 2300}
             }
         }), \
         patch('clients.db_client.DatabaseClient.get_food_info_from_db', return_value={
             "food_id": 1,
             "food_name": "김치찌개",
             "Energy": 180,
             "Carbohydrates": 15,
             "Protein": 12,
             "Fat": 8,
             "Dietary_Fiber": 3,
             "Sodium": 900,
             "created_at": datetime(2024, 2, 15, 12, 30, 0)
         }), \
         patch('clients.ml_client.MLClient.get_food_prediction', return_value=("김치찌개", 95.5)):
        demo.launch(
            server_name="0.0.0.0",  # Allow external connections
            server_port=7860,       # Specify port
            share=True              # Generate public URL
        )

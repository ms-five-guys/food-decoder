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
    # TODO(GideokKim): Remove this patch when ML server is ready
    # Mock the ML server functions for testing
    with patch('clients.db_client.DatabaseClient.get_food_info_from_db', return_value={
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

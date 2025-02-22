import os
import sys
import io

# Add the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(parent_dir)

from clients.ml_client import MLClient
from clients.db_client import DatabaseClient

class FoodProcessor:
    def __init__(self, ml_client=None, db_client=None):
        self.ml_client = ml_client or MLClient()
        self.db_client = db_client or DatabaseClient(
            host='azure-mysql-host',
            user='username',
            password='password',
            database='database-name'
        )
    
    def get_nutritional_info(self, image):
        """Process food image and get nutritional information"""
        if image is None:
            return {
                'error': "No image captured",
                'food_info': None,
                'confidence': 0
            }
        
        try:
            # Convert image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_bytes = img_byte_arr.getvalue()
            
            # Get food prediction
            food_name, confidence = self.ml_client.get_food_prediction(img_bytes)
            
            # Get nutritional information
            self.db_client.connect()
            food_info = self.db_client.get_food_info_from_db(food_name)
            self.db_client.close()
            
            if not food_info:
                return {
                    'error': f"No nutritional information found for {food_name}.",
                    'food_info': None,
                    'confidence': confidence
                }
            
            return {
                'error': None,
                'food_info': food_info,
                'confidence': confidence
            }
            
        except Exception as e:
            return {
                'error': f"Error: {str(e)}",
                'food_info': None,
                'confidence': 0
            } 
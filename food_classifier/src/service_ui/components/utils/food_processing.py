import os
import sys
import io

# Add the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(parent_dir)

from clients.ml_client import MLClient
from clients.db_client import DatabaseClient
from .customer_session import current_session

class FoodProcessor:
    def __init__(self, ml_client=None, db_client=None):
        self.ml_client = ml_client or MLClient()
        self.db_client = db_client or DatabaseClient()
    
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

    def get_recommended_values(self):
        """Get recommended nutritional values for the current customer"""
        try:
            if not current_session.is_active():
                print("No active customer session")
                return None
                
            self.db_client.connect()
            recommended = self.db_client.get_recommended_nutrition(current_session.customer_id)
            
            if recommended:
                return {
                    'calories': recommended['Energy_max'],
                    'carbohydrates': recommended['Carbohydrates_max'],
                    'protein': recommended['Protein_max'],
                    'fat': recommended['Fat_max'],
                    'fiber': recommended['Dietary_Fiber_max'],
                    'sodium': recommended['Sodium_max']
                }
            return None
            
        except Exception as e:
            print(f"Error getting recommended values: {str(e)}")
            return None
        finally:
            self.db_client.close() 
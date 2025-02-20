import os
import requests

class MLClient:
    def __init__(self):
        """
        Initialize the ML client with Azure Custom Vision configuration.
        """
        # Read configuration from env file
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        config = {}
        
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=')
                    # Remove quotes if present
                    config[key.strip()] = value.strip().strip('"').strip("'")
        
        # Get Azure Custom Vision configuration
        self.endpoint = config.get('AZURE_CUSTOM_VISION_ENDPOINT')
        self.prediction_key = config.get('AZURE_CUSTOM_VISION_API_KEY')
        self.project_id = config.get('AZURE_CUSTOM_VISION_PROJECT_ID')
        self.model_name = config.get('AZURE_CUSTOM_VISION_MODEL_NAME')
        
        # Construct the prediction URL
        self.prediction_url = f"{self.endpoint}/customvision/v3.0/Prediction/{self.project_id}/classify/iterations/{self.model_name}/image"

    def get_food_prediction(self, img_bytes):
        """
        Send image to Azure Custom Vision and get food prediction.
        
        Args:
            img_bytes: Image data in bytes
            
        Returns:
            tuple: (food_name, confidence)
        """
        headers = {
            'Content-Type': 'application/octet-stream',
            'Prediction-Key': self.prediction_key
        }
        
        try:
            # Send image to Custom Vision
            response = requests.post(
                self.prediction_url,
                headers=headers,
                data=img_bytes,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                predictions = result.get("predictions", [])
                
                if predictions:
                    # Get the prediction with highest probability
                    top_prediction = max(predictions, key=lambda x: x.get("probability", 0))
                    food_name = top_prediction.get("tagName", "Unknown")
                    confidence = top_prediction.get("probability", 0.0) * 100
                    print(f"Food name: {food_name}, Confidence: {confidence}")
                    return food_name, confidence
                else:
                    print("No predictions returned from Custom Vision")
                    return "Unknown", 0.0
            else:
                print(f"Custom Vision error: {response.status_code}")
                print(f"Response: {response.text}")
                return "Unknown", 0.0
                
        except requests.exceptions.Timeout:
            print("Request to Custom Vision timed out")
            return "Unknown", 0.0
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Custom Vision: {str(e)}")
            return "Unknown", 0.0
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return "Unknown", 0.0

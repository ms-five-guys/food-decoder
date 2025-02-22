from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os
from pathlib import Path

class MLClient:
    def __init__(self):
        """
        Initialize the ML client with Azure Custom Vision configuration.
        """
        current_dir = Path(__file__).resolve().parent
        
        # Construct path to .env file (2 levels up + etc directory)
        env_path = current_dir.parent.parent.parent / 'etc' / 'food-classifier' / '.env'
    
        
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"').strip("'")
        
        self.endpoint = os.getenv('AZURE_CUSTOM_VISION_ENDPOINT')
        self.api_key = os.getenv('AZURE_CUSTOM_VISION_API_KEY')
        self.project_id = os.getenv('AZURE_CUSTOM_VISION_PROJECT_ID')
        self.model_name = os.getenv('AZURE_CUSTOM_VISION_MODEL_NAME')
        
        credentials = ApiKeyCredentials(in_headers={"Prediction-key": self.api_key})
        self.classifier = CustomVisionPredictionClient(endpoint=self.endpoint, credentials=credentials)

    def get_food_prediction(self, img_bytes):
        """
        Send image to Azure Custom Vision and get food prediction using SDK.
        
        Args:
            img_bytes: Image data in bytes
            
        Returns:
            tuple: (food_name, confidence)
        """
        try:
            results = self.classifier.classify_image(
                project_id=self.project_id,
                published_name=self.model_name,
                image_data=img_bytes
            )
            
            if results.predictions:
                # Get the prediction with highest probability
                top_prediction = results.predictions[0]
                food_name = top_prediction.tag_name
                confidence = top_prediction.probability * 100
                
                print(f"Food name: {food_name}, Confidence: {confidence}")
                return food_name, confidence
            else:
                print("No predictions returned from Custom Vision")
                return "Unknown", 0.0
                
        except Exception as e:
            print(f"Error in Custom Vision prediction: {str(e)}")
            return "Unknown", 0.0

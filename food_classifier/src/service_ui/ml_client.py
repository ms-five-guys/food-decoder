import requests

class MLClient:
    def __init__(self, server_url, prediction_key):
        """
        Initialize the ML client with the server URL and prediction key.
        """
        self.server_url = server_url
        self.prediction_key = prediction_key

    # TODO(GideokKim): Connect to Custom Vision Server
    def get_food_prediction(self, img_bytes):
        """
        Send image to Custom Vision Server and get food prediction.
        """
        headers = {
            'Content-Type': 'application/octet-stream',
            'Prediction-Key': self.prediction_key
        }
        
        try:
            # Send image to Custom Vision Server
            response = requests.post(
                self.server_url,  # Custom Vision Server endpoint
                headers=headers,
                data=img_bytes,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                predictions = result.get("predictions", [])
                if predictions:
                    top_prediction = predictions[0]
                    food_name = top_prediction.get("tagName", "Unknown")
                    confidence = top_prediction.get("probability", 0.0) * 100
                    return food_name, confidence
                else:
                    return "Unknown", 0.0
            else:
                print("Custom Vision Server error:", response.status_code)
                return "Unknown", 0.0
        except Exception as e:
            print("Error communicating with Custom Vision Server:", str(e))
            return "Unknown", 0.0

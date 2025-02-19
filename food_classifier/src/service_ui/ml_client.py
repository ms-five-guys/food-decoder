import requests

def get_food_prediction_from_ml_server(img_bytes):
    """
    Send image to ML server and get food prediction.
    TODO(GideokKim): Connect to Custom Vision Server
    """

    # TODO(GideokKim): Uncomment when ML server is ready
    # # Send image to ML server
    # response = requests.post(
    #     "http://localhost:8000/predict",  # ML server endpoint
    #     files={"file": img_bytes},
    #     timeout=30
    # )
    
    # if response.status_code == 200:
    #     result = response.json()
    #     food_name = result.get("food_name", "Unknown")
    #     confidence = result.get("confidence", 0.0)
    #     return food_name, confidence

    # This function will be mocked in tests
    return "Unknown", 0.0

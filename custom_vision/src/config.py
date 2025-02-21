############################################################
# Azure API Configurations
# Authentication-related sensitive keys.
############################################################


# Imports
## Prediction module from Azure Custom Vision API
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

## OpenAPI Authentication
from msrest.authentication import ApiKeyCredentials

# Environment variable management
## Keeps sensitive information out of the codebase
from dotenv import load_dotenv

# Operating system interactions and directory management
## Used for environment variable access
import os


# Retrieve Azure Custom Vision API Configurations
def get_config():

    config = dict()
    
    ## Load environment variables
    load_dotenv()

    ## Retrieve sensitive credentials from environment variables
    ENDPOINT = os.getenv("AZURE_CUSTOM_VISION_ENDPOINT")
    KEY = os.getenv("AZURE_CUSTOM_VISION_API_KEY")
    PROJECT_ID  = os.getenv("AZURE_CUSTOM_VISION_PROJECT_ID")
    MODEL_NAME = os.getenv("AZURE_CUSTOM_VISION_MODEL_NAME")

    # Store sensitive data in a dictionary format
    config.update({"ENDPOINT": ENDPOINT, "KEY": KEY, "PROJECT_ID": PROJECT_ID, "MODEL_NAME": MODEL_NAME})

    return config


# Authenticate and return the client
def get_client(ENDPOINT, KEY):
    credentials = ApiKeyCredentials(in_headers = {"Prediction-key": KEY})
    client  = CustomVisionPredictionClient(endpoint = ENDPOINT, credentials = credentials)

    return client

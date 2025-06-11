import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_BASE_URL = "http://localhost:8000"  # Replace with your actual API base URL
API_TIMEOUT = 30  # seconds

# API Endpoints
SALES_ENDPOINTS = {
    'daily': '/sales/daily',
    'monthly': '/sales/monthly',
    'quarterly': '/sales/quarterly'
}

# Prediction API configuration
PREDICTION_API_URL = "https://salesninjaapi-752034082007.europe-west1.run.app/predict_basic" 
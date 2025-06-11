import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '90'))  # seconds

# API Endpoints
SALES_ENDPOINTS = {
    'daily': '/sales/daily',
    'monthly': '/sales/monthly',
    'quarterly': '/sales/quarterly'
}

# Prediction API Configuration
PREDICTION_API_URL = os.getenv(
    'PREDICTION_API_URL',
    'http://localhost:8000'
) 
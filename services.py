import requests
from urllib.parse import urljoin
import pandas as pd
from config import API_BASE_URL, API_TIMEOUT, SALES_ENDPOINTS, PREDICTION_API_URL

class SalesService:
    @staticmethod
    def get_daily_sales(start_date: str, end_date: str) -> pd.DataFrame:
        """Get daily sales data between start_date and end_date."""
        endpoint = urljoin(API_BASE_URL, SALES_ENDPOINTS['daily'])
        params = {'start_date': start_date, 'end_date': end_date}
        
        try:
            response = requests.get(endpoint, params=params, timeout=API_TIMEOUT)
            response.raise_for_status()
            
            # Convert response to DataFrame
            data = response.json()
            if not data:  # If data is empty
                return pd.DataFrame(columns=['date', 'total_sales', 'day_of_week', 'store_count', 'product_count'])
                
            df = pd.DataFrame(data)
            
            # Ensure date column exists and is in datetime format
            if 'date' not in df.columns:
                raise ValueError("API response does not contain 'date' field")
                
            df['date'] = pd.to_datetime(df['date'])
            return df
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except ValueError as e:
            raise Exception(f"Data processing error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_monthly_sales(year: int) -> dict:
        """Get monthly sales data for a specific year.
        
        Args:
            year (int): The year to get sales data for
            
        Returns:
            dict: A dictionary containing yearly total and monthly breakdown with the following structure:
                {
                    'year': int,
                    'total_yearly_sales': float,
                    'monthly_data': List[dict]
                }
        """
        endpoint = urljoin(API_BASE_URL, SALES_ENDPOINTS['monthly'])
        params = {'year': year}
        
        try:
            response = requests.get(endpoint, params=params, timeout=API_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_quarterly_sales(quarter: int, year: int) -> pd.DataFrame:
        """Get quarterly sales data for specific quarter and year."""
        endpoint = urljoin(API_BASE_URL, SALES_ENDPOINTS['quarterly'])
        params = {'quarter': quarter, 'year': year}
        
        response = requests.get(endpoint, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
        return pd.DataFrame(response.json())

    @staticmethod
    def get_sales_prediction(min_date: str, max_date: str) -> pd.DataFrame:
        """Get sales predictions for a date range.
        
        Args:
            min_date (str): Start date in YYYY-MM-DD format
            max_date (str): End date in YYYY-MM-DD format
            
        Returns:
            pd.DataFrame: DataFrame with date and predicted sales
        """
        try:
            params = {
                'min_date': min_date,
                'max_date': max_date
            }
            
            response = requests.get(PREDICTION_API_URL, params=params, timeout=API_TIMEOUT)
            response.raise_for_status()
            
            # Convert response to DataFrame
            data = response.json()
            if not data:  # If data is empty
                return pd.DataFrame(columns=['date', 'predicted_sales'])
            
            # Convert dictionary to DataFrame
            df = pd.DataFrame(list(data.items()), columns=['date', 'predicted_sales'])
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            return df
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Prediction API request failed: {str(e)}")
        except ValueError as e:
            raise Exception(f"Data processing error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}") 
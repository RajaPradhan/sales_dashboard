# Sales Dashboard

A Streamlit-based dashboard for visualizing sales data from a REST API.

## Features

- Daily sales analysis with date range filtering
- Monthly sales analysis with month and year selection
- Quarterly sales analysis with quarter and year selection
- Interactive charts and data tables
- Configurable API endpoints

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `env.example` to `.env` and configure your environment variables:
   ```bash
   cp env.example .env
   ```
5. Edit `.env` file with your specific configuration

## Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The dashboard will be available at http://localhost:8501

## Configuration

The following environment variables can be configured in `.env`:

- `API_BASE_URL`: Base URL for the REST API (default: http://localhost:8000)
- `API_TIMEOUT`: API request timeout in seconds (default: 30)

## API Endpoints

The dashboard connects to the following API endpoints:

- Daily sales: `GET /sales/daily?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- Monthly sales: `GET /sales/monthly?month=MM&year=YYYY`
- Quarterly sales: `GET /sales/quarterly?quarter=Q&year=YYYY` 
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Alpha Vantage Configuration
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
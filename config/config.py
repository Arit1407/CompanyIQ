"""
Project Configuration File
CompanyIQ - AI Powered Company Intelligence Platform
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# ===================================================
# LOAD ENVIRONMENT VARIABLES
# ===================================================

load_dotenv()

# ===================================================
# PROJECT ROOT
# ===================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# ===================================================
# API CONFIGURATION
# ===================================================

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

REQUEST_TIMEOUT = 30

# ===================================================
# DATA DIRECTORY
# ===================================================

DATA_PATH = BASE_DIR / "data"

# ===================================================
# RAW DATA
# ===================================================

RAW_DATA_PATH = DATA_PATH / "raw"

# Company Master
COMPANY_MASTER_PATH = (
    RAW_DATA_PATH
    / "company_master"
    / "company_master_fixed.csv"
)

# Raw API Responses
API_RESPONSE_PATH = (
    RAW_DATA_PATH
    / "api_responses"
)

INCOME_STATEMENT_PATH = (
    API_RESPONSE_PATH
    / "income_statement"
)

BALANCE_SHEET_PATH = (
    API_RESPONSE_PATH
    / "balance_sheet"
)

CASH_FLOW_PATH = (
    API_RESPONSE_PATH
    / "cash_flow"
)

OVERVIEW_PATH = (
    API_RESPONSE_PATH
    / "overview"
)

# Annual Reports
REPORTS_PATH = (
    RAW_DATA_PATH
    / "reports"
)

# ===================================================
# PROCESSED DATASETS
# ===================================================

PROCESSED_DATA_PATH = (
    DATA_PATH
    / "processed"
)

FINANCIAL_DATASET_PATH = (
    PROCESSED_DATA_PATH
    / "financial_data.csv"
)

VALUATION_DATASET_PATH = (
    PROCESSED_DATA_PATH
    / "valuation_data.csv"
)

NEWS_DATASET_PATH = (
    PROCESSED_DATA_PATH
    / "news_data.csv"
)

# ===================================================
# RAG
# ===================================================

RAG_PATH = BASE_DIR / "rag"

REPORT_CHUNKS_PATH = (
    RAG_PATH
    / "chunks"
)

EMBEDDINGS_PATH = (
    RAG_PATH
    / "embeddings"
)

# ===================================================
# VECTOR DATABASE
# ===================================================

VECTOR_DB_PATH = (
    BASE_DIR
    / "vector_db"
)

CHROMA_DB_PATH = (
    VECTOR_DB_PATH
    / "chroma_db"
)

# ===================================================
# DASHBOARD
# ===================================================

DASHBOARD_PATH = (
    BASE_DIR
    / "dashboard"
)

# ===================================================
# AGENTS
# ===================================================

AGENTS_PATH = (
    BASE_DIR
    / "agents"
)

# ===================================================
# LOGS
# ===================================================

LOG_PATH = (
    BASE_DIR
    / "logs"
)

# ===================================================
# PROJECT SETTINGS
# ===================================================

FINANCIAL_YEARS = 3

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

TOP_K_RESULTS = 5

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ===================================================
# CREATE PROJECT DIRECTORIES
# ===================================================

DIRECTORIES = [

    # API Responses
    API_RESPONSE_PATH,
    INCOME_STATEMENT_PATH,
    BALANCE_SHEET_PATH,
    CASH_FLOW_PATH,
    OVERVIEW_PATH,

    # Reports
    REPORTS_PATH,

    # Processed Data
    PROCESSED_DATA_PATH,

    # RAG
    REPORT_CHUNKS_PATH,
    EMBEDDINGS_PATH,

    # Vector Database
    CHROMA_DB_PATH,

    # Dashboard
    DASHBOARD_PATH,

    # Agents
    AGENTS_PATH,

    # Logs
    LOG_PATH

]

for directory in DIRECTORIES:
    directory.mkdir(parents=True, exist_ok=True)
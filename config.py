import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB configuration
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB")

# Other configuration variables
DEBUG = os.getenv("DEBUG", default=False)  # Use 'True' or 'False' as strings for boolean values
SECRET_KEY = os.getenv("SECRET_KEY")

HOST = os.getenv("HOST", "0.0.0.0")
PORT = os.getenv("PORT", 8000)

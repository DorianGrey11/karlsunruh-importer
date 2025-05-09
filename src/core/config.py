import os
from dotenv import load_dotenv

load_dotenv()

API_URL: str = os.getenv("API_URL", "http://localhost:8000/api/v1")
AUTH_EMAIL: str = os.getenv("AUTH_EMAIL", "admin@example.com")
AUTH_PASSWORD: str = os.getenv("AUTH_PASSWORD", "admin")

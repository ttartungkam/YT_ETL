import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")
YT_URL = os.getenv("YT_URL")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 50))
MAX_RESULTS = int(os.getenv("MAX_RESULTS", 50))
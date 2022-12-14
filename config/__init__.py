import os

from .logger import *
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
API_TOKEN = os.getenv("API_TOKEN")
SERVICE_PORT = int(os.getenv("SERVICE_PORT"))
SERVICE_HOST = os.getenv("SERVICE_HOST")
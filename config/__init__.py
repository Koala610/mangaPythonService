import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
API_TOKEN = os.getenv("API_TOKEN")

SERVICE_PORT = int(os.getenv("SERVICE_PORT"))
SERVICE_HOST = os.getenv("SERVICE_HOST")

USERNAME = os.getenv("MYSQL_USERNAME")
PASSWORD = os.getenv("MYSQL_PASSWORD")
HOST = os.getenv("MYSQL_HOST")
DATABASE = os.getenv("MYSQL_DATABASE")
PORT = os.getenv("MYSQL_PORT")

DSN = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8mb4"

TEST_USERNAME = os.getenv("TEST_USERNAME")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")
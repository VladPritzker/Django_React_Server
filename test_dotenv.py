# test_dotenv.py
from dotenv import load_dotenv
import os

load_dotenv()

print("SECRET_KEY:", os.getenv('SECRET_KEY'))
print("DEBUG:", os.getenv('DEBUG'))
print("DB_NAME:", os.getenv('DB_NAME'))

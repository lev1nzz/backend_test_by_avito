
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SHORT_URL_LEN = int(os.getenv('SHORT_URL_LEN', '50')) 
BASE_URL_LEN = int(os.getenv('BASE_URL_LEN', '500'))
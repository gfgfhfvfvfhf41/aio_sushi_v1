import os
from dotenv import load_dotenv

load_dotenv()
token_main = os.getenv("TOKEN_MAIN")
token_test = os.getenv("TOKEN_TEST")

TOKEN = token_main 
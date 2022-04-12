import os
import sys

from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from src.api.router import api

if __name__ == "__main__":
    load_dotenv()
    api.run(host='0.0.0.0')

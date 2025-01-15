import os
from os.path import join, dirname
from dotenv import load_dotenv


load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SUB_KEY = os.environ.get("SUBSCRIPTION_KEY")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
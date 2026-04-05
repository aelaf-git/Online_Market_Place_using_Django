import os
from pathlib import Path
from environ import Env

BASE_DIR = Path(__file__).resolve().parent
env = Env()
env_file = BASE_DIR / '.env'
print(f"Reading {env_file}...")
if env_file.exists():
    env.read_env(env_file)
    print(f"GOOGLE_CLIENT_ID: {env('GOOGLE_CLIENT_ID', default='NOT FOUND')}")
else:
    print(".env file not found!")

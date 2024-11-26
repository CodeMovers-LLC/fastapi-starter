from contextlib import asynccontextmanager
from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()

DB_ENDPOINT = os.getenv("AWS_DATABASE_ENDPOINT")
DB_USERNAME = os.getenv("AWS_DATABASE_USERNAME")
DB_PASSWORD = os.getenv("AWS_DATABASE_PASSWORD")
DB_NAME = os.getenv("AWS_DATABASE_NAME")

required_vars = ["AWS_DATABASE_ENDPOINT", "AWS_DATABASE_USERNAME",
                 "AWS_DATABASE_PASSWORD", "AWS_DATABASE_NAME"]

for var in required_vars:
    if not os.getenv(var):
        raise EnvironmentError(f"Environment variable {var} is missing")

DATABASE_URL = f"mysql+aiomysql://{DB_USERNAME}:{
    DB_PASSWORD}@{DB_ENDPOINT}/{DB_NAME}"
    
database = Database(DATABASE_URL)

@asynccontextmanager
async def lifespan(app):
    await database.connect()
    yield
    await database.disconnect()

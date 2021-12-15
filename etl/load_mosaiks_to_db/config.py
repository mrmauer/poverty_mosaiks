import os

class Config:
    DATABASE_NAME = "mosaics"
    DATABASE_USER = "postgres"
    DATABASE_PASSWORD = os.getenv("MOSAIKS_DATABASE_PASSWORD")
    DATABASE_PORT = 5432
    DATABASE_HOST = os.getenv("MOSAIKS_DATABASE_HOST")
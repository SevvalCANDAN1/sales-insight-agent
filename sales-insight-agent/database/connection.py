import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """
    Establishes a connection to the PostgreSQL database using environment variables.
    """

    required_variables = [
        "DB_HOST",
        "DB_PORT",
        "DB_USER",
        "DB_PASSWORD"
    ]

    missing = [
        variable
        for variable in required_variables
        if not os.getenv
    ]

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}"
        )

    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"), 
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    connection.set_session(readonly=True)
    return connection
# sherlock-ai/database/db_config.py

from pathlib import Path
from sqlalchemy import create_engine, Engine

def get_db_engine() -> Engine:
    """
    Creates and returns a SQLAlchemy engine connected to the Chinook SQLite database.

    The path to the database is constructed relative to the project's root
    directory to ensure it works regardless of where the script is executed.

    Returns:
        Engine: A SQLAlchemy Engine instance.
    """
    # Define the path to the project root.
    # Assumes this file is in 'insightgpt/database/'.
    # We go up two levels to get to the 'insightgpt' root.
    project_root = Path(__file__).parent.parent
    
    # Define the path to the SQLite database file.
    db_path = project_root / "database" / "chinook.db"

    # Check if the database file exists before creating the engine
    if not db_path.exists():
        raise FileNotFoundError(
            f"Database file not found at {db_path}. "
            "Please ensure the chinook.db file is in the 'database' directory."
        )

    # Create the SQLAlchemy engine
    engine = create_engine(f"sqlite:///{db_path}")
    
    return engine

# import os
# from sqlalchemy import create_engine

# def get_db_engine():
#     engine = create_engine(
#         f"snowflake://{os.environ['SNOWFLAKE_USER']}:{os.environ['SNOWFLAKE_PASSWORD']}"
#         f"@{os.environ['SNOWFLAKE_ACCOUNT']}/{os.environ['SNOWFLAKE_DATABASE']}/{os.environ['SNOWFLAKE_SCHEMA']}"
#         f"?warehouse={os.environ['SNOWFLAKE_WAREHOUSE']}"
#     )
#     return engine

if __name__ == '__main__':
    # A simple test to verify the connection when the script is run directly
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            print("Successfully connected to the Chinook database!")
            print(f"Engine Dialect: {engine.dialect.name}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
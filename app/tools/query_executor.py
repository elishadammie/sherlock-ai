# sherlock-ai/app/tools/query_executor.py

import pandas as pd
from langchain_core.tools import tool
from sqlalchemy.exc import SQLAlchemyError

from database.db_config import get_db_engine

@tool
def execute_sql_tool(query: str) -> str | list[dict]:
    """
    Executes a given SQL query against the Chinook database and returns the result.

    This tool is designed to be robust. If the query is successful, it returns
    a list of dictionaries (one for each row). If the query fails for any
    reason, it catches the exception and returns a formatted error message.
    This feedback is crucial for the agent to debug its own generated SQL.

    Args:
        query: A string containing the SQLite-compatible SQL query to be executed.

    Returns:
        - A list of dictionaries representing the query result on success.
        - A string containing a detailed error message on failure.
    """
    print("---EXECUTING SQL QUERY---")
    print(f"Query: {query}")
    
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            # Use pandas to execute the query and fetch results into a DataFrame
            df = pd.read_sql_query(query, connection)
        
        # Convert the DataFrame to a list of dictionaries for serialization
        result = df.to_dict(orient='records')
        print("---QUERY SUCCESSFUL---")
        return result

    except SQLAlchemyError as e:
        # Catch specific database errors
        error_message = (
            f"Error executing SQL query: {e}\n"
            f"Query: '{query}'\n"
            "Please check the SQL syntax and ensure the table and column names are correct."
        )
        print(f"---QUERY FAILED---\n{error_message}")
        return error_message
        
    except Exception as e:
        # Catch any other unexpected errors
        error_message = (
            f"An unexpected error occurred: {e}\n"
            f"Query: '{query}'"
        )
        print(f"---UNEXPECTED ERROR---\n{error_message}")
        return error_message

if __name__ == '__main__':
    # This block allows for independent testing of the query executor tool
    print("---Running Tool Tests---")

    # Test Case 1: Successful query
    print("\n---Test 1: Successful Query---")
    success_query = "SELECT ArtistId, Name FROM artists ORDER BY ArtistId LIMIT 3;"
    success_result = execute_sql_tool.invoke({"query": success_query})
    print("Result:", success_result)
    assert isinstance(success_result, list)
    assert len(success_result) == 3
    assert success_result[0]['Name'] == 'AC/DC'
    print("Success test PASSED.")

    # Test Case 2: Failed query (syntax error)
    print("\n---Test 2: Failed Query (Incorrect Column)---")
    fail_query = "SELECT NonExistentColumn FROM artists LIMIT 3;"
    fail_result = execute_sql_tool.invoke({"query": fail_query})
    print("Result:", fail_result)
    assert isinstance(fail_result, str)
    assert "Error" in fail_result
    print("Failure test PASSED.")

    # Test Case 3: Failed query (incorrect table)
    print("\n---Test 3: Failed Query (Incorrect Table)---")
    fail_query_2 = "SELECT Name FROM artistss LIMIT 3;"
    fail_result_2 = execute_sql_tool.invoke({"query": fail_query_2})
    print("Result:", fail_result_2)
    assert isinstance(fail_result_2, str)
    assert "Error" in fail_result_2
    print("Failure test PASSED.")
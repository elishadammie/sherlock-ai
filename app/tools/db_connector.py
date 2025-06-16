# sherlock-ai/app/tools/db_connector.py

from langchain_core.tools import tool
from sqlalchemy import inspect, Engine
from database.db_config import get_db_engine

# Initialize the engine once to be reused by the tools
db_engine: Engine = get_db_engine()

@tool
def list_tables_tool() -> list[str]:
    """
    Returns a list of table names available in the database.
    This is a critical first step for the agent to know what tables it can query.
    """
    inspector = inspect(db_engine)
    return inspector.get_table_names()

@tool
def get_table_schema_tool(table_name: str) -> str:
    """
    Returns the DDL 'CREATE TABLE' statement for a specified table.
    This helps the agent understand the columns, types, and keys of a table.
    """
    inspector = inspect(db_engine)
    try:
        # The inspector's get_table_ddl method is not standard.
        # We will reflect the table and construct the DDL manually.
        # This is a simplified example. A more robust version could be built.
        
        # A simple way to get schema is to just get column info.
        columns = inspector.get_columns(table_name)
        
        col_defs = []
        for col in columns:
            col_defs.append(f"    {col['name']} {col['type']}")
        
        primary_keys = inspector.get_pk_constraint(table_name)['constrained_columns']
        pk_def = f",\n    PRIMARY KEY ({', '.join(primary_keys)})" if primary_keys else ""

        return f"CREATE TABLE {table_name} (\n{',\n'.join(col_defs)}{pk_def}\n);"
        
    except Exception as e:
        return f"Error: Could not retrieve schema for table '{table_name}'. Reason: {e}"

if __name__ == '__main__':
    # Test the tools
    print("Available tables:", list_tables_tool.invoke({}))
    print("\nSchema for 'invoices' table:")
    print(get_table_schema_tool.invoke({"table_name": "invoices"}))
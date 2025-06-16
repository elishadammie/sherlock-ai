# isherlock-ai/app/agents/schema_retriever.py

import yaml
from pathlib import Path
from sqlalchemy import inspect
from database.db_config import get_db_engine

def get_enhanced_schema() -> str:
    """
    Loads custom table/column descriptions and combines them with the actual
    DB schema to create an enhanced, context-rich schema prompt for the LLM.

    Returns:
        A formatted string describing the database schema with business context.
    """
    engine = get_db_engine()
    inspector = inspect(engine)
    
    # Load the custom descriptions from our YAML file
    prompt_path = Path(__file__).parent.parent.parent / "prompts" / "schema_descriptions.yaml"
    with open(prompt_path, 'r') as f:
        custom_descriptions = yaml.safe_load(f).get('tables', [])
    
    desc_map = {item['name']: item for item in custom_descriptions}

    output = ["Here is the database schema you must use to answer the user's question:"]
    
    table_names = inspector.get_table_names()
    
    for table_name in table_names:
        output.append(f"\n--- Table: {table_name} ---")
        
        # Add custom table description if available
        if table_name in desc_map and 'description' in desc_map[table_name]:
            output.append(f"Description: {desc_map[table_name]['description']}")
            
        # Add table schema (DDL)
        columns = inspector.get_columns(table_name)
        col_defs = []
        custom_col_descs = {col['name']: col['description'] for col in desc_map.get(table_name, {}).get('columns', [])}

        for col in columns:
            col_name = col['name']
            col_type = col['type']
            # Add custom column description if available
            col_desc = f" -- {custom_col_descs[col_name]}" if col_name in custom_col_descs else ""
            col_defs.append(f"  {col_name} ({col_type}){col_desc}")
            
        output.append("Columns:\n" + "\n".join(col_defs))
        
    return "\n".join(output)

if __name__ == '__main__':
    # Test the schema retriever
    enhanced_schema = get_enhanced_schema()
    print(enhanced_schema)
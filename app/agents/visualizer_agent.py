# insightgpt/app/agents/visualizer_agent.py

import httpx
import pandas as pd
import plotly.express as px
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.state import AgentState

def generate_chart_from_data(state: AgentState) -> dict:
    """
    Analyzes the raw data and user question to generate the best possible
    Plotly chart, returning it as a PNG image in bytes.
    This version includes the definitive fix for the chart title and theme.
    """
    print("---GENERATING VISUALIZATION---")
    
    raw_result = state.get('raw_result')
    if not raw_result or not isinstance(raw_result, list):
        print("No valid data found to visualize.")
        return {}

    df = pd.DataFrame(raw_result)
    
    if df.empty or (df.shape[0] == 1 and df.shape[1] == 1):
        print("Data is a single metric or empty. Skipping chart generation.")
        return {}
        
    prompt_template = """
Given the user's original question and a dataset, choose the best chart type to visualize the answer.
Your choices are: 'bar', 'line', 'pie'.

You must also decide which column(s) from the dataset should be used for the x and y axes (or names and values for a pie chart).

User Question: {question}
Dataset Columns: {columns}

Provide your response as a single line of comma-separated values in the following format:
CHART_TYPE,X_COLUMN,Y_COLUMN
Example: bar,product_name,total_sales
Example: pie,country,customer_count

Your decision:
"""
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    http_client = httpx.Client(verify=False)
    llm = ChatOpenAI(model="gpt-4o", temperature=0.0, http_client=http_client)
    chain = prompt | llm

    # The original question is the first message in the state
    original_question = state['messages'][0].content
    
    response = chain.invoke({
        "question": original_question,
        "columns": ", ".join(df.columns)
    })
    
    llm_output = response.content
    if not isinstance(llm_output, str):
        print(f"LLM output was not a string, skipping chart generation. Output: {llm_output}")
        return {}
        
    try:
        parts = [part.strip() for part in llm_output.strip().split(',')]
        if len(parts) != 3:
            raise ValueError("LLM output did not contain 3 parts (chart_type, col1, col2)")
        chart_type, col1, col2 = parts
        
        print(f"LLM decided to create a '{chart_type}' chart with columns '{col1}' and '{col2}'.")
        
       
        # Bypassing the title altogether
        template = "plotly_dark"
        # template = "plotly_white"
        
        fig = None
        if chart_type == 'pie':
            fig = px.pie(df, names=col1, values=col2, template=template)
        elif chart_type == 'bar':
            fig = px.bar(df, x=col1, y=col2, template=template)
        elif chart_type == 'line':
            fig = px.line(df, x=col1, y=col2, template=template)
        
        if fig:
            # Update figure layout for better readability on a dark theme
            fig.update_layout(
                font_color="white",
                title_font_color="white",
                legend_title_font_color="white"
            )
            png_image = fig.to_image(format="png")
            return {"chart_image": png_image}

    except Exception as e:
        print(f"An error occurred during chart generation: {e}")
    
    return {}

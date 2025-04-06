import pandas as pd
import streamlit as st
import google.generativeai as genai
import textwrap
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Liquor Sales Analytics Assistant",
    page_icon="🥃",
    layout="wide"
)

# Sidebar for app controls
with st.sidebar:
    st.title("Liquor Sales Analytics")
    st.markdown("Use this tool to analyze Iowa liquor sales data using AI.")
    
    # API key input (with save option)
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    
    # api_key = st.text_input("Enter Gemini API Key:", value=st.session_state.api_key, type="password")
    # if api_key:
    #     st.session_state.api_key = api_key
    
    st.divider()
    
    # Display data dictionary
    with st.expander("📊 Data Dictionary", expanded=False):
        data_dict_df = pd.read_csv('./data/data_dict.csv')
        st.dataframe(data_dict_df, use_container_width=True)
    
    # Display sample data
    with st.expander("🔍 Sample Data", expanded=False):
        transaction_df = pd.read_csv('./data/transactions.csv')
        st.dataframe(transaction_df.head(5), use_container_width=True)

# Setup database connection
@st.cache_data
def setup_db():
    transaction_df = pd.read_csv('./data/transactions.csv')
    # Convert date to datetime
    transaction_df['date'] = pd.to_datetime(transaction_df['date'])
    
    data_dict_df = pd.read_csv('./data/data_dict.csv')
    data_dict_text = '\n'.join('- '+data_dict_df['column_name']+
                            ': '+data_dict_df['data_type']+
                            '. '+data_dict_df['description'])
    example_record = transaction_df.head(3).to_string()

    df_name = 'transaction_df'

    return transaction_df, data_dict_df, data_dict_text, df_name, example_record

# Configure Gemini model
def configure_gemini():
    try:
        if st.session_state.api_key:
            genai.configure(api_key=st.session_state.api_key)
            return genai.GenerativeModel('gemini-2.0-flash-lite')
        else:
            try:
                key = st.secrets["gemini_api_key"]
                genai.configure(api_key=key)
                return genai.GenerativeModel('gemini-2.0-flash-lite')
            except:
                st.sidebar.warning("Please enter a valid API key in the sidebar.")
                return None
    except Exception as e:
        st.sidebar.error(f"Error configuring Gemini: {e}")
        return None

# Generate prompt with RAG context
def gen_with_rag(question):
    transaction_df, data_dict_df, data_dict_text, df_name, example_record = setup_db()
    
    prompt = f"""
    You are a helpful Python code generator specializing in data analysis.
    Your goal is to write Python code snippets based on the user's question
    and the provided DataFrame information about Iowa liquor sales.

    Here's the context:
    **User Question:**
    {question}
    
    **DataFrame Name:**
    {df_name}
    
    **DataFrame Details (data dictionary):**
    {data_dict_text}
    
    **Sample Data (Top 3 Rows):**
    {example_record}

    **Instructions:**
    1. Write Python code that addresses the user's question by querying or manipulating the DataFrame.
    2. The code will be executed, so ensure it's correct and handles edge cases.
    3. Always convert the 'date' column to datetime if it's not already.
    4. Store the result in a variable named `ANSWER`.
    5. Include visualizations using Streamlit's native charting functions (st.bar_chart, st.line_chart, st.area_chart) 
       or Plotly for more complex visualizations.
    6. Format your output as follows:
       - First provide a brief explanation of your approach
       - Then provide the code in a markdown code block
       - Then explain what the code does step by step
    7. If the user's question is unclear, ask for clarification rather than making assumptions.
    8. Don't include code for loading data - assume the DataFrame is already available as `{df_name}`.
    9. DO NOT use matplotlib or seaborn for visualizations. Only use Streamlit's native charts or Plotly.
    
    Remember that this is Iowa liquor sales data containing information about sales transactions, 
    including details like invoice numbers, dates, store information, product details, and sales figures.

    **Example:**
    If the user asks: "Show me the rows where the 'age' column is
    greater than 30."
    And the DataFrame has an 'age' column.
    The generated code should look something like this (inside the
    `exec()` string):
    ```python
    query_result = {df_name}[{df_name}['age'] > 30]
    """
    return prompt

# Execute generated code and display results
def execute_code_and_show_results(code_to_execute, transaction_df):
    try:
        # Create local namespace with the DataFrame and streamlit
        local_namespace = {
            "transaction_df": transaction_df, 
            "pd": pd,
            "st": st
        }
        
        # Execute the code in the local namespace
        exec(code_to_execute, globals(), local_namespace)
        
        # Try to get the ANSWER variable from the local namespace
        if "ANSWER" in local_namespace:
            result = local_namespace["ANSWER"]
            
            # Display the result based on its type
            if isinstance(result, pd.DataFrame):
                st.write("### Result DataFrame:")
                st.dataframe(result, use_container_width=True)
            elif isinstance(result, (list, tuple)):
                st.write("### Result List:")
                for item in result:
                    st.write(item)
            elif str(type(result)).find("plotly") != -1:
                # It's a plotly figure
                st.write("### Visualization:")
                st.plotly_chart(result, use_container_width=True)
            else:
                st.write("### Result:")
                st.write(result)
                
            return True
        else:
            st.warning("Code executed but no ANSWER variable was defined.")
            return False
            
    except Exception as e:
        st.error(f"Error executing code: {e}")
        return False

# Main app content
st.title("Liquor Sales Analytics Assistant")
st.markdown("""
Ask questions about the Iowa liquor sales data and get AI-generated insights.
The assistant will write and execute code to answer your questions.
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # If there's code to display
        if "code" in message:
            with st.expander("View Generated Code"):
                st.code(message["code"], language="python")

# Setup model
model = configure_gemini()

# User input
if prompt := st.chat_input("Ask a question about the liquor sales data:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response if model is configured
    if model:
        with st.chat_message("assistant"):
            with st.spinner("Generating response..."):
                # Load data
                transaction_df, _, _, _, _ = setup_db()
                
                # Generate prompt with RAG context
                rag_prompt = gen_with_rag(prompt)
                
                # Get response from Gemini
                response = model.generate_content(rag_prompt)
                response_text = response.text
                
                # Display explanation part
                parts = response_text.split("```python")
                if len(parts) > 1:
                    explanation = parts[0].strip()
                    code_part = parts[1].split("```")[0].strip()
                    
                    # Show explanation
                    st.markdown(explanation)
                    
                    # Show code
                    st.code(code_part, language="python")
                    
                    # Execute code and show results
                    with st.spinner("Executing code..."):
                        execute_code_and_show_results(code_part, transaction_df)
                    
                    # If there's post-code explanation
                    if len(parts) > 2:
                        st.markdown(parts[2].strip())
                    
                    # Save to chat history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": explanation + 
                                  (parts[2].strip() if len(parts) > 2 else ""),
                        "code": code_part
                    })
                else:
                    # No code in the response, just show text
                    st.markdown(response_text)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response_text
                    })
    else:
        with st.chat_message("assistant"):
            st.markdown("Please provide a valid Gemini API key in the sidebar to continue.")
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "Please provide a valid Gemini API key in the sidebar to continue."
            })
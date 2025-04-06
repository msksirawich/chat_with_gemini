import pandas as pd
import streamlit as st
import google.generativeai as genai
import textwrap
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Pokémon Data Analyzer",
    page_icon="🐲",
    layout="wide"
)

# Setup data dictionary
@st.cache_data
def create_data_dict():
    return [
        {"column_name": "abilities", "data_type": "String", "description": "Pokémon abilities separated by comma"},
        {"column_name": "against_bug", "data_type": "Float", "description": "Effectiveness multiplier of Bug-type moves against this Pokémon"},
        {"column_name": "against_dark", "data_type": "Float", "description": "Effectiveness multiplier of Dark-type moves against this Pokémon"},
        {"column_name": "against_dragon", "data_type": "Float", "description": "Effectiveness multiplier of Dragon-type moves against this Pokémon"},
        {"column_name": "against_electric", "data_type": "Float", "description": "Effectiveness multiplier of Electric-type moves against this Pokémon"},
        {"column_name": "against_fairy", "data_type": "Float", "description": "Effectiveness multiplier of Fairy-type moves against this Pokémon"},
        {"column_name": "against_fight", "data_type": "Float", "description": "Effectiveness multiplier of Fighting-type moves against this Pokémon"},
        {"column_name": "against_fire", "data_type": "Float", "description": "Effectiveness multiplier of Fire-type moves against this Pokémon"},
        {"column_name": "against_flying", "data_type": "Float", "description": "Effectiveness multiplier of Flying-type moves against this Pokémon"},
        {"column_name": "against_ghost", "data_type": "Float", "description": "Effectiveness multiplier of Ghost-type moves against this Pokémon"},
        {"column_name": "against_grass", "data_type": "Float", "description": "Effectiveness multiplier of Grass-type moves against this Pokémon"},
        {"column_name": "against_ground", "data_type": "Float", "description": "Effectiveness multiplier of Ground-type moves against this Pokémon"},
        {"column_name": "against_ice", "data_type": "Float", "description": "Effectiveness multiplier of Ice-type moves against this Pokémon"},
        {"column_name": "against_normal", "data_type": "Float", "description": "Effectiveness multiplier of Normal-type moves against this Pokémon"},
        {"column_name": "against_poison", "data_type": "Float", "description": "Effectiveness multiplier of Poison-type moves against this Pokémon"},
        {"column_name": "against_psychic", "data_type": "Float", "description": "Effectiveness multiplier of Psychic-type moves against this Pokémon"},
        {"column_name": "against_rock", "data_type": "Float", "description": "Effectiveness multiplier of Rock-type moves against this Pokémon"},
        {"column_name": "against_steel", "data_type": "Float", "description": "Effectiveness multiplier of Steel-type moves against this Pokémon"},
        {"column_name": "against_water", "data_type": "Float", "description": "Effectiveness multiplier of Water-type moves against this Pokémon"},
        {"column_name": "attack", "data_type": "Integer", "description": "Base Attack stat"},
        {"column_name": "base_egg_steps", "data_type": "Integer", "description": "Number of steps required to hatch an egg of this Pokémon"},
        {"column_name": "base_happiness", "data_type": "Integer", "description": "Base happiness when caught"},
        {"column_name": "base_total", "data_type": "Integer", "description": "Sum of all base stats"},
        {"column_name": "capture_rate", "data_type": "String", "description": "Capture rate (higher is easier to catch)"},
        {"column_name": "classfication", "data_type": "String", "description": "Classification of the Pokémon (e.g., 'Seed Pokémon')"},
        {"column_name": "defense", "data_type": "Integer", "description": "Base Defense stat"},
        {"column_name": "experience_growth", "data_type": "Integer", "description": "Experience growth rate"},
        {"column_name": "height_m", "data_type": "Float", "description": "Height in meters"},
        {"column_name": "hp", "data_type": "Integer", "description": "Base HP (Hit Points) stat"},
        {"column_name": "japanese_name", "data_type": "String", "description": "Japanese name of the Pokémon"},
        {"column_name": "name", "data_type": "String", "description": "English name of the Pokémon"},
        {"column_name": "percentage_male", "data_type": "Float", "description": "Percentage of this Pokémon species that are male"},
        {"column_name": "pokedex_number", "data_type": "Integer", "description": "National Pokédex number (ID)"},
        {"column_name": "sp_attack", "data_type": "Integer", "description": "Base Special Attack stat"},
        {"column_name": "sp_defense", "data_type": "Integer", "description": "Base Special Defense stat"},
        {"column_name": "speed", "data_type": "Integer", "description": "Base Speed stat"},
        {"column_name": "type1", "data_type": "String", "description": "Primary type of the Pokémon"},
        {"column_name": "type2", "data_type": "String", "description": "Secondary type of the Pokémon (if any)"},
        {"column_name": "weight_kg", "data_type": "Float", "description": "Weight in kilograms"},
        {"column_name": "generation", "data_type": "Integer", "description": "Generation when this Pokémon was introduced (1-7)"},
        {"column_name": "is_legendary", "data_type": "Integer", "description": "Whether this Pokémon is legendary (1) or not (0)"}
    ]

# Sidebar for app controls
with st.sidebar:
    st.title("Pokémon Analyzer")
    st.markdown("Use this tool to analyze Pokémon data using AI.")
    
    # API key input (with save option)
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    
    api_key = st.text_input("Enter Gemini API Key:", value=st.session_state.api_key, type="password")
    if api_key:
        st.session_state.api_key = api_key
    
    st.divider()
    
    # Display data dictionary
    with st.expander("📊 Data Dictionary", expanded=False):
        data_dict_df = pd.DataFrame(create_data_dict())
        st.dataframe(data_dict_df, use_container_width=True, hide_index=True)
    
    # Display sample data
    with st.expander("🔍 Sample Data", expanded=False):
        pokemon_df = pd.read_csv('./data/pokemon.csv')
        st.dataframe(pokemon_df.head(5), use_container_width=True, hide_index=True)

# Setup database connection
@st.cache_data
def setup_db():
    pokemon_df = pd.read_csv('./data/pokemon.csv')
    
    data_dict = create_data_dict()
    data_dict_df = pd.DataFrame(data_dict)
    data_dict_text = '\n'.join('- '+data_dict_df['column_name']+
                            ': '+data_dict_df['data_type']+
                            '. '+data_dict_df['description'])
    example_record = pokemon_df.head(3).to_string(index=False)

    df_name = 'pokemon_df'

    return pokemon_df, data_dict_df, data_dict_text, df_name, example_record

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
    pokemon_df, data_dict_df, data_dict_text, df_name, example_record = setup_db()
    
    prompt = f"""
    You are an expert Python data scientist specializing in Pokémon analysis and visualization.
    Your task is to generate executable, production-quality Python code that answers the user's question
    about the Pokémon dataset.

    ## Context
    **User Query:**
    {question}

    **Available Data:**
    - DataFrame variable name: `{df_name}`
    - This DataFrame contains complete information about Pokémon, their stats, types, and battle characteristics
    - The DataFrame is already loaded and ready to use

    **Data Dictionary:**
    {data_dict_text}

    **Sample Data:**
    {example_record}

    ## Requirements
    1. Generate clean, efficient Python code that directly addresses the user's question
    2. Follow these implementation guidelines:
    - Store your final result in a variable named `ANSWER`
    - NEVER show index columns in output (use `.reset_index(drop=True)` for DataFrames or `index=False` in display methods)
    - Use ONLY Streamlit's native visualization functions (st.bar_chart, st.line_chart, st.area_chart)
    - DO NOT use Plotly, matplotlib, or seaborn
    - Handle all edge cases and potential errors gracefully
    - Optimize for readability and performance
    - Do not include code to load the DataFrame - it's already available as `{df_name}`

    3. For visualizations:
    - Use Streamlit's built-in charts (st.bar_chart, st.line_chart, st.area_chart) for all visualizations
    - Prepare data in the appropriate format for Streamlit's native charts
    - When needed, create multiple charts to show different aspects of the data
    - Always include clear titles and labels using st.write() or st.markdown() before charts

    4. Add context and insights to numerical results:
    - When comparing Pokémon, explain the significance of the differences
    - When analyzing type advantages, include strategic implications
    - For stat analysis, relate findings to gameplay mechanics

    ## Response Format
    Your complete response should include:

    1. A brief, clear explanation of your approach (2-3 sentences)
    2. Your code solution in a Python code block (properly formatted and indented)
    3. A step-by-step explanation of how your code works
    4. Any additional insights about the results that would be valuable to a Pokémon trainer or analyst

    Remember that your code will be executed directly, so it must run without errors and produce clear, insightful results with no index columns visible in any output.
    """
    
    return prompt

# Execute generated code and display results
def execute_code_and_show_results(code_to_execute, pokemon_df):
    try:
        # Create local namespace with the DataFrame and streamlit
        local_namespace = {
            "pokemon_df": pokemon_df, 
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
                st.dataframe(result, use_container_width=True, hide_index=True)
            elif isinstance(result, (list, tuple)):
                st.write("### Result List:")
                for item in result:
                    st.write(item)
            else:
                st.write("### Result:")
                st.write(result)
                
            return True
        else:
            st.warning("Code executed but no ANSWER variable was defined.")
            return False
            
    except Exception as e:
        st.error(f"Pokemon โกรธแล้ว Trainer ไม่ถามแบบนี้กัน")
        # return False


try:

    # Main app content
    st.title("Pokémon Data Analyzer")
    st.markdown("""
    Ask questions about the Pokémon dataset and get AI-generated insights.
    The assistant will write and execute code to answer your questions.

    Some example questions:
    - Is it possible to build a classifier to identify legendary Pokemon?
    - How does height and weight of a Pokemon correlate with its various base stats?
    - What factors influence the Experience Growth and Egg Steps? Are these quantities correlated?
    - Which type is the strongest overall? Which is the weakest?
    - Which type is the most likely to be a legendary Pokemon?
    - Can you build a Pokemon dream team? A team of 6 Pokemon that inflicts the most damage while remaining relatively impervious to any other team of 6 Pokemon.
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
    if prompt := st.chat_input("Ask a question about the Pokémon data:"):
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
                    pokemon_df, _, _, _, _ = setup_db()
                    
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
                            execute_code_and_show_results(code_part, pokemon_df)
                        
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

except Exception as e:
    st.error(f"Pokemon โกรธแล้ว Trainer ไม่ถามแบบนี้กัน")
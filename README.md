# Pokémon Data Analyzer

A Streamlit application powered by Gemini AI to analyze and visualize Pokémon data.

![Pokémon Data Analyzer](https://raw.githubusercontent.com/username/pokemon-analyzer/main/images/screenshot.png)

## Overview

Pokémon Data Analyzer is an interactive web application that allows users to ask questions about Pokémon data in natural language. The application uses Google's Gemini AI to:

1. Interpret user questions about Pokémon
2. Generate optimized Python code to answer those questions
3. Execute the code and display results in an easy-to-understand format
4. Provide insights and explanations about the results

## Features

- **Natural Language Interface**: Ask questions about Pokémon in plain English
- **AI-Powered Code Generation**: Automatically generates Python code to analyze the data
- **Interactive Visualizations**: View your results through Streamlit's native charts
- **Comprehensive Dataset**: Includes data on all Pokémon up through Generation 7, including:
  - Base stats (HP, Attack, Defense, Speed, etc.)
  - Type effectiveness
  - Physical attributes (height, weight)
  - Classification information
  - Legendary status
  - And much more!
- **Persistent Chat History**: Continue your analysis across sessions

## Sample Questions

You can ask the application questions like:

- Which Pokémon have the highest attack stat?
- Compare the average stats between legendary and non-legendary Pokémon
- What are the most common Pokémon types?
- Which Pokémon have the best defense against fire-type moves?
- Is it possible to build a classifier to identify legendary Pokémon?
- How does height and weight correlate with base stats?
- What factors influence the Experience Growth and Egg Steps?
- Which type is the strongest overall? Which is the weakest?
- Which type is the most likely to be a legendary Pokémon?
- Can you build a Pokémon dream team?

## Installation

### Prerequisites

- Python 3.9+
- pip (Python package installer)
- Google Gemini API key

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/username/pokemon-analyzer.git
   cd pokemon-analyzer
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.streamlit/secrets.toml` file with your Gemini API key (optional):
   ```
   gemini_api_key = "your-api-key-here"
   ```

### Running the Application

Start the application with:

```
streamlit run app.py
```

Then open your browser and navigate to `http://localhost:8501`.

## Project Structure

```
pokemon-analyzer/
├── app.py                  # Main application file
├── data/
│   ├── pokemon.csv         # Pokémon dataset
│   └── data_dict.csv       # Data dictionary for the dataset
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── secrets.toml        # API keys (not included in repo)
└── README.md               # This file
```

## Using Your Own API Key

You can provide your Gemini API key in two ways:

1. Create a `.streamlit/secrets.toml` file with your API key:
   ```
   gemini_api_key = "your-api-key-here"
   ```

2. Enter your API key directly in the sidebar of the application.

## Requirements

The application requires the following Python packages:

- streamlit
- pandas
- google-generativeai
- python-dotenv

A complete list of dependencies is available in the `requirements.txt` file.

## Limitations

- Visualizations are limited to Streamlit's native charts (bar_chart, line_chart, area_chart)
- Analysis is limited to the data available in the dataset
- The Gemini API may have usage limits based on your access level

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Pokémon data sourced from [Kaggle](https://www.kaggle.com/datasets/rounakbanik/pokemon)
- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Gemini AI](https://ai.google.dev/)

---

*Note: Pokémon and all related properties are trademarks of Nintendo, The Pokémon Company, and Game Freak.*
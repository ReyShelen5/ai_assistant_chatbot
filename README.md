Project Description:
    -Ask Your Data is an interactive Streamlit-based web application that lets users converse with their PostgreSQL database using natural language. It combines the power of Google's Gemini AI (via LangChain) with SQL generation and execution, allowing non-technical users to gain insights from their databases with ease.

Features
    -Chat with your database using plain English.

    -LLM-powered SQL generation via Gemini 1.5 Pro (Google Generative AI).

    -Schema-aware query construction using LangChain’s SQL agents.

    -Live SQL execution and result summarization.

    -Custom database configuration through a sidebar settings panel.

    -Dark-themed UI with custom CSS styling for a modern chat experience.

Tech Stack used:
    -Frontend	Streamlit
    -AI/LLM	    LangChain + Gemini 1.5 Pro
    -Database	PostgreSQL
    -Others	    Python, dotenv, psycopg2
(Their versions are specified in the requirement.txt)

The flow of the project:

    -The user connects to a PostgreSQL database by providing connection details in the sidebar.

    -The system fetches the table schema using LangChain's SQLDatabase utility.

    -The user's natural language question is processed by the Gemini model to generate a valid SQL query.

    -The query is executed, and the results are passed back to Gemini to generate a natural language response.

    -The conversation is maintained and displayed on a left-aligned chat interface using Streamlit’s chat components.

Sample Input Flow:
    User Input:
        -Show me the top 5 customers by payment amount.

    App Flow:
        → Gemini generates SQL → App runs the SQL on PostgreSQL → Result is summarized back to the user in plain English.

Folder Structure:
    ask-your-data/
        ├── chat_assistant.py
        ├── requirements.txt
        |── README.md







import streamlit as st
st.set_page_config(
    page_title="Ask Your Data 💬",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Inject CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }
    input, textarea {
        background-color: #1f1f1f !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 5px;
    }
    .stTextInput > div > div > input {
        background-color: #1f1f1f;
        color: white;
    }
    .stButton > button {
        background-color: teal;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stButton > button:hover {
        background-color: #008080;
    }
    </style>
""", unsafe_allow_html=True)

# Create two columns: Chat on left, Settings on right
chat_col, settings_col = st.columns([3, 1])

from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import AIMessage , HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser





load_dotenv()
st.title("Chat Anywhere With Your Database")

def init_database(user:str,password:str,host:str,port:str,database:str)-> SQLDatabase:
    db_uri=f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)

with st.sidebar:
    st.subheader("Change Settings")
    st.write("This is a simple chat application with PostgreSQL. Connect to your databases and start chatting")
    st.text_input("Host",value="localhost",key="Host")
    st.text_input("Port",value="5432",key="Port")
    st.text_input("User",value="postgres",key="User")
    st.text_input("Password",type="password",value="reya2006#",key="Password")
    st.text_input("Database",value="pagila",key="Database")

    if st.button("Connect"):
        with st.spinner("Connecting to your database"):
            db=init_database(st.session_state["User"],
                                st.session_state["Password"],
                                st.session_state["Host"],
                                st.session_state["Port"],
                                st.session_state["Database"])
        st.session_state.db =db
        st.success("Successfully connected to your database")




def get_sql_chain(db):
    template = """You are a data analyst at a company. You are interacting with a user who is asking you questions about the company’s database.  
    Based on the table schema below, write a SQL query that would answer the user’s question. Take the conversation history into account.

    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}

    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.

    For example:  
    Question: which 3 artists have the most tracks?  
    SQL Query: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3;

    Question: Name 10 artists  
    SQL Query: SELECT Name FROM Artist LIMIT 10;

    Your turn:

    Question: {question}  
    SQL Query:
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-latest")

    def get_schema(_):
        return db.get_table_info()
    return(
        RunnablePassthrough.assign(schema=get_schema)
        |prompt
        |llm
        |StrOutputParser()
    )
def get_response(user_query:str, db : SQLDatabase, chat_history: list):
    sql_chain = get_sql_chain(db)
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company’s database.
    Based on the table schema below, question, sql query, and sql response, write a natural language response.
    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}
    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}"""

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-latest")

    chain=(
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema = lambda _:db.get_table_info(),
            response = lambda vars:db.run(vars["query"])
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain.invoke({
        "question":user_query,
        "chat_history":chat_history
    })



if "chat_history" not in st.session_state:
    st.session_state.chat_history= [
        AIMessage(content="Hello!! This is your SQL assistant. Ask anything about your database.")]



for message in st.session_state.chat_history:
    if isinstance(message,AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message,HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)


user_query = st.chat_input("Type to chat")
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)
    with st.chat_message("AI"):
        response= get_response(user_query,st.session_state.db,st.session_state.chat_history)
        st.markdown(response)
        
    st.session_state.chat_history.append(AIMessage(content=response))

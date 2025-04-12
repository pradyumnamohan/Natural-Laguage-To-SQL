from dotenv import load_dotenv
import os
import sqlite3
import streamlit as st
import google.generativeai as genai

load_dotenv()  

# Set up the Google Generative AI API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(prompt, question):
    try:
        response = model.generate_content(prompt = prompt, question=question)
        parts = response.candidates[0].content.parts
        text = ' '.join([part.text for part in parts])
        return text
    except Exception as e:
        st.error(f"Error generating text: {e}")
        return None

def read_sql_query(sql, db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.commit()
        return data
    except sqlite3.Error as e:
        st.error(f"SQL error: {e}")
        return None
    finally:
        connection.close()

prompt = """
You are an expert in converting english questions to SQL queries.
The SQL database has the table employee with the following columns:
EMP_NAME varchar(50), EMP_ID varchar(50), DESIGNATION varchar(50), EMP_AGE int
\n\n

For Example, \n
Example 1: How many entries of records are present?
the SQL query is: SELECT COUNT(*) FROM employee; \n\n

Example 2: What is the name of the employee with ID E123?
the SQL query is: SELECT EMP_NAME FROM employee WHERE EMP_ID = 'E123'; \n\n

Example 3: Tell me all the employees with designation as Software Engineer?
the SQL query is: SELECT * FROM employee WHERE DESIGNATION = 'Software Engineer'; \n\n

also the SQL query should not have  ``` in the begning and end of the query.

if generated SQL query contains triple quotes, remove them, and give the SQL query without triple quotes.

You should not allow DML commands like INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, TRUNCATE etc.
\n\n
"""
st.set_page_config(page_title="AskSQL")
st.header("Gemini Application to retrieve SQL data using English")
question=st.text_input("Enter your question: ",key="input")
submit=st.button("Submit")

if submit:
    response=get_gemini_response(prompt, question)
    print(response)
    response=read_sql_query(response,"emp.db")
    st.subheader("The LLM response is")
    for row in response:
        st.write(row)
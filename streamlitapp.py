import os
import json
import pandas as pd
import traceback
import streamlit as st
import PyPDF2

from utils import read_file, get_table_data
from logger import logging, LOG_FILEPATH
from langchain.callbacks import get_openai_callback
from main import generate_evaluate_chain

RESPONSE_JSON_PATH = os.path.join(os.path.dirname(__file__), 'Response.json')

# Load the response JSON file
try:
    with open(RESPONSE_JSON_PATH, 'r') as file:
        RESPONSE_JSON = json.load(file)
except FileNotFoundError:
    logging.error(f"Response JSON file not found at {RESPONSE_JSON_PATH}")
    st.error("Response JSON file not found. Please check the file path.")
    RESPONSE_JSON = {}
except json.JSONDecodeError:
    logging.error(f"Error decoding the JSON file at {RESPONSE_JSON_PATH}")
    st.error("Error decoding the JSON file. Please check the file format.")
    RESPONSE_JSON = {}

st.title("QuizFast⚡💥") 

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or a txt file")
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    subject = st.text_input("Insert subject", max_chars=20)
    tone = st.text_input("Complexity level of Questions", max_chars=20, placeholder="simple")
    button = st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading...."):
            try:
                text = read_file(uploaded_file)
                
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain({
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    })
                
                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        logging.info(f"Table data: {table_data}")
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            st.text_area(label="Review", value=response["review"])
                        else:
                            logging.error("Error in the table data format")
                            st.error("Error in the table data")
                else:
                    st.write(response)
                
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("An error occurred while generating MCQs. Please try again.")







# import os
# import json
# import pandas as pd
# import traceback

# from utils import read_file, get_table_data
# from logger import logging,LOG_FILEPATH
# from langchain.callbacks import get_openai_callback
# from main import generate_evaluate_chain
# import streamlit as st
# import PyPDF2
# RESPONSE_JSON_PATH = os.path.join(os.path.dirname(__file__), 'Response.json')
# try:
#     with open(RESPONSE_JSON_PATH, 'r') as file:
#         RESPONSE_JSON = json.load(file)
# except FileNotFoundError:
#     logging.error(f"Response JSON file not found at {RESPONSE_JSON_PATH}")
#     st.error("Response JSON file not found. Please check the file path.")
#     RESPONSE_JSON = {}
# except json.JSONDecodeError:
#     logging.error(f"Error decoding the JSON file at {RESPONSE_JSON_PATH}")
#     st.error("Error decoding the JSON file. Please check the file format.")
#     RESPONSE_JSON = {}


# st.title("QuizFast⚡💥") 

# with st.form("user_inputs"):
#     uploaded_file = st.file_uploader("Upload a PDF or a txt file")

#     mcq_count = st.number_input("No. of MCQs",min_value = 3, max_value =50)

#     subject = st.text_input("Insert subject",max_chars = 20)

#     tone = st.text_input("Complexity level of Questions",max_chars=20, placeholder="simple")

#     button = st.form_submit_button("Create MCQs")

#     if button and uploaded_file is not None and mcq_count and subject and tone:
#         with st.spinner("loading...."):
#             try:
#                 text = read_file(uploaded_file)

#                 with get_openai_callback() as cb:
#                     response = generate_evaluate_chain(
#                         {
#                             "text":text,
#                             "number":mcq_count,
#                             "subject":subject,
#                             "tone": tone,
#                             "response_json":json.dumps(RESPONSE_JSON)
#                         }
#                     )

#             except Exception as e:
#                 traceback.print_exception(type(e), e, e.__traceback__)
#                 st.error("Error")
#     # else:
#     #     print(f"Total Tokens : {cb.total_tokens}")
#     #     print(f"Prompt Tokens : {cb.prompt_tokens}")
#     #     print(f"Completion Tokens : {cb.completion_tokens}")
#     #     print(f"Total cose : {cb.total_cost}")
#         if isinstance(response,dict):
#             quiz = response.get("quiz",None)
#             if quiz is not None:
#                 table_data = get_table_data(quiz)
#                 logging.info(f"Table data: {table_data}")
#                 if table_data is not None:
#                     df=pd.DataFrame(table_data)
#                     df.index=df.index+1
#                     st.table(df)
#                     st.text_area(label="Review", value = response["review"])
#                 else:
#                     logging.error("Error in the table data format")
#                     st.error("Error in the table data")


#         #     else:
#         #         st.write(response)
#         # if isinstance(response, dict):
#         #     quiz = response.get("quiz", None)
#         #     if quiz is not None:
#         #         table_data = get_table_data(quiz)
#         #         logging.info(f"Table data type: {type(table_data)}") 
#         #         logging.info(f"Table data: {table_data}")  # Debugging statement to log the content of table_data

#         #         if table_data and isinstance(table_data, list) and all(isinstance(i, dict) for i in table_data):
#         #             try:
#         #                 df = pd.DataFrame(table_data)
#         #                 df.index = df.index + 1
#         #                 st.table(df)
#         #                 st.text_area(label="Review", value=response["review"])
#         #             except ValueError as ve:
#         #                 logging.error(f"Error creating DataFrame: {ve}")
#         #                 st.error("Error creating DataFrame. Please check the table data format.")
#         #         else:
#         #             logging.error("Error in the table data format")
#         #             st.error("Error in the table data format")
#         #     else:
#         #         st.write(response)
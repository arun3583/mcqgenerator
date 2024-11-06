import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.mcqgenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging


with open("response.json", "r") as f:
    RESPONSE_JSON = json.load(f)


st.title("MCQ Generator using Langchain")

with st.form("user_input"):
    uploaded_file = st.file_uploader("Upload a pdf or text file", type=["pdf", "txt"])
    mcq_count = st.number_input("Number of MCQs", min_value=5, max_value=10)
    subject = st.text_input("Subject", max_chars=20)
    tone = st.text_input("Complexity level of the quiz", max_chars=20, placeholder="Simple")
    button = st.form_submit_button("Generate MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text = read_file(uploaded_file)
                
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error(f"Error generating MCQs: {e}")
            else:
                logging.info(f"Total Tokens: {cb.total_tokens}")
                logging.info(f"Total Cost: ${cb.total_cost}")
                logging.info(f"Total Prompt Cost: ${cb.prompt_tokens}")
                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table = get_table_data(quiz)
                        if table:
                            df = pd.DataFrame(table)
                            df.index = df.index + 1
                            st.table(df)
                            st.text_area(label="Review", value=response.get("review", None), height=200)
                        else:
                            st.error("Error generating table")
                else:
                    st.write(response)
                            

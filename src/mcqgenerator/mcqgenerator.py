import json
import os
import traceback

import pandas as pd
from dotenv import load_dotenv
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging


# load environmental variable
load_dotenv()

key = os.getenv("GROQ_API_KEY")


llm = ChatGroq(api_key=key, model="mixtral-8x7b-32768", temperature=1, max_retries=2)

template="""
Text: {text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and usel it as a guide. \
Ensure to make {number} MCQs
### RESPONSE JSON
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=template
)


quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)


template2 = """
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}
Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(input_variables=["subject", "quiz"], template=template2)

review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain], input_variables=["text", "number", "subject", "tone", "response_json"], output_variables=["quiz", "review"], verbose=True
)


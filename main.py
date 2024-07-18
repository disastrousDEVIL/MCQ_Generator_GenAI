import os
import json
import pandas as pd
import traceback
import time
from secretkey import OPENAI_API_KEY

from utils import read_file, get_table_data
from logger import logging

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import PyPDF2

os.environ['OPENAI_API_KEY']=OPENAI_API_KEY
llm=ChatOpenAI(temperature=0.5,max_tokens=3500,model="gpt-4")

TEMPLATE="""
Text: {text}
You are an expert MCQ maker. Given the above text, create a quiz of {number} multiple choice questions for {subject} students in a {tone} tone. Ensure the questions are not repeated and conform to the text. Format your response like RESPONSE_JSON below and use it as a guide. Ensure to create {number} MCQs.

###RESPONSE_JSON
{response_json}

"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
    )

quiz_chain=LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)


TEMPLATE2="""
 Given a Multiple Choice Quiz for {subject} students
Quiz_MCQs:
{quiz} , in JSOn format , read it carefully and justify the answers in 50 words total
"""


quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE2)

review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

generate_evaluate_chain=SequentialChain(chains=[quiz_chain,review_chain], input_variables=["text", "number", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True,)
# generate_evaluate_chain.invoke({"text":"The Bombay Stock Exchange (BSE) is renowned for its rigorous regulatory framework, designed to ensure a transparent, fair, and efficient market. As India's oldest stock exchange, the BSE has developed a comprehensive set of policies that govern all aspects of trading and listings, enhancing the overall market integrity and protecting investor interests.One of the fundamental policies implemented by the BSE involves strict listing criteria. This ensures that only companies that meet high standards of financial health, corporate governance, and compliance are allowed to list. These criteria are aimed at ensuring that companies are well-managed and financially stable, minimizing the risk to investors and maintaining public confidence in the financial markets.To combat unethical practices like market manipulation and insider trading, the BSE has established robust surveillance mechanisms. These systems monitor trading patterns and flag unusual activity, allowing the BSE to take swift action against individuals and companies that violate trading regulations. This is crucial for maintaining a level playing field and ensuring that the market operates in a transparent and fair manner. In addition to these safeguards, the BSE actively promotes investor education, providing resources and tools to help investors make informed decisions. This is complemented by the BSE's proactive approach to technology adoption, which has seen the introduction of advanced trading systems and platforms that provide greater accessibility and improved transaction speeds. The BSE's policies are regularly reviewed and updated to reflect changes in the global financial landscape and emerging trends in market practices. This adaptive approach ensures that the BSE remains at the forefront of market regulation, capable of effectively managing new challenges and opportunities in the market. Overall, the Bombay Stock Exchange's policies are a testament to its commitment to upholding the highest standards of market conduct and investor protection, making it a model for other exchanges around the world.",""})



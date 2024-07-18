import os
import json
import pandas as pd
import traceback
import PyPDF2
from logger import logging

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PDFFileReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text

        except Exception as e:
            raise Exception("error reading the PDF file")

    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "Unsupported file format !! Only PDF and text file supported."
        )

def get_table_data(quiz_str):
    try:
        logging.info(f"Received quiz_str: {quiz_str}")  # Log the received quiz_str
        with open("quiz_output.txt", "w") as f:
            f.write(quiz_str)
            print(quiz_str)
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        logging.info(f"Parsed quiz_dict: {quiz_dict}")  # Log the parsed quiz_dict

        for key, value in quiz_dict.items():
            logging.info(f"Processing item: {key}, {value}")  # Log each item being processed
            mcq = value.get("mcq")
            options = value.get("options")
            correct = value.get("correct")

            if not (mcq and options and correct):
                logging.error(f"Missing data in item: {key}, mcq: {mcq}, options: {options}, correct: {correct}")
                continue  # Skip this item if any required field is missing

            options_str = " || ".join([f"{option} -> {option_value}" for option, option_value in options.items()])
            quiz_table_data.append({"MCQ": mcq, "Choices": options_str, "Correct": correct})

        logging.info(f"Constructed quiz_table_data: {quiz_table_data}")  # Log the final table data
        return quiz_table_data
    except Exception as e:
        logging.error(f"Exception in get_table_data: {e}")
        traceback.print_exception(type(e), e, e.__traceback__)
        return None
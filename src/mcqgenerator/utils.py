import os
import traceback
import json
import PyPDF2

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfFileReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        except Exception as e:
            raise Exception("error reading the PDF file")
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise Exception("unsupported file format only pdf and text file suppoted")
    
def get_table_data(quiz_str):
    try:
        # convert the quiz from a str to dict
        quiz_dict=json.loads(quiz_str)
        quiz_table_data=[]
        # iterate over the quiz dictionary and extract the required information
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = list(value["options"].values())[:4]  # Ensure only the first 4 options are taken
            correct = value["correct"]

            quiz_table_data.append({
                "MCQ": mcq,
                "Option A": options[0] if len(options) > 0 else "",
                "Option B": options[1] if len(options) > 1 else "",
                "Option C": options[2] if len(options) > 2 else "",
                "Option D": options[3] if len(options) > 3 else "",
                "Correct": correct
            })

        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
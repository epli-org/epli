# Steps
# 1. Get pdf
# 2. Get abstract from pdf
# 3. Enter abstract into GPT-3 with prompt to simplify
# 4. Show simplified abstract

# ----- Get PDFs -----
# from PyPDF2 import PdfReader
# reader = PdfReader("papers/attention.pdf")
# number_of_pages = len(reader.pages)

# txt_file_path = r"papers/attention.txt"
# file=open(txt_file_path,"a")
# for x in range(0, number_of_pages):
#   page = reader.pages[x]
#   text = page.extract_text()
#   file.writelines(text)

# ----- Get Abstract section -----
abstract=""
def get_arxiv_abstract(txt_file_path):
  # Just match based on hardcoded keywords
  abstract_start = "Abstract"
  abstract_end = "Introduction"
  abstract = ""
  inside_abstract = False
  with open(txt_file_path, 'r') as txt_file:
    for line in txt_file.readlines():
      if abstract_start in line:
        inside_abstract = True
      

# ----- Simplify abstract -----
import os
import openai

openai.api_key = os.getenv("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")
response = openai.Completion.create(
  model="text-davinci-002", 
  prompt="Explain '" + abstract + "' like I am five years old.", 
  temperature=1, 
  max_tokens=6
  )


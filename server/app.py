from flask import Flask, request, jsonify
from urllib import request as urllib_request
from PyPDF2 import PdfReader
import os
import openai


app = Flask(__name__)

@app.route("/")
def get_papers_cached():
    papers = []
    for index, paper_tag in enumerate(os.listdir("server/papers")):
        print(paper_tag)
        papers.append(paper_tag)
        if index >= 10:
            break
    paper_string = ', \n'.join(papers)
    
    return f"<p>Hello, World! Papers in our 'database': {paper_string}.</p>"


def download_file(download_url, download_folder, download_filename):
    response = urllib_request.urlopen(download_url)
    final_output_path = os.path.join(download_folder, f"{download_filename}.pdf")
    file = open(final_output_path, 'wb')
    file.write(response.read())
    file.close()
    print("Download Completed")

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
                continue
            elif abstract_end in line:
                outside_abstract = True
                break
            elif inside_abstract:
                abstract += line.strip() + ' '
    return abstract

def get_explanation_prompt(abstract):
    return f"Explain '{abstract}' like I am a fifth grader, in 3 sentences or less."

def llm_paper_summary(arxiv_id, abstract):
    """Returns the LLM-Generated summary of the paper, either fresh or cached
    """
    # Set the API key
    openai.api_key = "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"
    summary_filename = f"{arxiv_id}.txt"
    summary_directory = "server/summaries"
    if not os.path.exists(summary_directory):
        os.mkdir(summary_directory)
    # Check if it's in the cache
    if (summary_filename in os.listdir(summary_directory)):
        # It's in the cache, lets just return the cached version
        with open(os.path.join(summary_directory, summary_filename), 'r') as f:
            paper_summary = f.readlines()[0]
            print("From Cache")
            print(paper_summary)
            return paper_summary
    
    # If it's not in the cache, summarize via the OpenAI API and cache the result
    else:
        response = openai.Completion.create(
            model="text-davinci-002", 
            prompt=get_explanation_prompt(abstract), 
            temperature=1,
            max_tokens=100
        )
        summary = response['choices'][0]['text'].strip()
        print("Abstract: ", abstract)
        with open(os.path.join(summary_directory, summary_filename), 'w') as f:
            f.write(summary)

        return summary


@app.route("/main_paper_information")
def main_paper_info():
    """Returns a json object with the following format:
    {
        abstract:<paper_abstract>
        summary:<paper_summary>
    }
    Other fields to be added in other functions

    Assumes that the request.args object contains a `paper_url` parameter
    """
    print(request.args)
    paper_url = request.args.get('paper_url')
    print(paper_url)

    # TODO: Break the text extraction and summarization into separate function, with support for caching,
    # and specializations for specific URL types (arxiv-vanity is the only one that works rn, slowly add
    # support for more).

    # Check if URL is a valid arxiv page or not
    if "arxiv-vanity" in paper_url:
        # If it's an Arxiv URL, get the arxiv_id
        arxiv_id = paper_url.split('arxiv-vanity.com/papers/')[1].strip('/')

    else:
        # If not, then return a default object. TODO: Make this an error that's handled upstream.
        return jsonify({"summary": "summary", "abstract": "abstract"})

    # Reconstruct the Arxiv URL from the ID.
    download_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    # Grab the PDF and download it (TODO: check cache in the future)
    download_directory = "server/papers"
    if not os.path.exists(download_directory):
        os.mkdir(download_directory)
    download_file(download_url, download_directory, arxiv_id)

    # Extract the text from the PDF
    pdf_path = os.path.join(download_directory, f"{arxiv_id}.pdf")
    reader = PdfReader(pdf_path)
    number_of_pages = len(reader.pages)

    txt_file_path = os.path.join(download_directory, f"{arxiv_id}.txt")
    with open(txt_file_path,"w") as f:
        for x in range(0, number_of_pages):
            page = reader.pages[x]
            text = page.extract_text()
            f.writelines(text)

    # Extract the abstract from the PDF text
    abstract = get_arxiv_abstract(txt_file_path)

    # Use GPT-3 to summarize the PDF
    summary = llm_paper_summary(arxiv_id, abstract)
    # openai.api_key = "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"
    # response = openai.Completion.create(
    #     model="text-davinci-002", 
    #     prompt=get_explanation_prompt(abstract), 
    #     temperature=1,
    #     max_tokens=10
    # )
    # summary = response['choices'][0]['text']
    # print("Abstract: ", abstract)

    # Return the abstract and summary in a JSON response object
    test_response = {
        "summary": summary,
        "abstract": abstract,
    }
    return jsonify(test_response)


if __name__ == '__main__':
    app.run()
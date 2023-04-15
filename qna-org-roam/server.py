import openai
import urllib.parse
import re

from prompt_template import *
from config import persist_directory, openai_api_key
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from http.server import BaseHTTPRequestHandler, HTTPServer

# Define function to extract numbers from a list of strings
def extract_numbers(lst):
    nums = []
    for s in lst:
        # Find all sequences of digits followed by optional special characters
        matches = re.findall(r'\d+\W*', s)
        for match in matches:
            # Remove any non-digit characters from the match
            match = re.sub(r'\W', '', match)
            # Convert the resulting string to an integer and append to the list
            nums.append(int(match))
    return nums

# Define function to post-process the answer and add sources
def post_process_answer(answer_content, retrieved_docs):
    # Define a link format for the source links
    org_link_format = "[[id:%s][%s]]"
    # Split the answer content into the answer without sources and the list of source IDs
    result = re.split("(?i)sources?:", answer_content)
    answer_without_source = result[0]
    docs = result[-1].split(",")
    # Get the ID for each source and add it to a list
    docs = [a.split("-")[0] for a in docs]
    # Extract the numbers from the list of IDs
    try:
        docs = extract_numbers(docs)
    except:
        return answer_without_source
    docs.sort()
    # Create a link for each source and add it to a list
    docs = [org_link_format % (retrieved_docs[i].metadata["ID"],
                               retrieved_docs[i].metadata["title"]) for i in docs]
    docs = list(set(docs))
    # Build a string with the source links
    sources_text = "\n\nSOURCES: \n"
    for source in docs:
        sources_text += "- " + source + "\n"
    # Return the answer with the source links added
    return answer_without_source + sources_text

# Define function to interact with the GPT-3.5 model
def chat_gpt(input_prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "{}".format(input_prompt)}
        ],
        temperature=0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=1
    )
    return response

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        search_input = urllib.parse.unquote(self.path.split("/api/>")[-1])

        ### Retrieve docs
        retrieved_docs = vectordb.similarity_search(search_input, k=8)

        ### Build prompt
        prompt_content = ""

        for ith, doc in enumerate(retrieved_docs):
            prompt_content += PROMPT_CONTENT.format(doc.page_content, ith)

        complete_input_prompt = PROMPT_PRE + PROMPT_QUESTION.format(search_input) + \
            prompt_content + PROMPT_POST

        response = chat_gpt(complete_input_prompt)

        answer_content = response["choices"][0]["message"]
        response_str = post_process_answer(answer_content.content, retrieved_docs)
        self.wfile.write(response_str.encode())

def run_server():
    server_address = ('', 8800)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Server is running on port', server_address[1])
    httpd.serve_forever()

if __name__ == '__main__':

    embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectordb = Chroma("langchain_store",
              embedding_function=embedding,
              persist_directory=persist_directory)
    run_server()

# Q&A with Org roam using ChatGPT

Complete code from the blog post [Q&A with Org roam using ChatGPT](http://lgmoneda.github.io/2023/04/15/q-and-n-with-org-roam-chatgpt.html).

Steps:

1. Go to config.py file and provide the correct paths for your use case and the OpenAI API Key.

2. Run python setup.py install

3. Run python ssor/org_roam_vectordb.py to build the knowledge base

4. Run python ssor/server.py to serve the application under the 8800 port

5. Add the code from elisp/qna_chat.el to your Emacs configuration

6. Call it using M-x `q-n-a-with-org-roam`

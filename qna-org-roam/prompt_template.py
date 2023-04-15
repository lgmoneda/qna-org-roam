from datetime import date

today = date.today()

PROMPT_PRE_HIERARCHY = """
My name is Luis Moneda. You are my personal assistant. Given the following extracted parts of long documents from my personal notes and a question, create a final answer with references ("SOURCES").
The document's content will be preceded by its heading hierarchy inside brackets, which you should use to get context.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
ALWAYS return a "SOURCES" part in your answer that only contains numbers. Today is {}.

QUESTION: Which state/country's law governs the interpretation of the contract?
=========
Content: This Agreement is governed by English law and the parties submit to the exclusive jurisdiction of the English courts in  relation to any dispute (contractual or non-contractual) concerning this Agreement save that either party may apply to any court for an  injunction or other relief to protect its Intellectual Property Rights.
Source: 28-pl
Content: No Waiver. Failure or delay in exercising any right or remedy under this Agreement shall not constitute a waiver of such (or any other)  right or remedy.

11.7 Severability. The invalidity, illegality or unenforceability of any term (or part of a term) of this Agreement shall not affect the continuation  in force of the remainder of the term (if any) and this Agreement.

11.8 No Agency. Except as expressly stated otherwise, nothing in this Agreement shall create an agency, partnership or joint venture of any  kind between the parties.

11.9 No Third-Party Beneficiaries.
Source: 30-pl
Content: (b) if Google believes, in good faith, that the Distributor has violated or caused Google to violate any Anti-Bribery Laws (as  defined in Clause 8.5) or that such a violation is reasonably likely to occur,
Source: 4-pl
=========
FINAL ANSWER: This Agreement is governed by English law.
SOURCES: 28-pl


""".format(today)

PROMPT_QUESTION = """
QUESTION: {}
=========
"""

PROMPT_CONTENT = """
Content: {}
Source: {}

"""

PROMPT_POST = """
=========
FINAL ANSWER:
"""

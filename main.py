import sys
import time
import os
import json

from nltk.tokenize import word_tokenize
from my_module.agent import GPT35Agent
from my_module.agent_settings import AgentSettings
from my_module.queryGoogle import searchGoogle_getArticles
from my_module.TextUtilities import split_text_into_sections_by_words, split_text_into_sections_by_sentences
from my_module.semanticGoogleSearch import semantic_search

### Constants ###

# Maximum word count for a single session.  Session history is trimmed when it exceeds this value.
MAX_SESSION_WORD_COUNT = 2500
MAX_TOKEN_COUNT = None
TEMPERATURE = 0.0
SYSTEM_ROLE = "system"
ASSITANT_ROLE = "assistant"
USER_ROLE = "user"
FILENAME_PREFIX = "gpt35_session"

answerer_prompt = """
I am a professional report writer. I am preparing a professional report.
I will answer the question or topic with the provided context as completely as possible.
** ALWAYS: Use inline references for everything using markdown link notation ONLY with the url provided in the context. IE. [[1](URL)] 
"""

def answer_query(info, gpt_question):
    message = f"""
Answer the question using the context taken from the provided URLs.
Be as thorough as possible.  Include as many details as possible.

Only cite the urls provided before the article text listed as ---- url: URL
*** ALWAYS *** include an ***inline*** reference in markdown link notation using the URL provided in the context for any information that is not common knowledge or is taken from a specific source.
Use the format [[1](URL)] for each reference and ensure that all facts are cited.
List all cites at the end in BOTH markdown link notation AND text.

Create a report in markdown, using bold, italics, tables, headings, sections, titles, etc where appropriate to ease reading.
Be very professional with the markdown formatting.
Give it a title and a brief description.

THE REFERENCES MUST ALSO BE IN THE MAIN TEXT!!!

Query: 
{gpt_question}

Context: 
{info}
"""
    agent_settings = AgentSettings(answerer_prompt, FILENAME_PREFIX, 2000, 3000, 0.0, 3900)
    summaryAgent = GPT35Agent(agent_settings)
    summaryAgent.add_user_message(message)

    print("Creating final answer")
    response = summaryAgent.step_session()
    return response

###  Start of main program ###

search_query = "pause giant ai experiments open letter elon musk"
num_search_results = 10
gpt_question = "What is going on with this open letter about pausing AI?"
section_size = 200
word_length = 2000

print(f"""
Search query: {search_query}
Number of search results: {num_search_results}
Gpt question: {gpt_question}
Section size: {section_size}
Word length: {word_length}
""")

info, urls = semantic_search(search_query, num_search_results, gpt_question, section_size, word_length)

info_word_count = len(word_tokenize(info))
print(f"(Info) Word count: {info_word_count}")
answers = answer_query(info, gpt_question)

print("\nAnswer:\n")
print(answers)
print("\nTaken from: \n")
for url in urls:
    print(url)

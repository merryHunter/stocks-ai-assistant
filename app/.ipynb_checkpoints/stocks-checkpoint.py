#!/usr/bin/env python
# coding: utf-8
import os
import openai
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_openai import ChatOpenAI
from langchain.tools.render import format_tool_to_openai_function
import requests
from datetime import datetime, timedelta
from nemoguardrails import LLMRails, RailsConfig
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails

yesterday = (datetime.today() - timedelta(days = 1)).strftime('%Y-%m-%d')

openai_apikey = os.getenv('OPENAI_API_KEY')
openai.api_key =  os.getenv('OPENAI_API_KEY')

model = ChatOpenAI(openai_api_key=openai_apikey,temperature=0)

config = RailsConfig.from_path("nemo-config.yaml")
guardrails = RunnableRails(config)


ticker_template = """Extract the company name from the following text: 

{question}. 
Examples:
Should I buy Bruker Corp. stocks?
return: Bruker Corp.

Is it a good time to buy Maersk?
return Maersk
'
"""

hyde_template = """Pretend you are experienced stock financial advisor optimized for shorting strategy. Here is the question:

{question} .

 Provide a deliberate answer to the question above using facts from the following news:
 {context}
"""

def answer_stock_question(question: str) -> str:
    """ Answer question with LLM regarding stocks purchase using news context from newsapi.org.
        Use basic Nemo Guardrails to prevent harmful speech in the input/output. """
    hyde_prompt = ChatPromptTemplate.from_template(hyde_template)
    ticker_prompt = ChatPromptTemplate.from_template(ticker_template)
    
    hyde_query_transformer = hyde_prompt | ( guardrails | model) | StrOutputParser()
    ticker_tr = ticker_prompt | ( guardrails | model) | StrOutputParser()
    
    company_result = ticker_tr.invoke({"question": question})
    print(f"Company retrieved: {company_result}")
    
    if "can't respond" not in company_result:
        url = ('https://newsapi.org/v2/everything?'
               f'q={company_result}&'
               f'from={today}&'
               'sortBy=popularity&'
               f'apiKey={os.getenv("NEWS_API_KEY")}')
        
        response = requests.get(url)
        
        news_context = ""
        for art in response.json()['articles'][:10]:
            news_context += f"Title: {art['title']}\nDescription: {art['description']}, {art['content']}\n\n"
        #print(news_context)
        print("Assistant:\n")
        x = hyde_query_transformer.invoke({"question": baseline_question, "context": news_context})
        return x
    else:
        return company_result


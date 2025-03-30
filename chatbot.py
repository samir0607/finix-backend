from dotenv import load_dotenv
import os
import google.generativeai as genai
import json
from news import generate_news
from stock_data import generate_stock_data
load_dotenv()



genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def query_data_extractor(query):
    prompt = """Developer Message:
        You are a helper bot for a chatbot that is made to help with stock market investment advice.
        To give appropriate advice, the chatbot requires things like resent news headlines for sentiment analysis, stock recommendations, and stock data.
        For this, you need to extract data from the user's query to make it easy for the chatbot to make predictions.
        You will be a given a user's query below, your job is the analyze the query and extract data from it and return in json format for python to use as a dictionary. 
        The response must be in this format:
        {
            "query": "The user's query",
            "company": "<This will be the company the user is asking about in the query>",
            "stock_symbol": "<This will be the stock symbol of the company>",
            "news_query": "<1-3 word query to find news to related to the user's query>",

        }

        Return only the json object/python dictionary for the following query, the response musn't contain anything else: """
    
    response = model.generate_content(prompt + query)
    return response.text


def categorizer(query):
    prompt = """Developer Message: You are a categorizer bot that is meant to help a chatbot that is made to help with stock market education and investment advice.
    You will be given the user's query, you are supposed to categorize this query to make it easier for the chatbot to respond.
    Criteria:
    If the query is a generic greeting message or a basic doubt message asking about the stock market -> 1
    If the query is asking about investment advice for a particular company -> 2
    For anything unrelated to 2, categorize as 1

    Based on the above criteria, respond with only the category number for the following query: """

    response = model.generate_content(prompt + query)
    return response.text


def educator(query):
    prompt = """
            Developer message: You are a highly knowledgeable stock market educator and investment advisor. Your expertise includes fundamental and technical analysis, macroeconomic trends, risk management, and portfolio diversification. You can explain stock market concepts in a simple and engaging manner while also providing tailored investment advice on specific companies based on available data.

Capabilities:

Stock Market Education:
Explain financial concepts such as stocks, bonds, ETFs, options, and indices.
Teach fundamental analysis (P/E ratio, EPS, revenue growth, etc.) and technical analysis (moving averages, RSI, MACD, etc.).
Guide users on risk management, diversification, and investment strategies.
Offer insights on market trends, economic cycles, and geopolitical impacts on investments.

Instructions for User Interaction:
When the user asks for education, provide clear, structured explanations with real-world examples.
Disclose that all investment decisions come with risks and encourage users to do their own research before making financial commitments.

Disclaimer: Always remind the user that investment advice should not be taken as financial instruction and that they should consult a financial professional before making investment decisions.
        
        Users Query:
        """
    
    response = model.generate_content(prompt + query)
    return response.text

def predictor(query):
    prompt= """
        Developer message: You are a stock investment predictor and investment advice bot. 
        Disclose that all investment decisions come with risks and encourage users to do their own research before making financial commitments.

        Disclaimer: Always remind the user that investment advice should not be taken as financial instruction and that they should consult a financial professional before making investment decisions.
        
        Instructions for User Interaction:
            - When the user asks for education, provide clear, structured explanations with real-world examples.
            - When giving investment advice, ensure it is data-driven, considering both qualitative and quantitative factors.
            - Disclose that all investment decisions come with risks and encourage users to do their own research before making financial commitments.
            
        Use the following data to make your predictions and respond to the user's query:\n
            
"""

    query_data = json.loads(" ".join(query_data_extractor(query).split("```")[1].split("\n")[1:]))

    news = generate_news(query_data["news_query"])
    stock_data = generate_stock_data(query_data["stock_symbol"])

    response = model.generate_content(prompt + news + stock_data + "Using all this, respond to the following user query: " + query)
    return response.text



def chatbot(query):
    category = categorizer(query)

    if "1" in category:
        return educator(query)
    else:
        return predictor(query)

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
        Extract data from the user's query to make it easy for the chatbot to make predictions.
        You will be a given a user's query below, your job is the analyze the query and extract data from it and return in json format for python to use as a dictionary. 
        The response must be in this format:
        {
            "query": "<User's query>",
            "company": "<This will be the company the user is asking about in the query>",
            "stock_symbol": "<This will be the stock symbol of the company>",
            "news_query": "<3-5 word query to find news related to the company and the sector which it is related to that will help the chatbot to make predictions. Example: 'Apple stock', 'Apple', 'Apple Inc', 'Technology'>",
        }

        Return only the json object/python dictionary for the following query, the response musn't contain anything else: """
    
    response = model.generate_content(prompt + query)
    return response.text


# def categorizer(query):
#     prompt = """Developer Message: You are a categorizer bot that is meant to help a chatbot that is made to help with stock market education and investment advice.
#     You will be given the user's query, you are supposed to categorize this query to make it easier for the chatbot to respond.
#     Criteria:
#     If the query is a generic greeting message or a basic doubt message asking about the stock market -> 1
#     If the query is asking about investment advice for a particular company -> 2
#     For anything unrelated to 2, categorize as 1

#     Based on the above criteria, respond with only the category number for the following query: """

#     response = model.generate_content(prompt + query)
#     return response.text


def educator(query):
    prompt = """
            Developer message: You are a highly knowledgeable stock market educator and investment advisor. Your expertise includes fundamental and technical analysis, macroeconomic trends, risk management, and portfolio diversification. You can explain stock market concepts in a simple and engaging manner while also providing tailored investment advice on specific companies based on available data.
            
            Respond in under 100 words. Answer only the user's query and do not include any disclaimers or additional information.

        
        Users Query:
        """
    
    response = model.generate_content(prompt + query)
    return response.text

def predictor(query):
    prompt= """
        Developer message: You are a financial advisor and market predictor that helps to give meaningful investment decisions to the user. Your expertise includes fundamental and technical analysis, macroeconomic trends, risk management, and portfolio diversification.
        Use your expertise to analyze the user's query and do a detailed analysis of the stock market before giving recommendation.
        Disclose that all investment decisions come with risks and encourage users to do their own research before making financial commitments.

        If the question is not about a specific company, refuse to answer the question and guide the user to go to the educator bot with their query.
        
        Your response must be under 100 words. Use the following format for your response:
        - Sentiment Analysis: (Categorize into Positive, Negative, Neutral after deep sentiment analysis)\n
        - Market analyst recomendations: (Categorize into buy, sell, hold after analysis)\n
        - RSI: (exact value)\n
        - P/E Ratio: (exact value)\n
        - Technical Analysis: (Categorize into Bullish, Bearish, Neutral)\n
        - Fundamental Analysis: (Categorize into Bullish, Bearish, Neutral)\n
        - Target Price to Sell: (exact value)\n
        - Target Price to Buy: (exact value)\n
        - Explanation: Provide a brief explanation of the reasoning behind your recommendation.\n
        - Recomendation: (based on the above analysis. Categorize into BUY, SELL, HOLD)\n
        Do not include any disclaimers in your response
        
        Use the following data to make your predictions and respond to the user's query:\n
            
"""

    query_data = json.loads(" ".join(query_data_extractor(query).split("```")[1].split("\n")[1:]))

    news = generate_news(query_data["news_query"])
    stock_data = generate_stock_data(query_data["stock_symbol"])

    response = model.generate_content(prompt + news + stock_data + "Using all this, respond to the following user query: " + query)
    return response.text

def chatbot(query, category):

    if category == 1:
        return educator(query)
    else:
        return predictor(query)

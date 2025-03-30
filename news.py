# from fastapi import FastAPI, HTTPException
from newsapi import NewsApiClient
from dotenv import load_dotenv
import os
import google.generativeai as genai
# from openai import OpenAI
load_dotenv()

# app = FastAPI()

api_key = os.getenv('NEWS_API_KEY')
newsapi = NewsApiClient(api_key=api_key)

def fetch_news(query=None, 
               sources=None, 
               category=None, 
               language='en', 
               country=None, 
               from_date=None, 
               to_date=None, 
               sort_by=None, 
               page=None, 
               fetch_type=None):
    try:
        if fetch_type == 'top_headlines':
            response = newsapi.get_top_headlines(
                q=query,
                sources=sources,
                category=category,
                language=language,
                country=country,
                page=page
            )
        elif fetch_type == 'everything':
            response = newsapi.get_everything(
                q=query,
                sources=sources,
                from_param=from_date,
                to=to_date,
                language=language,
                sort_by=sort_by,
                page=page
            )
        elif fetch_type == 'sources':
            response = newsapi.get_sources()
        else:
            raise ValueError("Invalid fetch_type. Choose 'top_headlines', 'everything', or 'sources'.")

        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def generate_news(query):
    news_response = fetch_news(query=query, fetch_type="everything")

    articles = news_response["articles"]
    print("Articles Content:", articles)

    news_text = "Here are the latest news headlines and descriptions about the topic:\n\n"
    for article in articles:
        title = article.get("title", "No Title")
        description = article.get("description", "No Description")
        news_text += f"- {title}\n  {description}\n\n"

    return news_text
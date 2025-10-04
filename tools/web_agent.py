# tools/web_agent.py
import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

class WebAgent:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            self.client = None
            print("WARNING: TAVILY_API_KEY not set. WebAgent will be non-functional.")
        else:
            self.client = TavilyClient(api_key=api_key)

    def search(self, query: str) -> str:
        if self.client is None:
            return "Error: WebAgent is not configured. Please set the TAVILY_API_KEY in your .env file."
        try:
            response = self.client.search(query=query, search_depth="advanced", max_results=3)
            return "\n\n".join([f"**{res['title']}**\n{res['content']}" for res in response['results']])
        except Exception as e:
            return f"Web search failed: {e}"
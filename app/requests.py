
import requests
#from request import get
from .models import Quotes
from config import Config

quotes_url = Config.QUOTES_URL

def getQuotes():
    random_quote = requests.get(quotes_url)
    new_quote = random_quote.json()
    author = new_quote.get("author")
    quote = new_quote.get("quote")
    quote_object = Quotes(author,quote)
    return quote_object
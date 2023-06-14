import re
import subprocess
import requests
import time
import datetime
import wikipedia
from bs4 import BeautifulSoup

def espeak(text: str, pitch: int=80) -> int:
    """ Use espeak to convert text to speech. """
    return subprocess.run(['espeak', f'-p {pitch}', text]).returncode

def get_time():
    time = datetime.datetime.now().strftime("%I:%M %p")
    return (f"The time is {time}")

def get_date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    return (f"The date is {date} {month} {year}")

def get_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    return ip_address

def get_wikipedia_info(query):
    pattern = r'(?:who|what|when|where|why|how|tell me somthing about|tell me about)\s+(.*)'
    match = re.search(pattern, query, re.IGNORECASE)
    if match:
        topic = match.group(1)
    else:
        topic = query

    print(topic)
    print("TEST STRING")
    try:
        # search for topic
        search_results = wikipedia.search(topic)
        if not search_results:
            raise wikipedia.exceptions.PageError(topic)
        
        # get summary of top search result
        try:
            page = wikipedia.page(search_results[0])
        except wikipedia.exceptions.DisambiguationError as e:
            page = wikipedia.page(e.options[0])  # Automatically choose the first option
        
        summary = wikipedia.summary(page.title, sentences=2)
        
        # speak the summary
        print(summary)
        return (summary)
    except wikipedia.exceptions.PageError:
        print(f"Sorry, I could not find any information about {topic}.")
    except Exception as e:
        print(f"An error occurred: {e}")

def evaluate_expression(query):
    # use regex to find mathematical expressions
    pattern = r'\b\d+\s*([-+*/%])\s*\d+\b'
    match = re.search(pattern, query)
    #print(match + '. . .')
    if match:
        expr = match.group(0)
        try:
            return eval(expr)
            #return result
        except:
            return None
    else:
        return None

def check_if_internet_working():
    try:
        requests.get("https://www.google.com")
        return True
    except:
        return False
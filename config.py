"""
Configuration for Holy Quran Tilawat Page
পেজ আইডি, এক্সেস টোকেন এবং পাথ কনফিগারেশন
"""

import os

FB_PAGE_ID = os.environ.get("FB_PAGE_ID", "1430288070174104")
FB_PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN", "EAAe1H3izQCYBTECDZBuZCdZBhUCSZCxHfp80umYK4Q1N0SamI5KuTJCCMba3fqlzttmCdOwlxlZBIkJd1ATBlZCYM7Rtn26yXO27C9lxvZAOQEbaJZBJ2svO9bLlEwT9ZCQgwnRud7dW5n6eB7XwGyqbMU2fXO3imIzWjAsHkJxbZCDZANzaWVwqJeCX1jkxV2t9LhhkzJNcbQEFcKcEsFkumXIddDVjowjtLvOXP6PJkQZD")

FB_GRAPH_URL = "https://graph.facebook.com/v21.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
LOGS_FILE = os.path.join(BASE_DIR, "posted_history.json")

os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

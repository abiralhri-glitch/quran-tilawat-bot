"""
Configuration for Holy Quran Tilawat Page
পেজ আইডি, এক্সেস টোকেন এবং পাথ কনফিগারেশন
"""

import os

FB_PAGE_ID = os.environ.get("FB_PAGE_ID", "1430288070174104")
FB_PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN", "EAAe1H3izQCYBTKqRGssZBfBij0DGxZCwQm12gkMuZBpWXwaiYuqbSmykjhXvytdEcoEtX89uZCaeUnMXuyr5bXHsZAi6rDcja9xK2ZBSZCsViywZBZAsW0LQqHHW75OsxFE8HivCbqUDA88qQocUSl2xsDv7VnmWMnCPj5A1tQ5XIp9FYEWsot8msfLN61xMMwJpCCb7uVcvz0pohbhRG89c4pt49auipck2sNdzOzs8Mdffk")

FB_GRAPH_URL = "https://graph.facebook.com/v21.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
LOGS_FILE = os.path.join(BASE_DIR, "posted_history.json")

os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

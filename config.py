import os
from dotenv import load_dotenv

load_dotenv()

# Facebook Graph API Credentials for "কুরআনের তিলাওয়াত - Quran Tilawat" (Page ID: 1430288070174104)
# Verified Lifetime Permanent Page Access Token (expires_at: 0 - NEVER EXPIRES)
PERMANENT_QURAN_TOKEN = "EAAe1H3izQCYBTIZAJZCf3kDxYyVg3DxziLkrE3mPJ68KOnPmLIajfvfznlFItheoclTjYZBKm26jPpoFM19i0nAx2DZA6VsQOGtjltqkkgD2AEdyHEGKDZAKId7jxZAX1QoDScW0Q4EdECG0MZCZCLnzr2MCZBytkWDSdT2DpdHbceLOQnmZAkzSo02rrBmPTTffMGvzT8"

FB_PAGE_ID = os.getenv("FB_PAGE_ID", "1430288070174104")
FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN") or PERMANENT_QURAN_TOKEN

# Meta Graph API Base URL
FB_GRAPH_API_VERSION = "v21.0"
FB_GRAPH_URL = f"https://graph.facebook.com/{FB_GRAPH_API_VERSION}"

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")

# Aliases for compatibility
DOWNLOADS_DIR = DOWNLOAD_DIR
PROCESSED_DIR = OUTPUT_DIR

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

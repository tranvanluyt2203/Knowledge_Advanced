from django.conf import settings
import os

SAVE_FOLDER_PATH = os.path.join(settings.BASE_DIR,'app', 'Module_Final', 'CallAPILibrary', 'results')
TEMP_SAVE_FOLDER_PATH = os.path.join(settings.BASE_DIR,'app', 'Module_Final', 'CallAPILibrary', 'results', 'temp')
TEMP_LOG_FOLDER_PATH =  os.path.join(settings.BASE_DIR,'app', 'Module_Final', 'CallAPILibrary', 'logs', 'temp')
API_KEYS_PATH = os.path.join(settings.BASE_DIR,'app', 'Module_Final', 'CallAPILibrary', 'data', 'gemini_api_keys.json')
# SAVE_FOLDER_PATH = "results"
# TEMP_SAVE_FOLDER_PATH = "results/temp"
# TEMP_LOG_FOLDER_PATH = "logs/temp"
# API_KEYS_PATH = "Module_Final/CallAPILibrarydata/gemini_api_keys.json"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent"
MAX_CALL_COUNT = 10
SLEEP_TIME = 30
HEADERS = '{"Content-Type": "application/json"}'

SAFETY_SETTINGS = """[
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]"""

GENERATION_CONFIG = '{"temperature": 0.3, "top_p": 0.5, "top_k": 1}'

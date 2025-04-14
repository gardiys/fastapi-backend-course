import os

from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("API_KEY")
account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")


url = 'https://api.jsonbin.io/v3/b/'

headers = {
    "X-Master-Key": api_key
}

headers_type = {
  'Content-Type': 'application/json',
  'X-Master-Key': api_key
}

API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/"

LLM_MODEL = "@cf/meta/llama-3-8b-instruct"

HEADERS_AI = {
    "Authorization": f"Bearer {os.getenv('CLOUDFLARE_API_TOKEN')}"
}

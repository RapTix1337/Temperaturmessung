import requests
from pprint import pprint
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')
url = os.getenv('API_URL') + '?x-aio-key=' + api_key
data = {
        'value': 12
}
r = requests.post(url, data=data)

pprint(r.text)

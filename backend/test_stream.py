import json
from main import ChatInSchema
import requests

url = "http://127.0.0.1:8000/chat-stream/"

data = {
    "query": "What are the steps to set up a source in Airbyte Cloud?",
    "current_url": "https://docs.airbyte.com/category/using-airbyte-cloud",
    "history": [
        {"message": "", "sender": ""},
    ],
}
# data = ChatInSchema(query=, current_url=, history=[])
# data_dict = data.dict()

headers = {"Content-type": "application/json"}

try:
    with requests.post(url, data=json.dumps(data), headers=headers, stream=True) as r:
        print('Status code:', r.status_code)

        for line in r.iter_lines():
            if line:
                print(line.decode("utf-8"), flush=True)
except Exception as e:
    print(f"Caught exception: {e}")
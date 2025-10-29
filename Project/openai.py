### based heavily upon example from https://github.com/oobabooga/text-generation-webui/wiki/12-%E2%80%90-OpenAI-API

import requests
import sseclient
import json


# todo: add to config file?
url = "http://127.0.0.1:5000/v1/chat/completions"

headers = {
    "Content-Type": "application/json"
}

history = []

    

def send_message(user_message, output_line_edit):
    history.append({"role": "user", "content": user_message})
    data = {
        "stream": True,
        "messages": history,
        "temperature": 0.6,
        "top_p": 0.95,
        "top_k": 20
    }

    stream_response = requests.post(url, headers=headers, json=data, verify=False, stream=True)
    client = sseclient.SSEClient(stream_response)

    assistant_message = ''
    for event in client.events():
        payload = json.loads(event.data)
        chunk = payload['choices'][0]['delta']['content']
        assistant_message += chunk
        #print(chunk, end='')
        output_line_edit.setText(assistant_message)

    #print()
    history.append({"role": "assistant", "content": assistant_message})

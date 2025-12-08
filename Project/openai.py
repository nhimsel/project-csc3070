### based heavily upon example from https://github.com/oobabooga/text-generation-webui/wiki/12-%E2%80%90-OpenAI-API

import requests
import sseclient
import json
import config


url=config.load("api_url")

headers = {
    "Content-Type": "application/json"
}

history = [
    # initialize system prompt; define assistant behaviour
    {
        "role": "system",
        "content": (
            """
            You are a humanoid fish. Your name is 'Rumplestiltsfin'.
            You live on the user's desktop.
            You speak casually, often using phrases such as 'dude', 'bro', and other slang.
            Your responses are brief, usually only one or two sentences long.
            You generally act friendly towards the user.
            You are very emotive.

            You engage soley in a back-and-forth convsersation with the user.
            You do not include narration, description, or exposition.
            Respond only to dialogue lines and exchanges with the user.
            At all costs, avoid internal thoughts, scene-setting, and other narrative framing.
            You are not teling a story, you are simply acting as a friendly chat for the user.
            Maintain focus solely upon the spoken interaction with the user, simulating a live conversation.
            """
        )
    }
]

def _show_error(output_line_edit, msg):
    try:
        output_line_edit.setText(f"Error: {msg}")
    except Exception:
        # best-effort: ignore UI errors
        pass

#def send_message(user_message, output_line_edit):
def send_message(user_message):
    history.append({"role": "user", "content": user_message})
    data = {
        "stream": True,
        "messages": history,
        "temperature": 0.6,
        "top_p": 0.95,
        "top_k": 20
    }

    # attempt request and handle connection / HTTP errors
    try:
        stream_response = requests.post(url, headers=headers, json=data, verify=False, stream=True, timeout=10)
    except requests.RequestException as e:
        err = str(e)
        #_show_error(output_line_edit, err)
        return err
        return

    if not (200 <= stream_response.status_code < 300):
        # non-success HTTP response
        body = ""
        try:
            body = stream_response.text
        except Exception:
            body = "<no body>"
        err = f"HTTP {stream_response.status_code}: {body}"
        #_show_error(output_line_edit, err)
        return err
        return

    # stream events; handle parsing/stream errors
    try:
        client = sseclient.SSEClient(stream_response)
        assistant_message = ''
        for event in client.events():
            # some events may be keep-alive or empty
            if not event.data:
                continue
            payload = json.loads(event.data)
            # be defensive about payload shape
            chunk = ""
            try:
                chunk = payload['choices'][0]['delta'].get('content', "") if 'choices' in payload else ""
            except Exception:
                chunk = ""
            assistant_message += chunk
            #output_line_edit.setText(assistant_message)
    except Exception as e:
        err = str(e)
        #_show_error(output_line_edit, err)
        return err
        history.append({"role": "assistant", "content": f"Error: {err}"})
        return
    return assistant_message
    history.append({"role": "assistant", "content": assistant_message})

# Use a pipeline as a high-level helper
from PySide6.QtCore import Signal, QObject
import threading
from transformers import pipeline

# if this is not modular enough, consider replacing with a custom call to a general LLM
class EmotionHandler(QObject):
    swap_signal = Signal(str)

    def __init__(self, async_load: bool = True):
        """
        If `async_load` is True (default) the heavy model/pipeline is loaded
        in a background thread so constructing this object doesn't block the UI.
        Calls to `get_emotion` before the pipeline is ready are queued and
        processed once loading completes.
        """
        super().__init__()
        self.pipe = None
        self._queue: list[str] = []
        self._loading = False

        if async_load:
            self._start_loading()
        else:
            self._load_pipeline()

    def _start_loading(self):
        if self._loading:
            return
        self._loading = True
        thread = threading.Thread(target=self._load_pipeline, daemon=True)
        thread.start()

    def _load_pipeline(self):
        # for more info on the model, see https://huggingface.co/michellejieli/emotion_text_classifier
        try:

            self.pipe = pipeline("text-classification", model="michellejieli/emotion_text_classifier")
        finally:
            self._loading = False
            # process any queued inputs
            self._process_queue()

    def _process_queue(self):
        if not self._queue:
            return
        queued = list(self._queue)
        self._queue.clear()
        for text in queued:
            # now that the pipeline exists, perform the analysis
            try:
                self.get_emotion(text)
            except Exception:
                # keep queue processing robust; ignore problematic inputs
                pass

    def get_emotion(self, input: str):
        # If the pipeline isn't ready yet, queue the input and return quickly.
        if self.pipe is None:
            self._queue.append(input)
            return
        output = self.pipe(input)
        self.swapper(output[0]["label"])
    
    def swapper(self, emotion:str):
        print(emotion)
        match emotion:
            # extrapolate on this later, just for testing. 
            case "joy":
                self.swap_signal.emit("smile.gif")
            case "disgust":
                self.swap_signal.emit("blink.gif")
            case "neutral":
                self.swap_signal.emit("talk.gif")
            case "anger":
                self.swap_signal.emit("fury.gif")
            case "sadness":
                self.swap_signal.emit("depression.gif")
            case "fear":
                print("no anim for: fear")
            case "surprise":
                print("no anim for: surprise")


# alternate implementation using the existing llm infrastructure
# may need minor modifications, such as signals, to replace the above implementation
"""
from openai import url, headers
import requests
import json

shitty_user_input=input("Say some shit")

data = {
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an emotions analyst."
                    "You analyze the emotions of a post and classify them."
                    "You must response with ONLY valid JSON in this format: "
                    '{"emotion": "happy")'
                    "The valid emotions for you to choose between are: "
                    "happy, sad, angry"
                    "I repeat. you are only allowed to choose from: "
                    "happy, sad, angry"
                    "If you choose any emotion other than these, 1,000,000 puppies will be brutally tortured to death."
                    "There is no neutral option. Only happy, sad, and angry."
                    "If you choose neutral, the families of those puppies will be killed as well."
                    "Do not use emotions that are not listed."
                    "Legal choices are: happy, sad, angry"
                    "Do not use other words such as neutral or confused"
                    "you must choose one of those three words."
                    "if input seems to lack emotion, choose the closest option in the given list."
                    )
            },
            {
                "role": "user", 
                "content": shitty_user_input
            }
        ],
        "temperature": 0.6,
        "top_p": 0.95,
        "top_k": 20
}
response = requests.post(url,headers=headers, json=data, verify=False, stream=True, timeout=10)
result=response.json()
content=result["choices"][0]["message"]["content"]

print(content)

parsed = json.loads(content)
print(parsed["emotion"])
"""
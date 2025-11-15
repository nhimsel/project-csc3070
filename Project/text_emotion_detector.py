# Use a pipeline as a high-level helper
from transformers import pipeline
from PySide6.QtCore import Signal, QObject

# if this is not modular enough, consider replacing with a custom call to a general LLM
class EmotionHandler(QObject):
    swap_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.pipe = pipeline("text-classification", model="michellejieli/emotion_text_classifier")
    
    def get_emotion(self, input:str):
        output=self.pipe(input)
        self.swapper(output[0]["label"])
    
    def swapper(self, emotion:str):
        print(emotion)
        match emotion:
            # extrapolate on this later, just for testing. 
            case "joy":
                self.swap_signal.emit("feesh")
            case "disgust":
                self.swap_signal.emit("feesh-2")
            case "neutral":
                self.swap_signal.emit("cat")

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
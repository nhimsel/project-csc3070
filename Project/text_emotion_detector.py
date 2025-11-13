# Use a pipeline as a high-level helper
from transformers import pipeline
from PySide6.QtCore import Signal, QObject

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
            case "joy":
                self.swap_signal.emit("feesh")
            case "disgust":
                self.swap_signal.emit("feesh-2")
            case "neutral":
                self.swap_signal.emit("cat")

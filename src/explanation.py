# src/explanation.py

class ExplanationLogger:
    def __init__(self):
        self.explanations = []

    def log(self, message):
        self.explanations.append(message)

    def get_all(self):
        return self.explanations

    def clear(self):
        self.explanations = []

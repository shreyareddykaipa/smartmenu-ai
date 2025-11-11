import pandas as pd
from gpt4all import GPT4All

class SmartMenuAI:
    def __init__(self, model_path):
        self.model = GPT4All(model_path)

    def generate_response(self, prompt):
        with self.model.chat_session():
            response = self.model.generate(prompt, max_tokens=200)
        return response

    def load_menu(self, csv_path):
        self.menu = pd.read_csv(csv_path)
        return self.menu

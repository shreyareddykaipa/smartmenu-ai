from gpt4all import GPT4All

model_path = "C:/Users/shrey/AppData/Local/nomic.ai/GPT4All"
model_name = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"

# Load the model without downloading
model = GPT4All(model_name=model_name, model_path=model_path, allow_download=False)

# Test a prompt
response = model.generate("Suggest a meal for someone who likes spicy food.")
print(response)

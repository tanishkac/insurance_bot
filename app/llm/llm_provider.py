from ollama import generate

class OllamaLLM:
    def __init__(self, model_name="mistral"):
        self.model_name = model_name

    def invoke(self, prompt: str) -> str:
        result = generate(model=self.model_name, prompt=prompt)
        return result['response']  # Returns the model's text answer

def get_llm_instance():
    return OllamaLLM()

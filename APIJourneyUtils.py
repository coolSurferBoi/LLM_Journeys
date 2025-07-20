from OpenAiJourneyUtils import OpenAiJourneyUtils
from HuggingFaceJourneysUtils import HuggingFaceJourneysUtils
class APIJourneyUtils:
    def __init__(self):
        self.LLM_connections = {}
        self.ImageGen_connections = {}
        

    def setup_LLM_connection(self, model_name):
        if model_name not in self.LLM_connections:
            if model_name == 'o4-mini':
                connection = OpenAiJourneyUtils()
            elif model_name == 'mistralai/Mixtral-8x7B-Instruct-v0.1':
                connection = HuggingFaceJourneysUtils(model_name)
            self.LLM_connections[model_name] = connection

    def setup_ImageGen_connection(self, model_name):
        if model_name not in self.ImageGen_connections:
            if model_name == 'dall-e-3':
                connection = OpenAiJourneyUtils()
            elif model_name == 'black-forest-labs/FLUX.1-dev':
                connection = HuggingFaceJourneysUtils(model_name)
            self.ImageGen_connections[model_name] = connection

    def get_LLM_connection(self,model_name):
        return self.LLM_connections[model_name]
    
    def get_ImageGen_connection(self,model_name):
        return self.ImageGen_connections[model_name]

    def chat(self, model_name, inp, message_history, role="user"):
        reply_content, message_history = self.get_LLM_connection(model_name).chat(model_name, inp, message_history, role="user")
        return reply_content, message_history

    def get_img(self, model_name, prompt):
        img_url = self.get_ImageGen_connection(model_name).get_img(model_name, prompt)
        return img_url
        
    def get_interaction_count(self,model_name):
        return self.get_LLM_connection(model_name).get_interaction_count()
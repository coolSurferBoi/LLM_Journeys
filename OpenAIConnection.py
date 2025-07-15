from openai import OpenAI
import os
from dotenv import load_dotenv
# Initialize OpenAI client
load_dotenv('.env')

class OpenAIConnection:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        self.interactions_count = 0 

    def get_client(self):
        return self.client
    
    def chat(self,model_name, inp, message_history, role="user"):
        self.interactions_count += 1
        if self.interactions_count >= 4:
            inp += " At the end of the response please add another new paragraph requesting them to refresh the page if they wish to play again."
        message_history.append({"role": role, "content": inp})
        completion = self.client.chat.completions.create(
            model=model_name,
            messages=message_history
        )
        reply_content = completion.choices[0].message.content
        message_history.append({"role": "assistant", "content": reply_content})
        return reply_content,message_history

    def get_img(self,model_name,prompt):
        image_response = self.client.images.generate(
            model=model_name,
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return image_response.data[0].url
    
    def get_interaction_count(self):
        return self.interactions_count
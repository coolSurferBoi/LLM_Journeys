class GPTJourneyUtils:

    def __init__(self,client):
        self.client = client
        self.llm = 'o4-mini'
        self.imagemodel = 'dall-e-3'
        self.interactions_count = 0 

    # Define a function to generate an image using the OpenAI API
    def get_img(self,prompt):
        image_response = self.client.images.generate(
            model=self.imagemodel,
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return image_response.data[0].url

    # Define a function to generate a chat response using the OpenAI API
    def chat(self,inp, message_history, role="user"):
        self.interactions_count += 1
        if self.interactions_count >= 4:
            inp += "At the end of the response please add another new paragraph requesting them to refresh the page if they wish to play again."
        message_history.append({"role": role, "content": f"{inp}"})
        completion = self.client.chat.completions.create(
            model=self.llm,
            messages=message_history
        )
        reply_content = completion.choices[0].message.content
        message_history.append({"role": "assistant", "content": f"{reply_content}"})

        return reply_content, message_history
    
    def get_interaction_count(self):
        return self.interactions_count
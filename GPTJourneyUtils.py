class GPTJourneyUtils:
    """
    A utility class to interact with the OpenAI API for generating images and chat completions.

    Attributes:
        client (openai.Client): The OpenAI API client instance to interact with OpenAI services.
        llm (str): The model name for generating text completions (default: 'o4-mini').
        imagemodel (str): The model name for generating images (default: 'dall-e-3').
        interactions_count (int): A counter to track the number of interactions in the current session.
    """

    def __init__(self, client):
        """
        Initializes the GPTJourneyUtils instance.

        Args:
            client (openai.Client): The OpenAI API client instance to interact with OpenAI services.
        """
        self.client = client
        self.llm = 'o4-mini'
        self.imagemodel = 'dall-e-3'
        self.interactions_count = 0 

    def get_img(self, prompt):
        """
        Generates an image based on the provided prompt using the DALL·E 3 model.

        Args:
            prompt (str): The text prompt for image generation.

        Returns:
            str: The URL of the generated image.
        """
        image_response = self.client.images.generate(
            model=self.imagemodel,
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return image_response.data[0].url

    def chat(self, inp, message_history, role="user"):
        """
        Sends a message to the OpenAI chat model and receives a response.
        Adds a custom message after 3 interactions asking the user to refresh the page.

        Args:
            inp (str): The input message from the user.
            message_history (list): The history of the conversation.
            role (str, optional): The role of the sender ("user" or "assistant"). Defaults to "user".

        Returns:
            tuple: The chat reply from the assistant and the updated message history.
        """
        self.interactions_count += 1
        
        # Add custom instruction after 3 interactions
        if self.interactions_count >= 4:
            inp += " At the end of the response please add another new paragraph requesting them to refresh the page if they wish to play again."
        
        message_history.append({"role": role, "content": inp})
        
        # Generate chat completion
        completion = self.client.chat.completions.create(
            model=self.llm,
            messages=message_history
        )
        
        reply_content = completion.choices[0].message.content
        message_history.append({"role": "assistant", "content": reply_content})

        return reply_content, message_history

    def get_interaction_count(self):
        """
        Returns the current interaction count.

        Returns:
            int: The number of interactions that have taken place.
        """
        return self.interactions_count

from openai import OpenAI
import os
from dotenv import load_dotenv

# Initialize OpenAI client
load_dotenv()

class OpenAiJourneyUtils:
    # Define supported models as class constant
    SUPPORTED_MODELS = {
    }
    MAX_INTERACTIONS = 5
    REFRESH_MESSAGE = (
        "\n\n Storyteller, Please try to end the story NOW!"
    )

    def __init__(self):
        """
        Initializes the GPTJourneyUtils instance.

        Args:
            client (openai.Client): The OpenAI API client instance to interact with OpenAI services.
        """
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.interactions_count = 0 

    def get_client(self):
        return self.client
    
    def get_img(self, model_name: str, prompt: str) -> str:
        try:
            image_response = self.client.images.generate(
                model=model_name,
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            return image_response.data[0].url
        except Exception as e:
            raise RuntimeError(f"Image generation failed: {str(e)}")
        
    def chat(self, 
             model_name, 
             inp, 
             message_history, 
             role
    ):
        self.interactions_count += 1
        
        # Add custom instruction after 3 interactions
        if self.interactions_count >= self.MAX_INTERACTIONS:
            inp += self.REFRESH_MESSAGE

        message_history.append({"role": role, "content": inp})
        try:
 
            # Generate chat completion
            completion = self.client.chat.completions.create(
                model=model_name,
                messages=message_history,
            )
            
            reply_content = completion.choices[0].message.content
            
            message_history.append({"role": "assistant", "content": reply_content})

            return reply_content, message_history
        except Exception as e:
            raise RuntimeError(f"Chat completion failed: {str(e)}")

    def get_interaction_count(self):
        """
        Returns the current interaction count.

        Returns:
            int: The number of interactions that have taken place.
        """
        return self.interactions_count

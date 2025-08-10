import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from pathlib import Path
from typing import Tuple, List, Dict
from PIL import Image

load_dotenv()

class HuggingFaceJourneysUtils:
    # Define supported models as class constant
    SUPPORTED_MODELS = {
        'mistralai/Mixtral-8x7B-Instruct-v0.1': 'together',
        'black-forest-labs/FLUX.1-dev': 'together'
    }
    
    # Define constants
    OUTPUT_DIR = Path("static/HuggingFaceImages/generated")
    IMAGE_FILENAME = "hgfImage.png"
    MAX_INTERACTIONS = 5
    REFRESH_MESSAGE = (
        "\n\n Storyteller, Please try to end the story NOW!"
    )
    def __init__(self, model_name: str, temp: float = 1):
        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model: {model_name}")
        
        self.provider = self.SUPPORTED_MODELS[model_name]
        self.client = InferenceClient(
            provider=self.provider,
            token=os.getenv("HF_TOKEN")  # Use token instead of api_key
        )
        self.interactions_count = 0
        self.output_dir = self.OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp = temp

    def get_client(self) -> InferenceClient:
        return self.client
    
    def get_img(self, model_name: str, prompt: str) -> str:
        try:
            img = self.client.text_to_image(prompt=prompt, model=model_name)
            return self._save_img(img)
        except Exception as e:
            raise RuntimeError(f"Image generation failed: {str(e)}")

    def _save_img(self, img: Image.Image) -> str:
        save_path = self.output_dir / self.IMAGE_FILENAME
        img.save(save_path)
        return f"/static/HuggingFaceImages/generated/{self.IMAGE_FILENAME}"
    
    def chat(self, 
             model_name: str, 
             inp: str, 
             message_history: List[Dict[str, str]], 
             role: str = "user"
    ) -> Tuple[str, List[Dict[str, str]]]:
        self.interactions_count += 1
        # Add custom instruction after 3 interactions
        if self.interactions_count >= self.MAX_INTERACTIONS:
            inp += self.REFRESH_MESSAGE
        message_history.append({"role": role, "content": inp})
        
        try:
            completion = self.client.chat.completions.create(
                model=model_name,
                messages=message_history,
                temperature= self.temp
            )
            reply_content = completion.choices[0].message.content
                
            message_history.append({"role": "assistant", "content": reply_content})
            return reply_content, message_history
        except Exception as e:
            raise RuntimeError(f"Chat completion failed: {str(e)}")

    def get_interaction_count(self) -> int:
        """Returns the current interaction count."""
        return self.interactions_count
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv('.env')

class HuggingFaceJourneysUtils:
    def __init__(self):
        self.client = InferenceClient(
            provider="together",
            api_key=os.environ["HF_TOKEN"],
        )

        # Save images inside Flask static folder
        self.output_dir = "static/HuggingFaceImages/generated"
        os.makedirs(self.output_dir, exist_ok=True)

    def get_client(self):
        return self.client
    
    def get_img(self, model_name, prompt):
        img = self.client.text_to_image(
            prompt,
            model=model_name,
        )
        return self._save_img(img)
    
    def _save_img(self, img):
        filename = "hgfImage.png"
        save_path = os.path.join(self.output_dir, filename)
        img.save(save_path)

        # Return the web-accessible path (relative to /static/)
        return f"/static/HuggingFaceImages/generated/{filename}"

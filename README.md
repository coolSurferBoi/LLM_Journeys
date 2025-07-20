# 🧠 LLM Journeys

Welcome to **LLM_Journeys**, a personal and practical exploration of Large Language Models (LLMs). This repository is curated and maintained by [Hoon Kim](https://github.com/HoonTheDataSpecialist), a data specialist diving deep into the capabilities, limitations, and applications of LLMs in real-world scenarios.

## 🌐 Repository Overview

This repo serves as a learning journal and implementation space for working with LLMs. It includes:

- 🧪 Experiments using Hugging Face Transformers, OpenAI API, and other LLM frameworks  
- 🛠️ Tools and scripts for inference, prompt engineering, and fine-tuning  
- 📁 A modular structure for easy expansion as the journey evolves  

## 📂 Directory Structure

```bash
LLM_Journeys/
├── static/                        
│   └── HuggingFaceImages/        
│       └── generated/            
├── templates/                    
├── .env.example                  
├── .python-version               
├── .gitignore                    
├── APIJourneyUtils.py            
├── HuggingFaceJourneysUtils.py  
├── LLMJourneyState.py            
├── OpenAiJourneyUtils.py         
├── README.md                     
├── app.py                        
├── requirements.txt              
```

## 🧰 Technologies & Tools

- [Hugging Face Models](https://huggingface.co/models)  
- [OpenAI Models](https://platform.openai.com/docs/models)  
- Python 3.10+  
- Flask (for minimal UI/API wrapping)  
- `python-dotenv` for managing environment variables  

## 🚀 Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/HoonTheDataSpecialist/LLM_Journeys.git
   cd LLM_Journeys
   ```

2. **(Optional) Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up API Keys**:

   Create a copy of the `.env.example` file and rename it to `.env`. Add your API credentials there:

   ```env
   OPENAI_API_KEY="your_openai_key_here"
   HF_TOKEN="your_huggingface_token_here"
   ```

   - Generate your Hugging Face token from [huggingface.co](https://huggingface.co/settings/tokens)  
   - Generate your OpenAI API key from [platform.openai.com](https://platform.openai.com/account/api-keys)

   **Important:** Don't commit your `.env` file. Add it to `.gitignore` to keep your keys safe:

   ```bash
   echo ".env" >> .gitignore
   ```

   Your Python scripts will load the keys using `dotenv`:

   ```python
   from dotenv import load_dotenv
   import os

   load_dotenv()

   openai_key = os.getenv("OPENAI_API_KEY")
   hf_token = os.getenv("HF_TOKEN")
   ```

## 🎯 Project Goals

- Learn by building and experimenting  
- Understand how LLM APIs work and how to integrate them  
- Explore prompt engineering, embeddings, fine-tuning, and vector search  
- Develop modular tools for reuse across projects  

## 🤝 Contributing

While this is primarily a personal learning project, you're welcome to fork the repo, open issues, or suggest improvements. Knowledge sharing is always welcome!

## 📜 License

This project is licensed under the MIT License.

---

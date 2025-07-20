# 🧠 LLM Journeys

Welcome to **LLM_Journeys**, a personal and practical exploration of Large Language Models (LLMs) from foundational concepts to advanced implementations. This repository is curated and maintained by [Hoon Kim](https://github.com/HoonTheDataSpecialist), a data specialist diving deep into the capabilities, limitations, and applications of LLMs in real-world scenarios.

## 🌐 Repository Overview

This repo serves as a learning journal and implementation space for working with LLMs. It includes:

- 🧪 Experiments and notebooks with Hugging Face Transformers, OpenAI API, and other LLM frameworks  
- 🛠️ Tools and scripts for model inference, prompt engineering, and fine-tuning  
- 📘 Notes and references to papers, tutorials, and best practices  
- 📁 Modular structure for easy extension as learning evolves  

## 📂 Directory Structure

```bash
LLM_Journeys/
├── static/    # 
  ├── HuggingFaceImages/    # 
    ├── generated/    #
├── templates/    # 
├── .env.example    # 
├── .python-version    # 
├── .gitignore    # 
├── APIJourneyUtils.py    # 
├── HuggingFaceJourneysUtils.py    # 
├── LLMJourneyState.py    # 
├── OpenAiJourneyUtils.py    # 
├── README.md    # 
├── app.py    # 
├── requirements.txt    # 
```

## 🧰 Technologies & Tools

- [Hugging Face Models](https://huggingface.co/models)  
- [OpenAI Models](https://platform.openai.com/docs/models)

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

4. **Set Up Api Keys**:
  Create a copy of the `.env.example` file in the root directory of the project to securely store your API keys. Rename it `.env`:
  ```
  OPENAI_API_KEY="hoonisveryintelligent1234"
  HF_TOKEN="hoonishandsome1234"
  ```
  You can create your HF_TOKEN FROM `https://huggingface.co/`. You can create the OPENAI_API_KEY from `https://openai.com/api`.
  When forking, Make sure to **not** commit your `.env` file by adding it to `.gitignore`:

  ```bash
   echo ".env" >> .gitignore
  ```
  Your Python scripts can then access these keys using the `dotenv` package:
   ```python
   from dotenv import load_dotenv
   import os

   load_dotenv()
   ```
## 🎯 Goals

- Learn by building and experimenting  
- Understand the inner workings of LLMs and utilizing them via API
- Explore prompt engineering, fine-tuning, embeddings, and vector search  
- Create modular, reusable tools and workflows  

## 🤝 Contributing

While this is a personal learning project, you're welcome to fork the repo, raise issues, or suggest improvements. Collaboration and knowledge sharing are always welcome!

## 📜 License

This project is licensed under the MIT License.

---

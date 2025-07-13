from openai import OpenAI
from dotenv import load_dotenv
import os
import re
from flask import Flask, render_template, request, session

# Initialize OpenAI client
load_dotenv('.env')

# Create a new Flask app and set the secret key
app = Flask(__name__)
app.secret_key = "mysecretkey"

# Define a function to generate an image using the OpenAI API
def get_img(prompt):
    image_response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return image_response.data[0].url

# Define a function to generate a chat response using the OpenAI API
def chat(inp, message_history, role="user"):

    message_history.append({"role": role, "content": f"{inp}"})
    completion = client.chat.completions.create(
        model="o4-mini",
        messages=message_history
    )
    reply_content = completion.choices[0].message.content
    message_history.append({"role": "assistant", "content": f"{reply_content}"})

    return reply_content, message_history


# Define the homepage route for the Flask app
@app.route('/', methods=['GET', 'POST'])
def home():
    # Page's title:
    title = "GPT-Journey"
    
    button_messages = {}
    button_states = {}

    if request.method == 'GET':
        # initialize 
        session['message_history'] = [{"role": "user", "content": """You are an interactive story game bot that proposes some hypothetical fantastical situation where the user needs to pick from 2-4 options that you provide. Once the user picks one of those options, you will then state what happens next and present new options, and this then repeats. If you understand, say, OK, and begin when I say "begin." When you present the story and options, present just the story and start immediately with the story, no further commentary, and then options like "Option 1:" "Option 2:" ...etc. Keep the story maxed at 5 scenarios."""},
                                      {"role": "assistant", "content": f"""OK, I understand. Begin when you're ready."""}]
        message_history = session['message_history']
        reply_content, message_history = chat("Begin", message_history)
        text = reply_content.split("Option 1")[0]#
        options = re.findall(r"Option \d:.*", reply_content)#

        for i, option in enumerate(options):
            button_messages[f"button{i+1}"] = option

        for button_name in button_messages.keys():
            button_states[button_name] = False

    message = None
    button_name = None
    if request.method == 'POST':

        message_history = session['message_history']
        button_messages = session['button_messages']
        button_name = request.form.get('button_name')
        button_states[button_name] = True
        message = button_messages.get(button_name)
        reply_content, message_history = chat(message, message_history)
        text = reply_content.split("Option 1")[0]#
        options = re.findall(r"Option \d:.*", reply_content)#
        button_messages = {}
        for i, option in enumerate(options):
            button_messages[f"button{i+1}"] = option
        for button_name in button_messages.keys():
            button_states[button_name] = False
    print(text)
    session['message_history'] = message_history
    session['button_messages'] = button_messages
    image_url = get_img(text)

    return render_template('home.html', title=title, text=text, image_url=image_url, button_messages=button_messages, button_states=button_states, message=message)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)
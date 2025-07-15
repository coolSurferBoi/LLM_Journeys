from flask import Flask
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
from flask import Flask, render_template, request, session, redirect, url_for
from APIJourneyUtils import APIJourneyUtils
from GPTJourneyState import GPTJourneyState

app = Flask(__name__)
app.secret_key = "mysecretkey"
api_obj = APIJourneyUtils()

INITIAL_PROMPT = """You are an interactive story game bot. Present a fantastical scenario where the user chooses from 3 options.
After each choice, continue the story and offer 3 new options. Make sure you keep the story to a maximum of 5 steps/selections.
Start directly with the story—no extra commentary—and format choices as 'Option 1:', 'Option 2:', etc.
If you understand, reply 'OK' and wait for me to say 'begin'."""

def init_session_state():
    session['message_history'] = [
        {"role": "user", "content": INITIAL_PROMPT},
        {"role": "assistant", "content": "OK, I understand. Begin when you're ready."}
    ]
    session['button_messages'] = {}

def process_reply(state: GPTJourneyState, reply_content: str):
    """Extracts story and options from reply and updates the button state."""
    text = reply_content.split("Option 1")[0]
    options = re.findall(r"Option \d:.*", reply_content)
    state.reset_message_states()
    state.setup_button_messages(options)
    state.reset_button_states()
    return text


@app.route('/')
def home():
    llm_options = ["o4-mini"]
    image_gen_options = ["dall-e-3","black-forest-labs/FLUX.1-dev"]
    return render_template('home.html', llm_options=llm_options, image_gen_options=image_gen_options)

@app.route('/journey', methods=['GET', 'POST'])
def journey():
    title = "GPT-Journey"
    message = None

    llm = request.args.get('llm') 
    image_gen = request.args.get('image_gen')
    api_obj.setup_LLM_connection(llm)
    api_obj.setup_ImageGen_connection(image_gen)

    # Initialize session and local state manager
    if 'message_history' not in session:
        init_session_state()
    state = GPTJourneyState()
    state.set_button_messages(session.get('button_messages', {}))
    state.reset_button_states()

    message_history = session.get('message_history', [])

    # Handle POST (button clicked)
    if request.method == 'POST':
        button_name = request.form.get('button_name')
        if not button_name or button_name not in state.get_all_button_messages():
            return redirect(url_for('home'))

        state.setup_button_state(button_name)
        message = state.get_button_message(button_name)

        reply_content, message_history = api_obj.chat(llm,message, message_history)
        text = process_reply(state, reply_content)

    # Handle GET (initial load)
    else:
        reply_content, message_history = api_obj.chat(llm,"Begin", message_history)
        text = process_reply(state, reply_content)

    # Get an image for the scene
    image_url = api_obj.get_img(image_gen,text)
    # Update session state
    session['message_history'] = message_history
    session['button_messages'] = state.get_all_button_messages()
    print(f'Number of Selections : {api_obj.get_interaction_count(llm)}')
    return render_template(
        'journey.html',
        title=title,
        text=text,
        image_url=image_url,
        button_messages=state.get_all_button_messages(),
        button_states=state.get_all_button_states(),
        message=message,
        dropdown1 = llm,
        dropdown2 = image_gen
    )

if __name__ == "__main__":
    app.run(debug=True)
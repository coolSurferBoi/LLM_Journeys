from flask import Flask
import re
from flask import Flask, render_template, request, session, redirect, url_for, g
from APIJourneyUtils import APIJourneyUtils
from LLMJourneyState import LLMJourneyState
import uuid

app = Flask(__name__)
app.secret_key = "mysecretkey"
api_obj_store = {}

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

@app.before_request
def load_api_obj():
    game_id = session.get('game_id')
    if not game_id or game_id not in api_obj_store:
        # Create new game session and api_obj
        game_id = str(uuid.uuid4())
        session['game_id'] = game_id
        api_obj_store[game_id] = APIJourneyUtils()
    g.api_obj = api_obj_store[game_id]

def process_reply(state: LLMJourneyState, reply_content: str):
    """Extracts story and options from reply and updates the button state."""
    text = reply_content.split("Option 1")[0]
    raw_options = re.findall(r"Option \d:.*", reply_content)[:3]
    # Remove 'Option N: ' prefix from each option string
    options = [re.sub(r"Option \d:\s*", "", opt) for opt in raw_options]
    
    state.reset_message_states()
    state.setup_button_messages(options)
    state.reset_button_states()
    return text

@app.route('/')
def home():
    llm_options = ["o4-mini","mistralai/Mixtral-8x7B-Instruct-v0.1"]
    image_gen_options = ["dall-e-3","black-forest-labs/FLUX.1-dev"]
    # Initialize session and local state manager
    init_session_state()
    return render_template('home.html', llm_options=llm_options, image_gen_options=image_gen_options)

@app.route('/journey', methods=['GET', 'POST'])
def journey():
    title = "LLM Journey"
    message = None

    llm = request.args.get('llm') 
    image_gen = request.args.get('image_gen')
    g.api_obj.setup_LLM_connection(llm)
    g.api_obj.setup_ImageGen_connection(image_gen)

    state = LLMJourneyState()
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

        reply_content, message_history = g.api_obj.chat(llm,message, message_history)
        text = process_reply(state, reply_content)
        
    # Handle GET (initial load)
    else:
        reply_content, message_history = g.api_obj.chat(llm,"Begin", message_history)
        text = process_reply(state, reply_content)
    image_url = g.api_obj.get_img(image_gen,text)
    session['message_history'] = message_history
    session['button_messages'] = state.get_all_button_messages()
    print(state.get_all_button_messages())
    if not state.get_all_button_messages():
        return render_template(
            'journey.html',
            title=title,
            text=text,
            image_url=image_url,
            button_messages=state.get_all_button_messages(),
            button_states=state.get_all_button_states(),
            message=message,
            dropdown1 = llm,
            dropdown2 = image_gen,
            ending = True
        )
    else:
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

@app.route('/reset')
def reset_game():
    api_obj_store.clear()
    game_id = session.get('game_id')
    api_obj_store[game_id] = APIJourneyUtils()  # fresh instance
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
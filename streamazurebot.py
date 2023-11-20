import os
import azure.cognitiveservices.speech as speechsdk
import re
import asyncio
from quart import (
    Quart,
    render_template,
    request,
    redirect,
    websocket,
    session,
    flash,
)
import json
from hypercorn.asyncio import serve
from hypercorn.config import Config
from collections import deque
import html


hostname = (os.getenv("IP") or "127.0.0.1") + ":" + (os.getenv("PORT") or "5000")
subscription=os.getenv("SPEECH_KEY")
region=os.getenv("SPEECH_REGION") or "eastus"
print("SPEECH_REGION: " + region)
print("Starting server on : " + hostname)

class QueueManager:
    def __init__(self):
        self._moderation_queue = deque()
        self._lock = asyncio.Lock()
        self._modified = asyncio.Event()

    async def get_moderation_queue(self):
        async with self._lock:
            return list(self._moderation_queue)

    async def add_to_moderation_queue(self, message):
        async with self._lock:
            self._moderation_queue.append(message)
            self._modified.set()

    async def pop_from_moderation_queue(self):
        async with self._lock:
            if self._moderation_queue:
                self._modified.set()
                return self._moderation_queue.popleft()
            raise IndexError("pop from an empty queue")

    async def is_empty(self):
        async with self._lock:
            return len(self._moderation_queue) == 0

    async def reset_modified(self):
        self._modified.clear()

    async def wait_for_modified(self):
        await self._modified.wait()

# Initialize the Quart app
app = Quart(__name__, static_folder="static", template_folder="templates")

# Initialize the QueueManager
queue_manager = QueueManager()

# Set the secret key for the app
app.secret_key = os.urandom(24)

def check_env_vars():
    required_vars = ["SPEECH_KEY"]
    for var in required_vars:
        if var not in os.environ:
            raise EnvironmentError(f"Environment variable {var} is not set")
        if not os.environ[var]:
            raise ValueError(f"Environment variable {var} is empty go to Azure Dashboard to get a key")


check_env_vars()

# Extract text inside parentheses and remove it from the original text
def extract_parentheses(text):
    pattern = r"^\((.*?)\)"
    match = re.search(pattern, text)

    if match:
        inside_parentheses = match.group(1)
        text = text.replace(match.group(0), "")
        return inside_parentheses, text
    else:
        return "default", text


#set up speech synthesizer
speech_config = speechsdk.SpeechConfig(subscription,region)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)


def synthesizer_with_style(chatmessage, speech_synthesizer, styledegree, voice, role):
    styleinput, twitch_text = extract_parentheses(chatmessage)
    styleinput = styleinput.lower()
    if not voice:
        voice = "en-US-DavisNeural"

    text = (
        f'<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts"'
        f'xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">'
        f'<voice name="{voice}"><s/><mstts:express-as style="{styleinput}"'
    )
    


    # Add optional parts
    if styledegree:
        text += f' styledegree="{styledegree}"'
    if role:
        text += f' role="{role}"'

    # Finish building the text variable
    text += f'>{twitch_text}</mstts:express-as><s /></voice></speak>'



    speech_synthesis_result = speech_synthesizer.speak_ssml_async(text).get()

    if (
        speech_synthesis_result.reason== speechsdk.ResultReason.SynthesizingAudioCompleted):
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

# WebSocket endpoint for receiving messages from Twitch chat
@app.websocket("/streamerbot")
async def ws_streamerbot():
    while True:
        chosen_message = await websocket.receive()
        chosen_message = html.escape(chosen_message)
        print(chosen_message)
        await queue_manager.add_to_moderation_queue(chosen_message)

# WebSocket endpoint for sending queue to web browser
@app.websocket("/queue")
async def ws():
    while True:
        await queue_manager.wait_for_modified()
        await websocket.send(json.dumps(await queue_manager.get_moderation_queue()))
        await queue_manager.reset_modified()

# Route for the settings page
@app.route("/settings", methods=["GET", "POST"])
async def settings():
    if request.method == "POST":
        form_data = await request.form
        if 'styledegree' in form_data:
            session['styledegree'] = form_data["styledegree"]
        if 'voice' in form_data:
            session['voice'] = form_data["voice"]
        if 'role' in form_data:
            session['role'] = form_data["role"]
        return redirect("/settings")
    return await render_template("settings.html")


# Route for the moderation page
@app.route("/", methods=["GET", "POST"])
async def moderation():
    if request.method == "POST":
        try:
            message = await queue_manager.pop_from_moderation_queue()
        except IndexError as IE:
            await flash("The queue is empty.")
            print(IE)
        form_data = await request.form
        if "allow" in form_data and message is not None:
            synthesizer_with_style(message, speech_synthesizer, session.get('styledegree'), session.get('voice'), session.get('role'))
        return redirect("/")
    return await render_template("moderation.html")

# Main function
if __name__ == "__main__":
    print(os.getpid())
    config = Config()
    config.bind = [hostname]
    asyncio.run(serve(app, config))


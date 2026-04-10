from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openrouter import OpenRouter
import datetime, os, random

load_dotenv()

app = App(token=os.getenv("SLACK_BOT_TOKEN"))

client = OpenRouter(
    api_key=(os.getenv("HCAI-API_KEY")),
    server_url="https://ai.hackclub.com/proxy/v1",
)

cycles = [
    "something an astronaut would use while on a mission",
    "something that would help civilization survive on the moon",
    "something that would help scientists study space better",
]

weeks_theme = random.choice(cycles)

@app.command("/nebuladev")
def callapi(ack, say):
    ack()
    print("Command Acknowlaged!")
    response = client.chat.send(
    model="qwen/qwen3-32b",
    messages=[
        {"role": "user", "content": 
         "You are a slack bot designed to generate one short (1-2 sentacnes) and creative project idea for a event called Nebula."
         "Every week is a new cycle, that means you generate a new project theme. That will be sent bellow!"
         "Please be very carful with formatting, make sure you use Slack Markdown and avoid using an exess of emojis!"
         "This weeks theme is: " + weeks_theme
         }
    ],
    stream=False,
)
    say(response.choices[0].message.content)
    print("Sent to channel!")
if __name__ == "__main__":
    SocketModeHandler(
        app,
        os.getenv("SLACK_APP_TOKEN")
    ).start()
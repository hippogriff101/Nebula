from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openrouter import OpenRouter
import datetime, os

load_dotenv()

app = App(token=os.getenv("SLACK_BOT_TOKEN"))

client = OpenRouter(
    api_key=(os.getenv("HCAI-API_KEY")),
    server_url="https://ai.hackclub.com/proxy/v1",
)

@app.command("/nebuladev")
def callapi(ack, say):
    ack()
    print("Command Acknowlaged!")
    response = client.chat.send(
    model="qwen/qwen3-32b",
    messages=[
        {"role": "user", "content": "Tell me a space themed joke."}
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
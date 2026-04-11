from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openrouter import OpenRouter
from datetime import date
import os
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

anchor = date(2026, 4, 15)
end_date = date(2026, 4, 30)
days = (date.today() - anchor).days
cycle_index = (days // 5) % len(cycles)
weeks_theme = cycles[cycle_index]

@app.command("/nebuladev")
def command(ack, say, respond, command):
    ack()
    print("We got a command!")

    user_text = (command.get("text") or "").strip().lower()

    today = date.today()
    if today < anchor or today > end_date:
        respond(f"This command is only available from {anchor.isoformat()} to {end_date.isoformat()}.")
        return

    if user_text == "idea":
        print("Idea being generated!")
        respond("Hey stargazer, I got your Project Request. Just cooking it up, it'll be with you soon!")
        response = client.chat.send(
        model="qwen/qwen3-32b",
        messages=[
            {"role": "user", "content": 
            "You are a slack bot designed to generate one short (1-2 sentacnes) and creative project idea for a event called Nebula."
            "Please be very carful with formatting, make sure you do not EVER Markdown and avoid using an exess of emojis!"
            "This weeks theme is: " + weeks_theme
            }
        ],
        stream=False,
    )
        say("Yo, <@{user_id}>, here is your idea: " + response.choices[0].message.content)
        print("Sent to channel!")
        return
    if user_text == "joke":
        print("somethin of a joker")
        response = client.chat.send(
        model="qwen/qwen3-32b",
        messages=[
            {"role": "user", "content": 
            "You are a slack bot designed to generate one short space themed joke!"
            "Please be very carful with formatting, make sure you do not EVER Markdown and avoid using an exess of emojis!"
            }
        ],
        stream=False,
    )
        respond("Here is your space joke!: " + response.choices[0].message.content)        
    if user_text == "theme":
        print("We got a THEMER!")
        respond("This cycles's theme is: " + weeks_theme)
        return
    if user_text == "admin":
        respond("*405 : FORBIDEN* - Don't press buttons if you don't know what they do :meow:")
        respond
    else:
        respond("Hey, I'm Nebula Bot! A little slack bot made by <@freddie> for <#nebula>! Unfortunatly just typing my command doesn't do anything; you can do `/nebula theme` to find out this cycles theme or `/nebula idea` to get project ideas!")
if __name__ == "__main__":
    SocketModeHandler(
        app,
        os.getenv("SLACK_APP_TOKEN")
    ).start()
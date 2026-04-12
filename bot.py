from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openrouter import OpenRouter
from datetime import date
import os, time
load_dotenv()

app = App(token=os.getenv("SLACK_BOT_TOKEN"))

CHALLENGER_CHANNEL_ID = os.getenv("CHALLENGER_CHANNEL_ID")
FLAVORTOWN_CHANNEL_ID = os.getenv("FLAVORTOWN_CHANNEL_ID")


def channel_mention(channel_id, fallback_name):
    return f"<#{channel_id}>" if channel_id else f"#{fallback_name}"

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

@app.command("/nebula")
def command(ack, say, respond, command):
    ack()
    print("We got a command!")

    user_text = (command.get("text") or "").strip().lower()
    user_id = command.get("user_id")

    if user_text == "idea":
        today = date.today()
        if today < anchor or today > end_date:
            respond("This command is only available from 15th April to 30th April.")
            return
        else:
            print("Idea being generated!")
            respond("Hey stargazer, I got your Project idea Request. Just cooking it up, it'll be with you soon!")
            response = client.chat.send(
            model="qwen/qwen3-32b",
            messages=[
                {"role": "user", "content": 
                "You are a slack bot designed to generate one short (1-2 sentances) and creative project idea for a event called challenger-space-centre."
                "Please be very carful with formatting, make sure you do not Markdown and avoid using an exess of emojis!"
                "This weeks theme is: " + weeks_theme
                }
            ],
            stream=False,
        )
            say(f"Yo, <@{user_id}>, here is your idea: " + response.choices[0].message.content)
            print("Sent to channel!")
            return
      
    if user_text == "theme":
        print("We got a THEMER!")
        today = date.today()
        if today < anchor or today > end_date:
            respond(f"This command is only available from {anchor.isoformat()} to {end_date.isoformat()}.")
            return
        else:
            respond("This cycles's theme is: " + weeks_theme)
            return

    if user_text == "help":
        respond("*Yo, here's what I can do!*: "
        + "- `/nebula idea` will generate a project idea following this cycles theme"
        + "- `/nebula theme` will tell you what the current cycles theme is"
        + "- `/nebula help` this command your using rn!"
        + "'But what actually is this' -  you may ask! Nebula is a space themed draft YSWS's whos org team is helping with the "
        + f"{channel_mention(FLAVORTOWN_CHANNEL_ID, 'flavortown')} sidequest "
        + f"{channel_mention(CHALLENGER_CHANNEL_ID, 'challenger-space-centre')}!"
        + "Starting on 15th April every five days there is a new cycle! Each cycle has a theme for your project!")
        respond(
            "Any more questions? Ask in "
            + f"{channel_mention(CHALLENGER_CHANNEL_ID, 'challenger-space-centre')}!"
        )
        return
    
    else:
        respond(
            "Hey, I'm Nebula Bot! A little slack bot made by <@freddie> for "
            + f"{channel_mention(CHALLENGER_CHANNEL_ID, 'challenger-space-centre')}! "
            + "Unfortunatly just typing my command doesn't do anything; you can run `/nebula help` to learn more!!"
        )

@app.command("/nebuladev")
def admin(ack, respond, command):
    ack()
    user_id = command.get("user_id")
    if user_id == "U078VN0UU2K":
        respond("Hey Freddie!")
    else:
        respond("This is a dev command for testng - go look at these space pi")
if __name__ == "__main__":
    SocketModeHandler(
        app,
        os.getenv("SLACK_APP_TOKEN")
    ).start()
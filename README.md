# Nebula Bot

 Nebula is a space themed draft YSWS's whos org team is helping with the flavortown sidequest challenger-space-centre! This bot provides some of the funtionality for the revamp of the sidequest!

 ## How to run it yourself!?

Head over to api.slack.com/apps and make a new application, enable socket mode and grab the `APP TOKEN`!

Then, in slack website, make the command needed: `/nebuladev` and `/nebula`!

Next add the following OAuth Bot Scopes:
```
commands
chat:write

```
Your good, install the app to your workspace, get the `BOT TOKEN`!

Head to ai.hackclub.com next and generate an API key!

Now add them into your `.env`!

```
SLACK_BOT_TOKEN=
SLACK_APP_TOKEN=
HCAI-API_KEY=
CHALLENGER_CHANNEL_ID=C0ART2QUS2C
FLAVORTOWN_CHANNEL_ID=C09MPB8NE8H
```
_you also need a few channel ID's I've added here_


> Make a virtual environment:
> ```commandline
> python -m venv .venv
> ```
> then activate it
> on macOS/Linux:
> ```commandline
> source .venv/bin/activate
> ```
> on windows:
> ```commandline
> .\venv\Scripts\activate.bat
> ```
> 
Install dependencies:
```commandline
pip install -r requirements.txt
```
Run the script!

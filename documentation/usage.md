<h1 align="center">BotFramework Usage</h1>

BotFramework provides a AdminBot and a Web User Interface to create/manage other Chatbots. Check out the experience [here](https://www.youtube.com/watch?v=X1D0ceIVELw)
For current version, AdminBot is supported in Slack only.

## Setup
### Pre-requisites
* Create Python v3.6 venv
* Create a new Slack app [here](https://api.slack.com/apps?new_app=1)
* Review and update deploy section for App tokens in [AdminBot.json](../bots/AdminBot/config/AdminBot.json)

```json
"deploy": {
		"channel": "Slack",
		"botControllerPort": "2000",
		"intentControllerPort": "2005",
		"nerControllerPort": "2006",
		"slackInteractPort": "2025",
		"slackSendMessagePort": "2015",
		"slackAppName": "AdminBot",
		"slackBotToken": "",
		"slackVerToken": ""
	}
```

### Library requirements
```python
pip install requirements.txt
```

### Run application
1. Run Bot CoreEngine for AdminBot

```python
python botstart.py AdminBot
```
2. Run Admin API's and UI

```python
python adminstart.py
```



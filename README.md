# IntruderDet

IntruderDet combines OAK-D-Lite with a Telegram ChatBot. On OAK-D-Lite MobileNet-SSD is executed, when a person is detected the telegram bot sends an image ot the user.

Please fill out the token and chat_id variable.
```
token = "TOKEN"
chat_id = "CHAT_ID"
```

## DepthAI

As camera we use OAK-D-Lite and its provided Python API
- https://github.com/luxonis/depthai-python

## Telegram ChatBot

Lazy Times, lets use BotFather
- https://www.freecodecamp.org/news/learn-to-build-your-first-bot-in-telegram-with-python-4c99526765e4/
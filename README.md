# IntruderDet

IntruderDet combines OAK-D-Lite with a Telegram ChatBot. On OAK-D-Lite MobileNet-SSD is executed, when a person is detected the telegram bot sends an image ot the user.

<img src="https://user-images.githubusercontent.com/22636930/153712904-e780b9f1-d3f9-454f-98b4-3532be9c3cb3.jpg" height="300"> <img src="https://user-images.githubusercontent.com/22636930/153712856-2a3d9eef-4c3a-4a07-9e78-5f706d18acc6.jpeg" height="300">

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

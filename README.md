# py_linebot_example
A simple linebot example to get zumba class reservation information

# package requirements
- flask
- beautifulsoup4
- line-bot-sdk 1.5.0 (https://pypi.python.org/pypi/line-bot-sdk/1.5.0)

# Apply a Line@ account / 申請 Line@ 帳號
- https://developers.line.me/en/
- Choose "developer trial" for PUSH_MESSAGE & REPLY_MESSAGE API

# Run
- 1) $> python main.py   # default app port 5000
- 2) $> ngrok http 5000  # This is optional, if you only want to test on your local environment.
- 3) Find the generated https url for your local enviroment and set it as webhook url in line@ setting page.

# TODO
1. Deploy it to Heroku. 

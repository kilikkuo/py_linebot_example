from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from confidential_info import botInfo

# Channel secret
msgVerifier = WebhookHandler(botInfo.secret())

def message_authentication(body, sig):
    # Handle webhook body
    try:
        msgVerifier.handle(body, sig)
    except InvalidSignatureError:
        return False
    return True
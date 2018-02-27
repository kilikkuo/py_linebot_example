from generaltaskthread import TaskThread, Task

class LineMsgTask(Task):
    def __init__(self, user, msg):
        Task.__init__(self)
        self.to = user
        self.msg = msg
    
    def run(self):
        from confidential_info import botInfo
        from linebot import LineBotApi
        from linebot.models import TextSendMessage
        botapi = LineBotApi(botInfo.token())
        botapi.push_message(self.to, TextSendMessage(self.msg))

class InfoSender(TaskThread):
    def __init__(self):
        TaskThread.__init__(self, name ='InfoSender')
    
    def add_msg_task(self, user, msg):
        task = LineMsgTask(user, msg)
        self.addtask(task)

__infosender = None
def start_infosender():
    global __infosender
    if __infosender is None:
        __infosender = InfoSender()
        __infosender.start()

def stop_infosender():
    global __infosender
    if __infosender:
        __infosender.stop()
        __infosender = None

def send_message(user, msg):
    global __infosender
    assert type(msg) == str
    assert __infosender
    __infosender.add_msg_task(user, msg)
    pass

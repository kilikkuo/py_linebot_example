
def convert_weekday_to_str(weekday):
    assert 0 <= weekday <= 6
    weekdaystr = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return weekdaystr[weekday]

class ZumbaAccountInfo(object):
    def __init__(self):
        self.__username = ''
        self.__pwd = ''
        self.__login_url = ''
        self.__schedules_url = ''
        pass

    def login_url(self):
        return self.__login_url
    
    def schedules_url_payload(self, start, end):
        payload = {}
        return self.__schedules_url, payload

    def username(self):
        return self.__username
    
    def password(self):
        return self.__pwd
    
    def process_customized_info(self, sp):
        return None

zumbaInfo = ZumbaAccountInfo()

class LineBotInfo(object):
    def __init__(self):
        self.__token = 'YOUR_CHANNEL_TOKEN'
        self.__secret = 'YOUR_CHANNEL_SECRET'
        self.__test_user_ids = []
        self.__target_user_ids = []

    def token(self):
        return self.__token

    def test_user_ids(self):
        return self.__test_user_ids
    
    def target_user_ids(self):
        return self.__target_user_ids

    def secret(self):
        return self.__secret

botInfo = LineBotInfo()
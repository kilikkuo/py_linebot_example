from generaltaskthread import TaskThread, Task
from confidential_info import zumbaInfo, botInfo
import datetime

class ZumbaInfoCrawler(object):
    def __init__(self, start, end):
        self.__start_date = start
        self.__end_date = end
        self.__session = None
        self.__is_logged_in = False
        self.__sp = None

    def is_logged_in(self):
        return self.__is_logged_in

    def init_session(self):
        import requests

        self.__session = requests.Session()
        url = zumbaInfo.login_url()
        payload = {'username': zumbaInfo.username(), 'password': zumbaInfo.password(),}
        page = self.__session.post(url, payload)
        # 如果上述的網路請求回傳的狀態值不為 ok, 則登入請求失敗.
        if page.ok:
            self.__is_logged_in = True
        print('[Status] Login result : {}'.format(self.__is_logged_in))

    def do_crawl(self):
        assert self.__is_logged_in

        url, payload = zumbaInfo.schedules_url_payload(self.__start_date, self.__end_date)
        r = self.__session.get(url, params=payload)

        from bs4 import BeautifulSoup
        self.__sp = BeautifulSoup(r.content, 'lxml')        
        if self.__sp:
            print('[Status] Crawling class information ok !')
            return True
        return False

    def process_info(self):
        return zumbaInfo.process_customized_info(self.__sp)

class ZumbaInfoCrawlerTask(Task):
    def __init__(self, date_start, date_end):
        Task.__init__(self)
        self.crawler = ZumbaInfoCrawler(date_start, date_end)
    
    def run(self):
        self.crawler.init_session()
        results = []
        if self.crawler.is_logged_in() and self.crawler.do_crawl():
            results = self.crawler.process_info()

        msg = ''
        while len(results) > 0:
            r = results.pop(0)
            msg += str(r)
            msg += '\n' if len(results) else ''
        
        if msg:
            from inforsender import send_message
            users = botInfo.test_user_ids()
            if users:
                send_message(users[0], msg)
        pass

class ZumbaInfoCrawlerThread(TaskThread):
    def __init__(self):
        TaskThread.__init__(self, name ='InfoCrawler')
    
    def add_crawling_task(self, start, end):
        task = ZumbaInfoCrawlerTask(start, end)
        return self.addtask(task)

__infocrawler = None

def get_classinfo_in_coming_week():
    start = datetime.datetime.today()
    end = start + datetime.timedelta(days=6)

    str_start_date = start.strftime('%Y-%m-%d')
    str_end_date = end.strftime('%Y-%m-%d')

    global __infocrawler
    assert __infocrawler
    taskid = __infocrawler.add_crawling_task(str_start_date, str_end_date)

def start_infocrawler():
    global __infocrawler
    if __infocrawler is None:
        __infocrawler = ZumbaInfoCrawlerThread()
        __infocrawler.start()

def stop_infocrawler():
    global __infocrawler
    if __infocrawler:
        __infocrawler.stop()
        __infocrawler = None

if __name__ == '__main__':
    start_infocrawler()
    get_classinfo_in_coming_week()
    import time
    time.sleep(10)
    stop_infocrawler()
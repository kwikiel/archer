from lxml import html
import requests
from queue import Queue
from threading import Thread


URL = 'https://bitlendingclub.com/user/index/id/'
SUFFIX = '/statuses/1/amount/0.00000000%3B0.00000000/invested/true/notInvested/true/reputation/-2000%3B2000/timeLeft/0%3B0/perPage//denomination/1%2C2%2C3/sort-by/apr/direction/desc'
XPATH = '//*[@id="main-wrapper"]/div[1]/div/div[4]/ul/li[1]/a'
BEGIN = 13880
END = 13900


def face(id):
    page = requests.get(URL + str(id)+ SUFFIX)
    tree = html.fromstring(page.text)
    face_id = tree.xpath(XPATH)
    return face_id[0].get('href') if face_id else 'Empty'


def worker():
    while True:
        item = q.get()
        print(item,face(item))
        q.task_done()

q = Queue()
num_worker_threads = 10
for i in range(num_worker_threads):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

for item in range(BEGIN,END):
    q.put(item)

q.join()

worker()

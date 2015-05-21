from lxml import html
import requests
from queue import Queue
from threading import Thread


URL = 'https://bitlendingclub.com/user/index/id/'
XPATH = '//*[@id="main-wrapper"]/div[1]/div/div[4]/ul/li[1]/a'
BEGIN = 1 
END = 30


def face(id):
    page = requests.get(URL + str(id))
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

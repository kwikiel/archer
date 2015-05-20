from lxml import html
import requests
from queue import Queue
from threading import Thread
URL = 'https://bitlendingclub.com/user/index/id/'

def face(id):
    page = requests.get(URL + str(id))
    tree = html.fromstring(page.text)
    face_id = tree.xpath('//*[@id="main-wrapper"]/div[1]/div/div[4]/ul/li[1]/a')
    return face_id[0].get('href') if face_id else 'Empty'


def worker():
    while True:
        item = q.get()
        print(item,face(item))
        q.task_done()

q = Queue()
num_worker_threads = 100
for i in range(num_worker_threads):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

for item in range(1,9000):
    q.put(item)

q.join()

worker()

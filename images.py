from bs4 import BeautifulSoap
import requests


raws = requests.get("https://bitlendingclub.com/user/index/id/13239/brollejonsson")
soup = BeautifilSoup(raws.content)
mydivs = soup.select('.user-pic > img')
print(mydivs[0].get("src"))

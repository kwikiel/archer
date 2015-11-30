from bs4 import BeautifulSoup
import requests


def get_image_link(bid):
    raws = requests.get("https://loanbase.com/user/index/id/"+str(bid))
    soup = BeautifulSoup(raws.content)
    mydivs = soup.select('.user-pic > img')
    print(mydivs[0].get("src"))

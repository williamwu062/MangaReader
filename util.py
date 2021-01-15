import os
import shutil
from bs4 import BeautifulSoup
import requests
import sys
import re


class Manga:
    def __init__(self, chapter, name):
        self.__chapter = chapter
        self.__name = name


class WebsiteUtility:
    @classmethod
    def getRequests(self, url):
        try:
            response = requests.get(url, timeout=10)  # exception handle here
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as h_err:
            print("Http Error:", h_err)
            sys.exit()
        except requests.exceptions.ConnectionError as c_err:
            print("Error Connecting:", c_err)
            sys.exit()
        except requests.exceptions.Timeout as t_err:
            print("Timeout Error:", t_err)
            sys.exit()
        except requests.exceptions.RequestException as err:
            print("Other Exception", err)
            sys.exit()

class Search:
    @staticmethod
    def __urlify(name):
        str = re.sub(r"[^\w\s]", '', name).strip()
        str = re.sub(r"\s+", '+', str)
        return str

    @staticmethod
    def mangaFast_search(name):
        name = Search.__urlify(name)
        link = "https://mangafast.net/?s=" + name
        print(link)
        response = WebsiteUtility.getRequests(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        sresults = soup.find_all('div', attrs={'class': 'ls5'})

        mnames = []
        chlinks = []
        for manga in sresults:
            mname = manga.find('h3').text
            mname = re.sub(r"[\n\t]", '', mname)
            mnames.append(mname)
            chapter = manga.find('a', attrs={'class': 'lats'})['href']
            end = chapter.rindex('chapter')
            chlinks.append(chapter[0:end + 8]) # includes ending dash

        return mnames, chlinks

class Reader:
    @staticmethod
    def mangaFast_chapter_scrape(url):
        response = WebsiteUtility.getRequests(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        img_html = soup.find('div', attrs={'id': 'Read'}).find_all('img')
        print(img_html)
        img_url = []
        for i, img in enumerate(img_html):
            if i == 0:
                img_url.append(img['src'])
            else:
                img_url.append(img['data-src'])
        print(img_url)

        for i, img_link in enumerate(img_url):
            with requests.get(img_link, stream=True) as r:
                directory = "/Users/williamwu/Downloads"
                file = str(i) + ".jpg"
                with open(os.path.join(directory, file), "wb") as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)

name = "naruto"
Search.mangaFast_search(name)
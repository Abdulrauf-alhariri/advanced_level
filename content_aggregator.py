import requests
from bs4 import BeautifulSoup
import feedparser


def google_news(rss_url):
    newfeed = feedparser.parse(rss_url)
    print("Google news")

    for i in range(6):
        new = newfeed.entries[i]
        print(new.title)
        print("url: ", new.link)
        print("###################################")
        print("")
    print("\r\n")


class RedditNews:
    def __init__(self, http_respons):
        self.http_respons = http_respons

    def __str__(self):
        return f"{self.http_respons}"

    @classmethod
    def http_respons(cls):
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        respons = requests.get(
            "https://www.reddit.com/api/trending_searches_v1.json", headers=header).json()
        return cls(respons)

    def trend_news(self):
        news_links = []
        respons = self.http_respons
        news_nr = 0
        print("Reddit trend news")
        for data in respons["trending_searches"]:
            news_nr += 1
            try:
                print("News nr", news_nr, " ", data["results"]["data"]
                      ["children"][0]["data"]["title"])
                print("link", "https://www.reddit.com/" +
                      data["results"]["data"]["children"][0]["data"]["permalink"])
                print("")
            except IndexError:
                pass


reddit_news = RedditNews.http_respons()
google_news("https://news.google.com/news/rss")
reddit_news.trend_news()

from bs4 import BeautifulSoup
import requests

class ParsingCalualties():
    def __init__(self) -> None:
        self.url = "https://index.minfin.com.ua/ua/russian-invading/casualties/"

    def __parse_casualties(self):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en,en-GB;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,uk;q=0.5",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
        source = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(source.content, "lxml", from_encoding="utf-8")
        return soup

    def get_casualties(self):
        soup = self.__parse_casualties()
        result = soup.find("div", class_="casualties").find_all("li")
        return list(map(lambda part: part.text, result))

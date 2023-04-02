from bs4 import BeautifulSoup
import requests

def parse_exchange():
    url = "https://bank.gov.ua/ua/markets/exchangerates"

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en,en-GB;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,uk;q=0.5",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    source = requests.get(url, headers=headers)
    soup = BeautifulSoup(source.content, "lxml", from_encoding="utf-8")
    table = soup.find("table", id="exchangeRates")
    tr = table.find("td", text="USD").parent
    rate = tr.find("td", {"data-label": "Офіційний курс"}).text
    return rate.replace(",", ".")
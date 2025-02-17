import requests


def get_cbr_currency_rate(currency: str = 'USD'):
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url)
    if response.status_code != 200:
        return -1

    from xml.etree import ElementTree as ET
    root = ET.fromstring(response.content)

    for valute in root.findall('Valute'):
        char_code = valute.find('CharCode').text
        if char_code == currency:
            value = valute.find('Value').text
            return float(value.replace(',', '.'))

    raise -1


if __name__ == "__main__":
    usd_rate = get_cbr_currency_rate('USD')
    print(f"Курс доллара США (USD): {usd_rate} рублей")

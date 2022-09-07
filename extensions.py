import requests
import json


class APIException(Exception):
    pass


class Currencies:
    """Класс для получения курсов валют из API (apilayer.com) и вычислений."""
    # Для читаемости k:v не меняли местами, т.к.имена обычно - значения
    names = {'EUR': 'евро', 'USD': 'доллар', 'RUB': 'рубль'}

    @staticmethod
    def get_price(base, quote, amount):
        names_get_id = {Currencies.names[k]: k for k in Currencies.names}
        base, quote = names_get_id[base], names_get_id[quote]
        url = 'https://api.apilayer.com/currency_data/convert?'
        url += f'to={quote}&from={base}&amount={amount}'
        payload = {}
        headers = {"apikey": "XL3zFKf08otrvDjcKBaqWP49P9WteAFd"}
        r = requests.get(url, headers=headers, data=payload)
        print(r.status_code)
        d = json.loads(r.content)
        print(d)
        if d['success'] is True:
            return d['result']
        raise Exception(d['error']['info'])

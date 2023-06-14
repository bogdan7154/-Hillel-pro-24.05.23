import requests
from datetime import datetime
from urllib import parse

def get_currency_iso_code(currency: str) -> int:
    '''
    Функция возвращает ISO код валюты
    :param currency: название валюты
    :return: код валюты
    '''
    currency_dict = {
        'UAH': 980,
        'USD': 840,
        'EUR': 978,
        'GBP': 826,
        'AZN': 944,
        'CAD': 124,
        'PLN': 985,
    }
    try:
        return currency_dict[currency]
    except KeyError:
        raise KeyError('Currency not found! Update currencies information')


def get_currency_exchange_rate(currency_a: str, currency_b: str) -> str:
    currency_code_a = get_currency_iso_code(currency_a)
    currency_code_b = get_currency_iso_code(currency_b)

    response = requests.get('https://api.monobank.ua/bank/currency')
    json = response.json()

    if response.status_code == 200:
        for i in range(len(json)):
            if json[i].get('currencyCodeA') == currency_code_a and json[i].get('currencyCodeB') == currency_code_b:
                date = datetime.fromtimestamp(int(json[i].get('date'))).strftime('%Y-%m-%d %H:%M:%S')
                rate_buy = json[i].get('rateBuy')
                rate_sell = json[i].get('rateSell')
                return f'Курс обмена {currency_a} на {currency_b} на {date}: \nПокупка - {rate_buy} \nПродажа - {rate_sell}'
        return f'Курс обмена {currency_a} на {currency_b} не найден'
    else:
        return f"Ошибка API {response.status_code}: {json.get('errorDescription')}"


def validate_date(date_str: str) -> str:
    '''
    Функция валидации формата даты.
    :param date_str: строка с датой
    :return: дата в формате 'дд.мм.гггг'
    '''
    formats = ['%Y-%m-%d', '%d-%m-%Y', '%d.%m.%Y', '%m.%d.%Y']
    for fmt in formats:
        try:
            date = datetime.strptime(date_str, fmt)
            return date.strftime('%d.%m.%Y')
        except ValueError:
            pass
    return 'Неверный формат даты'


def validate_bank(bank: str) -> str:
    '''
    Функция валидации ввода банка.
    :param bank: строка с названием банка
    :return: название банка в формате 'NB' или 'PB'
    '''
    bank = bank.lower()
    if bank in ['nbu', 'nationalbank', 'national bank', 'nb']:
        return 'NB'
    elif bank in ['pb', 'privatbank', 'privat bank']:
        return 'PB'
    else:
        return ''


def get_pb_exchange_rate(convert_currency: str, bank: str, rate_date: str) -> str:
    validate_date_result = validate_date(rate_date)
    if validate_date_result == 'Неверный формат даты':
        return 'Неверный формат даты'

    bank_code = validate_bank(bank)
    if not bank_code:
        return 'Неверный банк'

    params = {
        'json': '',
        'date': validate_date_result,
    }
    query = parse.urlencode(params)
    api_url = 'https://api.privatbank.ua/p24api/exchange_rates?'
    response = requests.get(api_url + query)
    json = response.json()

    if response.status_code == 200:
        rates = json['exchangeRate']
        for rate in rates:
            if rate['currency'] == convert_currency:
                if bank_code == 'NB':
                    try:
                        sale_rate = rate['saleRateNB']
                        purchase_rate = rate['purchaseRateNB']
                        return f'Курс обмена UAH на {convert_currency} на {validate_date_result} в {bank}: продажа={sale_rate}, покупка={purchase_rate}'
                    except KeyError:
                        return f'Нет курса обмена НБУ для {convert_currency}'
                elif bank_code == 'PB':
                    try:
                        sale_rate = rate['saleRate']
                        purchase_rate = rate['purchaseRate']
                        return f'Курс обмена UAH на {convert_currency} на {validate_date_result} в {bank}: продажа={sale_rate}, покупка={purchase_rate}'
                    except KeyError:
                        return f'Нет курса обмена ПриватБанка для {convert_currency}'
    else:
        return f'Ошибка {response.status_code}'


# Примеры использования функций
result = get_currency_exchange_rate('USD', 'UAH')
print(result)

result = get_pb_exchange_rate('USD', 'PB', '01.11.2022')
print(result)

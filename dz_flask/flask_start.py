from flask import Flask, request
from dz_flask.utils import get_currency_exchange_rate, get_pb_exchange_rate
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p><b>Hello, Worl!</b></p>"


@app.route("/rates", methods=['GET'])
def get_rates():
    currency_a = request.args.get('currency_a', default='USD')
    currency_b = request.args.get('currency_b', default='UAH')
    result = get_currency_exchange_rate(currency_a, currency_b)
    return result


@app.route("/rates_pb", methods=['GET'])
def get_pb_rates():
    convert_currency = request.args.get('convert_currency', default='USD')
    bank = request.args.get('bank', default='NBU')
    bank = validate_bank_input(bank)  # Валидация ввода банка
    rate_date = request.args.get('rate_date', default='01.11.2022')
    rate_date = validate_date_input(rate_date)  # Валидация ввода даты
    result = get_pb_exchange_rate(convert_currency, bank, rate_date)
    return result


def validate_date_input(date_str):
    # Попытка преобразования в формат 'Y-m-d'
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        return date.strftime('%d.%m.%Y')  # Возвращаем дату в формате 'd.m.Y'
    except ValueError:
        pass

    # Попытка преобразования в формат 'd-m-Y'
    try:
        date = datetime.strptime(date_str, '%d-%m-%Y').date()
        return date.strftime('%d.%m.%Y')  # Возвращаем дату в формате 'd.m.Y'
    except ValueError:
        pass

    # Попытка преобразования в формат 'd.m.Y'
    try:
        date = datetime.strptime(date_str, '%d.%m.%Y').date()
        return date.strftime('%d.%m.%Y')  # Возвращаем дату в формате 'd.m.Y'
    except ValueError:
        pass

    # Попытка преобразования в формат 'm.d.Y'
    try:
        date = datetime.strptime(date_str, '%m.%d.%Y').date()
        return date.strftime('%d.%m.%Y')  # Возвращаем дату в формате 'd.m.Y'
    except ValueError:
        pass

    return 'Некорректный формат даты'


def validate_bank_input(bank_str):
    bank_str = bank_str.lower()

    if bank_str in ['nbu', 'nationalbank']:
        return 'NB'
    elif bank_str in ['pb', 'privatbank']:
        return 'PB'
    else:
        return 'Некорректный банк'


if __name__ == '__main__':
    app.run()

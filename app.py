from flask import Flask, request, render_template, jsonify
from flask_wtf import Form
from wtforms import SelectField
from wtforms import DateField
from DH.currencies import FixerIoCurrencies
from json2html import *

BASE_CURRENCIES_LIST_CHOICE = FixerIoCurrencies.get_symbols()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'delivery_hero_secret'

@app.route('/')
def index():
    return render_template('index.jinja2')

@app.route('/historical_rates', methods=['GET', 'POST'])
def historical_rates():

    class CurrencyForm(Form):
        start_date = DateField("Start Date: (YYYY-MM-DD)", format='%Y-%m-%d')
        end_date = DateField("End Date: (YYYY-MM-DD)", format='%Y-%m-%d')
        base_currency_list = SelectField("Base Currency:", choices=BASE_CURRENCIES_LIST_CHOICE, default=47)
    
    form = CurrencyForm()
    latest_result = None
    historical_result = None

    if form.validate_on_submit():
        base_currency_choice = dict(form.base_currency_list.choices).get(form.base_currency_list.data)
        currency = FixerIoCurrencies(base_currency_choice)
        historical_result = json2html.convert(json = currency.get_historical_rate(form.start_date.data, form.end_date.data))
        latest_result = json2html.convert(json = currency.get_latest_rate()['rates'])
    return render_template('historical_rates.jinja2', latest_result = latest_result, historical_result=historical_result, form=form)

if __name__ == '__main__':
    app.debug = True
    app.run()


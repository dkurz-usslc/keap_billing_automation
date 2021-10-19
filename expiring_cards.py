from keap import xml, rest, dir_path, helpers
import datetime
import pandas as pd
import timeit
import os


def get_current_month_year(app):
    today_date = datetime.date.today()
    print(today_date)
    today_year = datetime.date.strftime(today_date, '%Y')
    print(today_year)
    today_month = datetime.date.strftime(today_date, '%m')
    print(today_month)
    find_expiring_cards(today_month, today_year, app)


def find_expiring_cards(exp_month, exp_year, app):
    cards = helpers.query_builder(app=app, table='CreditCard',
                                  return_fields=['Id', 'ContactId', 'Last4', 'ExpirationMonth', 'ExpirationYear',
                                                 'Status'], ExpirationMonth=exp_month, ExpirationYear=exp_year)
    cards_df = pd.DataFrame(data=cards,
                            columns=['card_id', 'contact_id', 'card_last_four', 'exp_month', 'exp_year', 'status'])
    print(cards_df)
    remove_canceled_contacts(app, cards_df)


# def today_order_check(app):
#     pd.set_option('display.max_columns', None)
#     pd.options.display.width = 0
#     app_path = os.path.join(dir_path, app)
#     today = datetime.datetime.today()
#     today_str = today.strftime("%Y-%m-%dT00:00:00.000Z")
#     resp = rest.ListOrders(app_path, {'since': today_str, 'paid': False}).rest_call()
#     remove_canceled_contacts(app, resp)


def remove_canceled_contacts(app, data):
    cancel_set = helpers.get_set_of_canceled_contacts(app)
    card_set = set(data["contact_id"])
    print(card_set)
    not_canceled_card_set = card_set.difference(cancel_set)
    print(not_canceled_card_set)
    not_canceled_card_df = data[data["contact_id"].isin(not_canceled_card_set)]
    print(not_canceled_card_df)


def find_time(app):
    l = helpers.get_set_of_canceled_contacts(app)
    n_l = helpers.test_get_set_of_canceled_contacts(app)
    print(len(l))
    print(len(n_l))
    print(l == n_l)


find_time('ed153')
# get_current_month_year("ed153")
# remove_canceled_contacts('ed153')
# today_order_check('ed153')

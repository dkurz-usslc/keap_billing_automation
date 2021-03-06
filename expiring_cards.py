from keap import xml, rest, dir_path, helpers
import datetime
import pandas as pd
import os


def get_current_month_year():
    today_date = datetime.date.today()
    print(today_date)
    today_year = datetime.date.strftime(today_date, '%Y')
    print(today_year)
    today_month = datetime.date.strftime(today_date, '%m')
    print(today_month)
    find_expiring_cards(today_month, today_year)


def find_expiring_cards(exp_month, exp_year):
    cards = xml.Query(app='ed153',
                      query_search={'ExpirationMonth': exp_month, 'ExpirationYear': exp_year},
                      table='CreditCard',
                      return_fields=['Id', 'ContactId', 'Last4', 'ExpirationMonth', 'ExpirationYear', 'Status']).query()
    cards_df = pd.DataFrame(data=cards,
                            columns=['card_id', 'contact_id', 'card_last_four', 'exp_month', 'exp_year', 'status'])
    print(cards_df)


def remove_canceled_contacts(app):
    app_path = os.path.join(dir_path, app)
    canceled_list = rest.ListContactsWithTag(path=app_path, tag_id=493).rest_call()
    print(canceled_list["next"])
    helpers.flatten_sorter(canceled_list)

def remove_canceled_contacts(app, data):
    cancel_set = helpers.get_set_of_canceled_contacts(app)
    card_set = set(data["contact_id"])
    print(card_set)
    not_canceled_card_set = card_set.difference(cancel_set)
    print(not_canceled_card_set)
    not_canceled_card_df = data[data["contact_id"].isin(not_canceled_card_set)]
    print(not_canceled_card_df)

def today_order_check(app):
    pd.set_option('display.max_columns', None)
    pd.options.display.width = 0
    app_path = os.path.join(dir_path, app)
    today = datetime.datetime.today()
    today_str = today.strftime("%Y-%m-%dT00:00:00.000Z")
    resp = rest.ListOrders(app_path, {'since': today_str, 'paid': False}).rest_call()
    print(resp)
    helpers.flatten_sorter(resp)

def find_time(app):
    l = helpers.get_set_of_canceled_contacts(app)
    n_l = helpers.test_get_set_of_canceled_contacts(app)
    print(len(l))
    print(len(n_l))
    print(l == n_l)

# get_current_month_year()
remove_canceled_contacts('ed153')
# today_order_check('ed153')

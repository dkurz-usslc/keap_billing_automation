from keap import xml, rest, dir_path, helpers
import os


# Need to pull fields, determine product based on number of payments, confirm dates, create order, determine credit
# card to use, replace payment plan/process order

# status draft?
def create_test(app):
    app_path = os.path.join(dir_path, app)
    con_id = 547234
    order_data = {
        "contact_id": con_id,
        "order_date": "2021-12-18T06:00:00.000Z",
        "order_items": [{
          "product_id": 142,
          "quantity": 1
        }],
        "order_title": "Test Order",
        "order_type": "Online",
        "lead_affiliate_id": 61582,
        "sales_affiliate_id": 61582
        }
    cards = rest.ListContactCards(path=app_path, contact_id=con_id).rest_call()
    q = helpers.query_builder(app, "CreditCard", ["ContactId", "Id", "Status", "ExpirationMonth", "ExpirationYear",
                                                "Last4"], ContactId=con_id, Status=3)
    f = rest.GetContactFields(path=app_path).rest_call()
    print(f)
    p = rest.GetContactProperties(path=app_path, contact_id=con_id).rest_call()
    dicts = p["custom_fields"]
    fields = [item for item in dicts if item["id"] in [108, 110, 112, 114, 116, 118] and item["content"] is not None]
    print(fields)
    # resp = rest.CreateOrder(path=app_path, data=order_data).rest_call()


create_test('ed153')

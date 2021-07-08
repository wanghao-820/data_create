from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":

    test = Renewal()

    uid = 445
    clazz_id = 3579
    order_id = test.get_order_id_from_payment(uid,clazz_id)
    portal_apis.exchange_order_user(order_id=order_id, to_user_id=446)
    
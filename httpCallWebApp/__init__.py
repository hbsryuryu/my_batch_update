import azure.functions as func
import json

# ----------------------------------

import os
import stripe

STRIPE_SECRET = os.environ["STRIPE_SECRET"]
stripe.api_key = STRIPE_SECRET

import time
import unicodedata
from datetime import datetime
from zoneinfo import ZoneInfo

TIME_META_TAG = "lecture_start_date"


# 文字検査
def str_datetime_transform(datetime_str):
    if type(datetime_str) != str:
        return None
    if len(datetime_str) <= 5:
        return None # 年と月と日だけで最低でも６文字はある
    
    datetime_str = datetime_str.replace("/","-")
    datetime_str = datetime_str.replace("年","-").replace("月","-").replace("日","-")

    reconstruction_datetime = ""
    for _d in datetime_str.split("-"):
        if len(_d) >= 2:
            reconstruction_datetime += _d
        if len(_d) == 1:
            reconstruction_datetime += "0"+_d
            


    zenkaku = reconstruction_datetime
    hankaku = unicodedata.normalize('NFKC', zenkaku)

    return datetime.fromisoformat(hankaku)


def trial_days_remaining(datetime_str):
    try:
        input_datetime = str_datetime_transform(datetime_str)
    except: # azure functionsでは見えないので、握りつぶす
        return None
    if not input_datetime:
        return None
    

    right_now = datetime.now(ZoneInfo("Asia/Tokyo"))

    now = datetime(right_now.year,right_now.month,right_now.day)
    unix_time_now = int(now.timestamp())
    unix_time_input_datetime = int(input_datetime.timestamp())

    if (unix_time_input_datetime < unix_time_now):
        return None # 操作不要
    
    return (input_datetime - now).days

def stripe_paymentLink_get_list():
    time.sleep(1) # リクエストしすぎ防止
    payment_links_list = stripe.PaymentLink.list(limit=30)
    # payment_links_list.has_more
    # payment_links_list.keys() # ['object', 'data', 'has_more', 'url']
    return payment_links_list

def stripe_paymentLink_modify(payment_link_id:str,remaining_days:int):
    time.sleep(1) # リクエストしすぎ防止
    payment_link = stripe.PaymentLink.modify(
        payment_link_id,
        subscription_data={"trial_period_days": remaining_days}
    )
    return payment_link









def my_function():
    res_array = []

    payment_links = stripe_paymentLink_get_list()
    payment_links_ids_trial_period_days_tuple = [
        (_p.id,_p.subscription_data,_p["metadata"].get(TIME_META_TAG,None))
        for _p in payment_links.data
    ]
    # subscription_dataのアクセス先はsubscription_data.trial_period_days

    for _id,_s_data,_s_meta_time_str in payment_links_ids_trial_period_days_tuple:
        if _s_data is None:
            continue
        else:
            datetime_str = _s_meta_time_str
            
            current_days = _s_data.trial_period_days # なければnull定義してくれている
            target_days = trial_days_remaining(datetime_str)
            target_id = _id


            if target_days == 0:
                target_days = None # 0日指定は対応してない
            if target_days and current_days:
                res_array.append(target_days)
                # res_data = stripe_paymentLink_modify(target_id,target_days) # 無料トライアルが設定されているかつ更新が必要なものだけリクエスト


    return res_array

# ----------------------------------











def main(req: func.HttpRequest) -> func.HttpResponse:
    test_id = req.params.get("test_id")

    # payment_links = stripe_paymentLink_get_list()
    # payment_links_ids_trial_period_days_tuple = [
    #     _p.id
    #     for _p in payment_links.data
    # ]
    

    # result_json = {"tests": [test_id]}
    result_json = {
        "key":STRIPE_SECRET[:3],
        "tests": [test_id],
        "ids": my_function() # payment_links_ids_trial_period_days_tuple

    }
    return func.HttpResponse(
        json.dumps(result_json, ensure_ascii=False),
        mimetype="application/json",
        charset="utf-8",
        status_code=200
    )


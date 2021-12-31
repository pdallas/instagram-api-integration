import time
from pymongo import MongoClient
from get_insta_acc import getIgUserInfo
from defines import getCreds
import os

params = getCreds()  # get creds
params['debug'] = 'no'  # set debug
mongodb_hostname = os.environ.get("MONGO_HOSTNAME", "localhost")
mongo_client = MongoClient('mongodb://' + mongodb_hostname + ':27017/')
db = mongo_client['IGUSERS']
# crate a table in mongodb
service_users = db["Users"]
ig_account_info = db["ig_account_info"]


def backround_task_update_accounts():
    delay = 20
    print("Task running..")
    add_accounts = getIgUserInfo(params)
    ex_insta_accounts = ig_account_info.find_one({"id": "17841406665384366"})
    if ex_insta_accounts is None:
        for obj in add_accounts:
            ig_account_info.insert_one(obj)
        print("Added.")
    else:
        i = 0
        for obj in add_accounts:
            myquery = {"id": obj["id"]}
            newvalues = {
                "$set": {"followers_count": obj["followers_count"]}
            }
            ig_account_info.update_one(myquery, newvalues)
            i = i + 1
        print("Updated " + str(i) + " records.")
    print(f"Simulating {delay} second delay..")
    time.sleep(delay)
    print("Task completed.")

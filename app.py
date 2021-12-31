from influxdb import InfluxDBClient
from pymongo import MongoClient
from flask import Flask, redirect, session, url_for, render_template, request, flash
import bcrypt
import os
from defines import getCreds
from get_insta_acc import getIgUserInfo
import json
import time
from rq import Queue, Worker
from rq.decorators import job
import redis
from story_insights import loops
from backround_tasks import backround_task_update_accounts

# from flask_caching import Cache
# from celery import Celery
# from make_celery import make_celery


# params = getCreds()  # get creds
# params['debug'] = 'no'  # set debug

# MongoDB
mongodb_hostname = os.environ.get("MONGO_HOSTNAME", "localhost")
mongo_client = MongoClient('mongodb://' + mongodb_hostname + ':27017/', maxPoolSize=3)
db = mongo_client['IGUSERS']
# crate a table in mongodb
service_users = db["Users"]
ig_account_info = db["ig_account_info"]

# Influx
client = InfluxDBClient(host='localhost', port=8086)
client.create_database("igtest")
client.switch_database("igtest")
# print(client.get_list_database())
# client.switch_database("TheWebNirTest")

# Flask
app = Flask(__name__)

# redis server
r = redis.Redis()
# initialize queue
q = Queue(connection=r)
# start the worker binded with the Queue (q) = doesnt work yet --- >
# https://pymongo.readthedocs.io/en/stable/faq.html#pymongo-fork-safe-details
# worker = Worker([q], connection=r)
# worker.work(burst=True)

# generate a secret key
app.secret_key = os.urandom(16)

# cache = Cache(app, config={'CACHE_TYPE': 'redis',
#                            'CACHE_KEY_PREFIX': 'server',
#                            'CACHE_REDIS_HOST': 'localhost',
#                            'CACHE_REDIS_PORT': '6379',
#                            'CACHE_REDIS_URL': 'redis://localhost:6379'
#                            })

data = {
    "name": "",
    "email": "",
    "password": "",
    "category": ""
}


@app.route('/')
@app.route('/home')
def index():
    # first time set up
    ex_users = service_users.find_one({"category": "admin"})
    if ex_users is None:
        passw = b"admin"  # set default bytestring password "admin" and hash it before adding it to our DB
        hashedpw = bcrypt.hashpw(passw, bcrypt.gensalt(12))
        first_user = {"name": "admin", "email": "admin@monitor.net", "password": hashedpw, "category": "admin"}
        service_users.insert_one(first_user)
    return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    # initialize backround task if GET method used.
    backround_update_accounts()
    if request.method == "POST":
        login_mail = request.form["login_mail"]
        login_pw = request.form["login_password"]
        # check for missing information
        if login_mail == "" or login_pw == "":
            flash("To login you must fill the required fields! Please retry")
            return redirect(url_for("login"))
        # search in the database for that email address
        sumbitted_mail = service_users.find_one({"email": login_mail})
        if sumbitted_mail is None:
            # let the client know that his email doesnt belong to our db, by flashing the message:
            flash("This email is not registered in our service, please contact support!")
            return redirect(url_for("login"))
        else:
            if bcrypt.checkpw(login_pw.encode("utf-8"), sumbitted_mail["password"]):
                flash("password matches")
                return redirect(url_for("store_accounts"))
            else:
                flash("Wrong password. Please try again!")
                return redirect(url_for("login"))
    return render_template('login.html')


@app.route('/logout')
def logout():
    # clear all session saved data.
    session.clear()
    # redirect to /login after logging out.
    return redirect("login")


@app.route('/store_accounts', methods=["POST", "GET"])
def store_accounts():
    """ need to add caching"""
    activeIGids = []
    activeIGusernames = []
    ig_account_list = []
    if request.method == "POST":
        # get the value of the button pressed (button values are defined by ig name)
        selectedstore = request.form.get("selectedstore")
        return redirect(url_for("account", usr=selectedstore))

    new = ig_account_info.find({})
    for number, cursor in enumerate(new):
        name = cursor.get("name")
        username = cursor.get("username")
        igid = cursor.get("id")
        followers_count = cursor.get("followers_count")
        media_count = cursor.get("media_count")
        biography = cursor.get("biography")
        k = {
            'number': number + 1,
            'name': name,
            'username': username,
            'id': igid,
            'followers_count': followers_count,
            'media_count': media_count,
            'biography': biography
        }
        activeIGids.append(k["username"])
        activeIGids.append(k["id"])
        ig_account_list.append(k)
    session["active_stores"] = activeIGids
    return render_template('store_accounts.html', accounts=ig_account_list)


@app.route("/store_accounts/<usr>", methods=["POST", "GET"])
def account(usr):
    for igid, store in enumerate(session["active_stores"]):
        next_id = igid + 1
        if store == usr:
            print(session["active_stores"])
            #ig_id = session["active_stores"][next_id]
            #print(ig_id)
            # retrieve story insights for the selected store
            new = loops(store)

            json_body = [{
                "measurement": store,
                " tags": {
                    "taps_fw": new[4],
                    "taps_bw": new[5]
                },
                "fields": {
                    "exits": new[0],
                    "impressions": new[1],
                    "reach": new[2],
                    "replies": new[3]
                }
            }]

            return f"<h1>{json_body}</h1>"

    return redirect(url_for("store_accounts"))


@app.route('/change_pw')
def changepw():
    return 'Hello world!'


@job('q', connection=r)
def backround_update_accounts():
    job_ = q.enqueue(backround_task_update_accounts)
    q_len = len(q)
    return print(f"Task {job_.id} added to queue at {job_.enqueued_at}. {q_len} tasks in the queue")


if __name__ == '__main__':
    app.run(debug=True, port=5000)


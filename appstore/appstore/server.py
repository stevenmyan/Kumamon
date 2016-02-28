# coding=utf-8
__author__ = 'jing'

from flask import Flask, render_template
import pymongo
from settings import MONGO_URI, MONGO_DATABASE

app = Flask(__name__)  # instantiate flask


@app.route("/")  # 这里的路径是基本域名之后的路径! 当返回路径为"/"时,即返回路径为基本域名时,用这个hello()处理
def appstore():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]
    print MONGO_DATABASE
    apps = db["AppstoreItem"].find()
    client.close()
    return render_template("appstore_index.html", apps=apps)  # render anything we have in each app


if __name__ == "__main__":
    app.run()

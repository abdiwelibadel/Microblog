import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient

from dotenv import load_dotenv

load_dotenv()

def create_app():

    app = Flask(__name__)

    client = MongoClient(os.getenv("MONGODB_URI"))

    app.db = client.Microblog



    @app.route('/', methods=["GET", "POST"])

    def index():
        if request.method == "POST":

            entry_content = request.form.get("content")
            formated_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formated_date})
        entries_with_date = [
            (
            entry["content"],
            entry["date"],
            datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
            ]
        return render_template("index.html", entries=entries_with_date)
    return app
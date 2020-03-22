import os
import requests

from flask import Flask, session, request, render_template, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_session import Session

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

channels_list = []
messages = [{"channel_name": "channel_name",
            "message_text": "message_text",
            "username": "user_id",
            "timestamp": "timestamp"
          }]

@app.route("/")
def index():
    if "user_id" not in session:
       username = None
    else:
       username = session["user_id"]

    return render_template("index.html", username=username)

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")

        if username is None or len(username) == 0:
            return render_template("heythere.html", message="Username must not be blank")
        else:
            session["user_id"] = username
            return redirect(url_for('channels'))


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return render_template("heythere.html", message="You are logged out")


@app.route("/channels", methods=["GET", "POST"])
def channels():

    if request.method == "GET":
        if "user_id" not in session:
            return render_template("heythere.html", message="You are not logged in")
        else:
            return render_template("channels.html", username=session["user_id"], channels=channels_list)

    if request.method == "POST":
        channel_name = request.form.get("channel_name")

        if channel_name is None or len(channel_name) == 0:
            return render_template("heythere.html", message="Channel name must not be blank")
        else:
            channels_list.append(channel_name)
            return render_template("channels.html", channels=channels_list)

@app.route("/channel_details/<string:channel_name>", methods=["GET"])
def channel_details(channel_name):

    if "user_id" not in session:
        return render_template("heythere.html", message="You are not logged in")

    messages_in_channel = []

    for message in messages:
        if message["channel_name"] == channel_name:
            messages_in_channel.append(message)

    return render_template("channel_details.html", messages=messages_in_channel, channel=channel_name, username=session["user_id"])


@socketio.on("send message")
def send(data):
    message_text = data["message_text"]
    timestamp = data["timestamp"]
    channel_name = data["channel_name"]
    message = {"channel_name": channel_name,
                "message_text": message_text,
                "username": session["user_id"],
                "timestamp": timestamp
              }

    messages_in_channel = []
    removed_message = {}

    for i in messages:
        if i["channel_name"] == channel_name:
            if len(messages_in_channel) >= 9:
                removed_message = messages_in_channel.pop(0)
            messages_in_channel.append(i)

    if removed_message != {}:
        messages.remove(removed_message)

    messages.append(message)

    emit(
        "announce message",
        message,
        broadcast=True
    )

@socketio.on("delete message")
def delete(data):
    message_text = data["message_text"]
    timestamp = data["timestamp"]
    channel_name = data["channel_name"]
    message = {"channel_name": channel_name,
                "message_text": message_text,
                "username": session["user_id"],
                "timestamp": timestamp
              }

    messages.remove(message)


if __name__ == '__main__':
    socketio.run(app)

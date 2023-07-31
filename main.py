import requests
from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def index():
    headers = {
    'Authorization': 'Bearer xoxb-2210535565-5678767726737-zgzdld6CkY5HPbPrI9kogcc8'
    }
    r = requests.get("https://slack.com/api/conversations.history?channel=C0M8PUPU6", headers=headers).json()
    msgs = []
    i = 0
    while len(msgs) < 11:
        if r['messages'][i]['text'] == "This message was deleted.": i+=1; continue
        text = r["messages"][i]["text"]
        if text == "": text = "(No text)"
        msgs.append({
            "text": text,
            "user": r["messages"][i]["user"],
            "ts": r["messages"][i]["ts"],
        })
        i += 1

    for msg in msgs:
        msg['id'] = "boat"+str(msgs.index(msg))
        userid = msg['user']
        user = requests.get("https://slack.com/api/users.info?user="+userid, headers=headers).json()["user"]
        msg["user"] = user["profile"]['display_name']
        msg['pfp'] = user["profile"]['image_512']
        link = requests.get("https://slack.com/api/chat.getPermalink?channel=C0M8PUPU6&message_ts="+msg["ts"], headers=headers).json()["permalink"]
        msg["link"] = link
    print(msgs)
    return render_template('index.html', msgs=msgs)

app.run(host='0.0.0.0', port=4576, debug=True)
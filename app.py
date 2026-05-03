from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GARENA_URL = "https://100067.connect.garena.com/oauth/guest/token/grant"

def get_access_token(uid, password):
    headers = {
        "User-Agent": "GarenaMSDK/4.0.19P4",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_id": "100067",
        "client_secret": ""
    }

    try:
        res = requests.post(GARENA_URL, headers=headers, data=data, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}


@app.route("/get", methods=["GET"])
def login():
    uid = request.args.get("uid")
    password = request.args.get("password")

    if not uid or not password:
        return jsonify({"status": "error", "message": "uid/password required"})

    data = get_access_token(uid, password)

    if "access_token" not in data:
        return jsonify({
            "status": "error",
            "message": "login failed",
            "response": data
        })

    return jsonify({
        "status": "success",
        "access_token": data["access_token"],
        "open_id": data.get("open_id")
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8792, debug=True)
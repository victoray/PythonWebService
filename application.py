import os

import gnupg

from flask import Flask, request, jsonify, json
from werkzeug.exceptions import HTTPException

app = Flask("__main__")


@app.route("/decryptMessage", methods=['POST'])
def decryptMessage():
    if not request.data:
        return jsonify(dict(name="Empty Message Body"))

    message = request.get_json().get('message')
    passphrase = request.get_json().get('passphrase')

    if not message or not passphrase:
        return jsonify(dict(name="Invalid Message Body"))

    gpg = gnupg.GPG(os.popen("which gpg").read().strip())
    decrypted = str(gpg.decrypt(message, passphrase=passphrase)).strip()
    decryptedMessage = {'DecryptedMessage': f"{decrypted}"}

    if len(decrypted) == 0:
        return jsonify(dict(name="Invalid Passphrase"))

    return jsonify(decryptedMessage)


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if "__main__" == __name__:
    app.debug = True
    app.run()

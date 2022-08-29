from flask import Flask, request, make_response, abort
from flask_cors import CORS
import requests
import json
import base64
import time
app = Flask(__name__)
CORS(app)
clientID = '081b69bc044e41d59d9d28bb6c8a4305'
clientSec = '9f61c2a752f14404959fc989e0d2cbef'
l = f'{clientID}:{clientSec}'
l = l.encode("utf-8")
accessTokenTime = 0
access_token = None


def getToken():
    global accessTokenTime
    global access_token
    if time.time() > accessTokenTime + 3600:
        clientAuth = f'Basic {base64.b64encode(l).decode("utf-8")}'
        r = requests.post('https://accounts.spotify.com/api/token', data={'grant_type':'client_credentials'}, headers={'Content-Type' : 'application/x-www-form-urlencoded', 'Authorization' : clientAuth})
        accessTokenTime = time.time()
        access_token = r.json()['access_token']
        return access_token
    else:
        return access_token



@app.route('/search', methods=["POST"])
def search():
    search = requests.get(f'https://api.spotify.com/v1/search?type=track&market=UG&include_external=audio&q={request.json["query"]}', headers={'Authorization': f'Bearer {getToken()}'})
    return search.json()

@app.route('/', methods=["POST"])
def main():
    return getToken() 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
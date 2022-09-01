from flask import Flask, request, make_response, abort, redirect
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
print(base64.b64encode(l))
accessTokenTime = 0
access_token = None

accessToken = None
refreshToken = None
refreshTime = None

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

def getRefreshedToken():

        if code.status_code == 200:
            refreshTime = time.time()
            accessToken = code.json()['access_token']
            refreshToken = code.json()['refresh_token']
    pass

@app.route('/search', methods=["POST"])
def search():
    search = requests.get(f'https://api.spotify.com/v1/search?type=track,album&market=UG&include_external=audio&q={request.json["query"]}', headers={'Authorization': f'Bearer {getToken()}'})
    return search.json()

@app.route('/queue', methods=["POST", "GET"])
def addtoqueue():
    if request.method == "POST":
        queue = requests.get(f'https://api.spotify.com/v1/me/player/devices', headers={'Authorization': f'Bearer {getToken()}'})
    elif request.method == "GET":
        queue = requests.get(f'https://api.spotify.com/v1/me/player/queue')
    return queue.json()

@app.route('/login')
def login():
    return redirect('https://accounts.spotify.com/authorize?client_id=081b69bc044e41d59d9d28bb6c8a4305&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A5555%2Fcallback&scope=user-modify-playback-state%20user-read-playback-state%20user-read-currently-playing%20user-read-playback-position%20&show_dialog=false')

@app.route('/callback')
def callback():
    global accessToken
    global refreshToken
    print(request.args.get("code"))
    code = requests.post(f'https://accounts.spotify.com/api/token?grant_type=authorization_code&code={request.args.get("code")}&redirect_uri=http%3A%2F%2Flocalhost%3A5555%2Fcallback', headers={'Authorization': f'Basic {base64.b64encode(l).decode("utf-8")}', 'Content-Type':'application/x-www-form-urlencoded'})
    
    return code.json()

@app.route('/', methods=["POST"])
def main():
    return getToken()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)

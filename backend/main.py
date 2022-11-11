# Flask imports
import base64
import json
import string
import flask, flask_login
from flask_cors import CORS
from flask import Flask, Response, request, redirect, jsonify, send_file

import os, requests, random

# start basic flask app
app = Flask(__name__)

# CORS SETTINGS
CORS(
    app,
    origins=["http://127.0.0.1:3000", "http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:5173"],
    supports_credentials=True,
)


# import spotify_token
from spotify_token import get_access_token

# ENVIRONMENT VARIABLES
from dotenv import load_dotenv, find_dotenv




# load environment variables
load_dotenv(find_dotenv())

token = ''

# write hello path
@app.route('/')
def hello():
		return 'Hello World!'

# access_token = ''
HEADERS = {
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'Authorization': 'Bearer BQAvD324yAbPwrXfoDkC4aTs-k02GJmH2ITyPVf85VknhYfhyLl0c8V6SJ9r061cH3Y8djrSzPxPIPMfjaAOUC8R2-7Rf8nDwU_lm_lDJTDZGywa1pq-HZhW_T0ELDVyUlLIWEq3bx3AkBUMD_fGtyGrUp5UyOQMoallekIJ1Yzc9S3DpLHPGG-00yiO7KM5BMKUx-r-FC_AkkDoAFs'
}

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

# Get Current User's Playlists
@app.route('/current/playlists')
def get_current_user_playlists():
	HEADERS = {
		'Content-Type': 'application/json',
		'Accept': 'application/json',
		'Authorization': f'Bearer {os.environ.get("ACCESS_TOKEN")}'
	}
	r = requests.get(BASE_URL + 'me/playlists', headers=HEADERS)
	r = r.json()
	return jsonify(r)


# Spotify
AUTH_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI = "http://localhost:5001/callback"

@app.route('/login')
def login():
	# generate random string for state of length 16
	state = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
	# set scope
	scope = 'user-read-private'

	# redirect to spotify login page
	return redirect(f'https://accounts.spotify.com/authorize?response_type=code&client_id={os.environ.get("CLIENT_ID")}&scope={scope}&redirect_uri={REDIRECT_URI}&state={state}')

@app.route('/callback')
def callback():
	code = request.args.get('code')
	state = request.args.get('state')

	b = base64.b64encode(bytes(f'{os.environ.get("CLIENT_ID")}:{os.environ.get("CLIENT_SECRET")}','utf-8')).decode('utf-8')

	if not state:
		return redirect('/?error=state_mismatch')
	else:
		authOptions = {
			'url': 'https://accounts.spotify.com/api/token',
			'form': {
				'code': code,
				'redirect_uri': REDIRECT_URI,
				'grant_type': 'authorization_code'
			},
			'headers': {
				'Authorization': 'Basic ' + b
			},
			'json': True
		}
	r = requests.post(authOptions['url'], data=authOptions['form'], headers=authOptions['headers'])
	r = r.json()
	# set refresh token environment variable
	os.environ['REFRESH_TOKEN'] = r['refresh_token']
	# set access token environment variable
	os.environ['ACCESS_TOKEN'] = r['access_token']

	return jsonify(r)

@app.route('/refresh-access-token')
def refresh_access_token():
	refresh_token = os.environ.get('REFRESH_TOKEN')
	b = base64.b64encode(bytes(f'{os.environ.get("CLIENT_ID")}:{os.environ.get("CLIENT_SECRET")}','utf-8')).decode('utf-8')
	auth_options = {
		'url': 'https://accounts.spotify.com/api/token',
		'headers': {
			'Authorization': 'Basic ' + b
		},
		'form': {
			'grant_type': 'refresh_token',
			'refresh_token': refresh_token
		},
		'json': True
	}
	r = requests.post(auth_options['url'], data=auth_options['form'], headers=auth_options['headers'])
	r = r.json()
	return jsonify(r)


@app.route('/success-login')
def success_login():
	return 'Success'

@app.route('/track')
def get_track():
	r = requests.get('https://api.spotify.com/v1/audio-features/06AKEBrKUckW0KREUWRnvT', headers=HEADERS)
	r = r.json()
	return jsonify(r)


@app.route('/me/profile')
def get_me():
	# get access token from environment variable
	access_token = get_access_token()

	print(f"ACCESS_TOKEN = {access_token}")
	HEADERS = {
		'Content-Type': 'application/json',
		'Accept': 'application/json',
		'Authorization': 'Bearer ' + access_token
	}
	r = requests.get('https://api.spotify.com/v1/me', headers=HEADERS)
	r = r.json()
	return jsonify(r)

def get_access_token():
	login()
	return os.environ.get('ACCESS_TOKEN')


@app.route('/me/top')
def get_top_items():
	# get access token from environment variable
	access_token = get_access_token()

	# read from query string
	type = request.args.get('type')
	HEADERS = {
		'Content-Type': 'application/json',
		'Accept': 'application/json',
		'Authorization': 'Bearer ' + access_token
	}
	r = requests.get('https://api.spotify.com/v1/me/top/{type}', headers=HEADERS)
	r = r.json()
	return jsonify(r)

@app.route('/me/playlists')
def get_playlists():
	# get access token from environment variable
	access_token = get_access_token()

	HEADERS = {
		'Content-Type': 'application/json',
		'Accept': 'application/json',
		'Authorization': 'Bearer ' + access_token
	}
	r = requests.get('https://api.spotify.com/v1/me/playlists', headers=HEADERS)
	r = r.json()
	res = [n['href'] for n in r['items']]
	return jsonify(res)

# run app
if __name__ == '__main__':
	# run app
	app.run(debug=True, host='localhost', port=5001)
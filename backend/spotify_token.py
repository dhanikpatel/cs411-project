import requests, os
from dotenv import load_dotenv



# Spotify
AUTH_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI = "http://localhost:5001/callback"


# Get Spotify Access Token
def get_access_token():
	request_body = {
        "grant_type": 'client_credentials',
				"scope": "playlist-modify-private user-library-read",
        "client_id": os.getenv('CLIENT_ID'),
        "client_secret": os.getenv('CLIENT_SECRET'),
    }
	r = requests.post(url=AUTH_URL, data=request_body)
	r = r.json()
	# set envinronment variable
	os.environ['ACCESS_TOKEN'] = r['access_token']
	return r['access_token']


if __name__ == "__main__":
	access_token = get_access_token()
	print("Access Token: ", access_token)
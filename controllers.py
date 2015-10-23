import json
import gspread, requests
from oauth2client.client import SignedJwtAssertionCredentials

def overall():
	json_key = json.load(open('./keys/requirements.json'))
	scope = ['https://spreadsheets.google.com/feeds']

	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

	gc = gspread.authorize(credentials)

	# Open the first worksheet
	standings = gc.open('Copy of IM Schedule and Standings').sheet1

	# Fetch overall rankings
	overall = standings.range('B3:D15')
	table = []

	for cell in overall:
		val = cell.value
		table.append(val)

	return table

def instagram():
	client_id = '574722ec06494eb79b0b9615ecd593cb'
	base_api = 'https://api.instagram.com/v1/'

	# Get 20 most recent posts with #CapitalOne tag
	result = requests.get(base_api + 'tags/CapitalOne/media/recent?count=20&client_id=' + client_id)

	captions = []
	likes = []
	images = []
	users = []

	data = result.json()['data']

	for post in data:
		captions.append(post['caption']['text'])
		likes.append(post['likes']['count'])
		images.append(post['images']['thumbnail']['url'])
		users.append(post['user']['username'])

	return { 'captions':captions, 'likes':likes, 'images':images, 'users':users }

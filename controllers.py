import json, time, os
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
	client_id = os.environ['INSTAGRAM_CLIENT_ID']
	insta_api = 'https://api.instagram.com/v1/'
	sentiment_api = 'http://text-processing.com/api/sentiment/'

	# Get 20 most recent posts with #CapitalOne tag
	result = requests.get(insta_api + 'tags/CapitalOne/media/recent?count=20&client_id=' + client_id)

	times = []
	captions = []
	likes = []
	images = []
	sentiments = []
	users = []

	data = result.json()['data']

	for post in data:
		# Get post content
		caption = post['caption']['text']
		captions.append(caption)
		likes.append(post['likes']['count'])
		images.append(post['images']['thumbnail']['url'])
		str_time = float(post['caption']['created_time'])
		datetime = time.strftime('%H:%M:%S %m-%d-%y', time.localtime(str_time))
		times.append(datetime)
		
		# Get post sentiment from http://text-processing.com/docs/sentiment.html
		payload = { 'text': caption }
		sentiment = requests.post(sentiment_api, data=payload).json()
		print(sentiment)
		sentiments.append(sentiment['label'])

		# Get user info
		user_id = post['user']['id']
		user_result = requests.get(insta_api + 'users/' + user_id + '?client_id=' + client_id)
		user_data = user_result.json()['data']['counts']

		# Create user dict
		user = { 
			'username': post['user']['username'],
			'num_posts': user_data['media'],
			'num_follows': user_data['follows'],
			'num_followers': user_data['followed_by']
		}

		users.append(user)

	return { 'captions':captions, 'likes':likes, 'images':images, 'users':users, 'times':times, 'sentiments':sentiments }

import json, time, os, operator
import requests, urllib2
from bs4 import BeautifulSoup

def overall():
	api = "http://www.imleagues.com/School/Division/viewstanding.aspx?Division="
	json_sports = json.load(open('./keys/links.json'))
	scores = {
		"Morse":0,
		"Branford":0,
		"Ezra Stiles":0,
		"Timothy Dwight":0,
		"Berkeley":0,
		"Calhoun":0,
		"Silliman":0,
		"Jonathan Edwards":0,
		"Trumbull":0,
		"Saybrook":0,
		"Davenport":0,
		"Pierson":0
	}

	full_team_size = 0
	for sport in json_sports:
		# Determine full_team_size
		if sport == "c_football" or sport == "m_football":
			full_team_size = 6
		elif sport == "c_soccer" or sport == "m_soccer" or sport == "w_soccer":
			full_team_size = 11
		elif sport == "c_tabletennis" or sport == "tennis":
			full_team_size = 10
		elif sport == "volleyball":
			full_team_size = 6

		# Go to site
		link = api + json_sports[sport]
		web_page = urllib2.urlopen(link).read()
		soup = BeautifulSoup(web_page, "html.parser")

		# Add to college totals
		for i in range(12):
			team_id = "ctl00_ContentPlaceHolder1_gvTeams_ctl%02d_lblName" % (i + 2)
			college_name = soup.find(id=team_id).string
			
			# Wins and Ties
			points_id = "ctl00_ContentPlaceHolder1_gvTeams_ctl%02d_lblWLT" % (i + 2)
			wlt = soup.findAll(id=points_id)
			wins = float(wlt[0].string)
			ties = float(wlt[2].string)

			# Exception for women's soccer since each team has two colleges
			if sport == "w_soccer":
				college1 = ""
				college2 = ""
				if college_name == "BK-ES":
					college1 = "Berkeley"
					college2 = "Ezra Stiles"
				elif college_name == "PC-TC":
					college1 = "Pierson"
					college2 = "Trumbull"
				elif college_name == "MC-SY":
					college1 = "Morse"
					college2 = "Saybrook"
				if college_name == "TD-SM":
					college1 = "Timothy Dwight"
					college2 = "Silliman"
				elif college_name == "JE-BR":
					college1 = "Jonathan Edwards"
					college2 = "Branford"
				elif college_name == "DC-CC":
					college1 = "Davenport"
					college2 = "Calhoun"
				scores[college1] += (wins + ties*0.5)*full_team_size
				scores[college2] += (wins + ties*0.5)*full_team_size
			else:
				scores[college_name] += (wins + ties*0.5)*full_team_size

			# Exception for women's soccer since there are only 6 teams
			if sport == "w_soccer" and i == 5:
				break;

	# Sort colleges by rank, display in table
	sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
	return sorted_scores

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

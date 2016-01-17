import json, time, os, operator
import requests, urllib2

from .models import Sport

def overall():
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

	# Call kimono API
	results = json.load(urllib2.urlopen("https://www.kimonolabs.com/api/5qxqpxj8?apikey=7b965rHdqqFqdp0McyJ3qkUGAQUoHXGx"))
	json_scores = results["results"]["scores"]

	for i in range(90):
		# Add to college totals
		sport = json_scores[i]["api"]
		college_name = json_scores[i]["team"]
		wins = float(json_scores[i]["wins"])
		ties = float(json_scores[i]["ties"])

		# Determine full_team_size
		full_team_size = 0
		if sport == "c_football" or sport == "m_football":
			full_team_size = 6
		elif sport == "c_soccer" or sport == "m_soccer" or sport == "w_soccer":
			full_team_size = 11
		elif sport == "c_tabletennis" or sport == "c_tennis":
			full_team_size = 10
		elif sport == "c_volleyball":
			full_team_size = 6

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
			elif college_name == "TD-SM":
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

	# Add stored scores
	stored_sports = Sport.query.all()
	for add_sport in stored_sports:
		scores["Morse"] += add_sport.mc
		scores["Branford"] += add_sport.br
		scores["Ezra Stiles"] += add_sport.es
		scores["Timothy Dwight"] += add_sport.td
		scores["Berkeley"] += add_sport.bk
		scores["Calhoun"] += add_sport.cc
		scores["Silliman"] += add_sport.sm
		scores["Jonathan Edwards"] += add_sport.je
		scores["Trumbull"] += add_sport.tc
		scores["Saybrook"] += add_sport.sy
		scores["Davenport"] += add_sport.dc
		scores["Pierson"] += add_sport.pc

	# Sort colleges by rank, display in table
	sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
	return sorted_scores

def db_sport(sport):
	add_sport = Sport.query.filter_by(name=sport).first()
	scores = {
		"Morse":add_sport.mc,
		"Branford":add_sport.br,
		"Ezra Stiles":add_sport.es,
		"Timothy Dwight":add_sport.td,
		"Berkeley":add_sport.bk,
		"Calhoun":add_sport.cc,
		"Silliman":add_sport.sm,
		"Jonathan Edwards":add_sport.je,
		"Trumbull":add_sport.tc,
		"Saybrook":add_sport.sy,
		"Davenport":add_sport.dc,
		"Pierson":add_sport.pc
	}
	# Sort colleges by rank for display in table
	sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
	return sorted_scores

def sport(sport):
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

	kimono_ids = {
		"w_soccer": "4gfpvl6w",
		"c_football": "8excyibu",
		"c_tennis": "2q1qdvcy",
		"c_tabletennis": "dhat65ri",
		"m_football": "a6i2zx3i",
		"m_soccer": "c9bbtr10",
		"c_soccer": "csg6u8yq",
		"c_volleyball": "5d49y3kc"
	}

	# Call kimono API
	results = json.load(urllib2.urlopen("https://www.kimonolabs.com/api/" + kimono_ids[sport] + "?apikey=7b965rHdqqFqdp0McyJ3qkUGAQUoHXGx"))
	json_scores = results["results"]["scores"]

	for i in range(len(json_scores)):
		# Add to college totals
		college_name = json_scores[i]["team"]
		wins = float(json_scores[i]["wins"])
		ties = float(json_scores[i]["ties"])

		# Determine full_team_size
		full_team_size = 0
		if sport == "c_football" or sport == "m_football":
			full_team_size = 6
		elif sport == "c_soccer" or sport == "m_soccer" or sport == "w_soccer":
			full_team_size = 11
		elif sport == "c_tabletennis" or sport == "c_tennis":
			full_team_size = 10
		elif sport == "c_volleyball":
			full_team_size = 6

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
			elif college_name == "TD-SM":
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

	# Sort colleges by rank, display in table
	sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
	return sorted_scores

def getProjects():
	return {}

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

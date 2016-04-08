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
	# results = json.load(urllib2.urlopen("https://sizzling-fire-1620.firebaseio.com/results.json"))
	# json_scores = results["scores"]

	results = json.load(urllib2.urlopen("https://api.import.io/store/connector/635dd6b4-4385-46f7-9e3a-ae0642483b96/_query?input=webpage/url:http%3A%2F%2Frender.import.io%2F%3Furl%3Dhttps%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2F1Dh54hH2GNdkL3SZrUi6e26TKS8hXu1gO5qnnTwrl3Lo%2Fpubhtml&&_apikey=b5595078310a443994942424fd0d17d8b030dd586a8c4a37e155e7436f3f73b0a42c2a94fa76a60fcacb46246436d09c4d2ab8a6ebdaea5332d19c89b9a8a01f79ba88dfb3163def3d1b504c84dbde1f"))
	json_scores = results["results"]

	for i in range(len(json_scores)):
		# Add to college totals
		# Catch exceptions when import.io isn't consistent
		if not json_scores[i].has_key("team"):
			continue

		college_name = json_scores[i]["team"]

		# Filter out import.io thing
		if college_name == "team":
			continue

		sport = json_scores[i]["sport"] #api for firebase/kimono
		wins = float(json_scores[i]["wins"])
		ties = float(json_scores[i]["ties"])

		# Determine full_team_size
		full_team_size = 0
		if sport == "w_squash":
			full_team_size = 3
		elif sport == "c_bowling":
			full_team_size = 4
		elif sport == "a_hoops" or sport == "b_hoops" or sport == "c_hoops" or sport == "w_hoops":
			full_team_size = 5
		elif sport == "c_football" or sport == "m_football" or sport == "c_hockey" or sport == "w_volleyball" or sport == "c_waterpolo":
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

	# kimono_ids = {
	# 	"w_soccer": "4gfpvl6w",
	# 	"c_football": "8excyibu",
	# 	"c_tennis": "2q1qdvcy",
	# 	"c_tabletennis": "dhat65ri",
	# 	"m_football": "a6i2zx3i",
	# 	"m_soccer": "c9bbtr10",
	# 	"c_soccer": "csg6u8yq",
	# 	"c_volleyball": "5d49y3kc"
	# }

	# # Call kimono API
	# results = json.load(urllib2.urlopen("https://sizzling-fire-1620.firebaseio.com/kimono/api/" + kimono_ids[sport] + "/latest.json"))
	# json_scores = results["results"]["scores"]

	results = json.load(urllib2.urlopen("https://api.import.io/store/connector/635dd6b4-4385-46f7-9e3a-ae0642483b96/_query?input=webpage/url:http%3A%2F%2Frender.import.io%2F%3Furl%3Dhttps%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2F1Dh54hH2GNdkL3SZrUi6e26TKS8hXu1gO5qnnTwrl3Lo%2Fpubhtml&&_apikey=b5595078310a443994942424fd0d17d8b030dd586a8c4a37e155e7436f3f73b0a42c2a94fa76a60fcacb46246436d09c4d2ab8a6ebdaea5332d19c89b9a8a01f79ba88dfb3163def3d1b504c84dbde1f"))
	json_scores = results["results"]

	for i in range(len(json_scores)):
		# Filter out sports not currently being queried
		sport_name = json_scores[i]["sport"]
		if sport_name != sport:
			continue

		# Compesate for import.io slowness
		if not json_scores[i].has_key("team"):
			continue

		# Add to college totals
		college_name = json_scores[i]["team"]
		wins = float(json_scores[i]["wins"])
		ties = float(json_scores[i]["ties"])

		# Determine full_team_size
		full_team_size = 0
		if sport == "w_squash":
			full_team_size = 3
		elif sport == "c_bowling":
			full_team_size = 4
		elif sport == "a_hoops" or sport == "b_hoops" or sport == "c_hoops" or sport == "w_hoops":
			full_team_size = 5
		elif sport == "c_football" or sport == "m_football" or sport == "c_hockey" or sport == "w_volleyball" or sport == "c_waterpolo":
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

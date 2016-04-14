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
	results = json.load(urllib2.urlopen("https://sizzling-fire-1620.firebaseio.com/kimono/api/c01pdz04/latest.json"))
	json_scores = results["results"]["scores"]

	sport = ""
	for i in range(results["count"]):
		# Add to college totals
		if json_scores[i].has_key("sport"):
			sport = json_scores[i]["sport"]

		college_name = json_scores[i]["team"]
		wins = float(json_scores[i]["wins"])
		ties = float(json_scores[i]["ties"])

		# Determine full_team_size
		full_team_size = 0
		if sport == "Women's Squash":
			full_team_size = 3
		elif sport == "Coed Bowling":
			full_team_size = 4
		elif sport == "A Hoops" or sport == "B Hoops" or sport == "C Hoops" or sport == "W Hoops":
			full_team_size = 5
		elif sport == "Coed Football" or sport == "Men's Football" or sport == "Coed Ice Hockey" or sport == "Women's Winter" or sport == "Coed Waterpolo":
			full_team_size = 6
		elif sport == "Fall Coed Soccer" or sport == "Men's Soccer" or sport == "Women's Soccer":
			full_team_size = 11
		elif sport == "Coed Table Tennis" or sport == "Coed Tennis":
			full_team_size = 10
		elif sport == "Fall Outdoor":
			full_team_size = 6

		# Exception for women's soccer since each team has two colleges
		if sport == "Women's Soccer":
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

	# Call kimono API
	results = json.load(urllib2.urlopen("https://sizzling-fire-1620.firebaseio.com/kimono/api/c01pdz04/latest.json"))
	json_scores = results["results"]["scores"]

	for i in range(results["count"]):
		# Only add score for queried sport
		if json_scores[i].has_key("sport") and json_scores[i]["sport"] == sport:
			print "found it: " + json_scores[i]["sport"] 
			# Add scores until the next sport is found
			while i < results["count"] and ((json_scores[i].has_key("sport") and json_scores[i]["sport"] == sport) or not json_scores[i].has_key("sport")):
				# Add to college totals
				college_name = json_scores[i]["team"]
				wins = float(json_scores[i]["wins"])
				ties = float(json_scores[i]["ties"])

				# Determine full_team_size
				full_team_size = 0
				if sport == "Women's Squash":
					full_team_size = 3
				elif sport == "Coed Bowling":
					full_team_size = 4
				elif sport == "A Hoops" or sport == "B Hoops" or sport == "C Hoops" or sport == "W Hoops":
					full_team_size = 5
				elif sport == "Coed Football" or sport == "Men's Football" or sport == "Coed Ice Hockey" or sport == "Women's Winter" or sport == "Coed Waterpolo":
					full_team_size = 6
				elif sport == "Fall Coed Soccer" or sport == "Men's Soccer" or sport == "Women's Soccer":
					full_team_size = 11
				elif sport == "Coed Table Tennis" or sport == "Coed Tennis":
					full_team_size = 10
				elif sport == "Fall Outdoor":
					full_team_size = 6

				# Exception for women's soccer since each team has two colleges
				if sport == "Women's Soccer":
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

				i += 1

			# Exit loop
			break

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

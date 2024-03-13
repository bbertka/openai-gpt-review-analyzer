from textblob import TextBlob
from temporalio import activity
import redis, json, textwrap
import os
import logging

logger = logging.getLogger(__name__)

#For Docker/Kuberntes
#redis_host = os.getenv("REDIS_HOST")
#redis_port = int(os.getenv("REDIS_PORT"))
#redis_db = os.getenv("REDIS_DB")

#For testing
redis_host = "192.168.1.110"
redis_port = 6379
redis_db = "0"

@activity.defn
async def sentiment(text):
	""" Quick and Dirty Sentiment """
	activity.logger.info("Sentiment activity with parameter %s" % text)

	value = 'Neutral'
	sentiment = 0
	try:
		sentiment = TextBlob(text).sentiment.polarity
	except:
		pass
	if sentiment < 0:
		value = 'Bad'
	elif sentiment > 0:
		value = 'Good'
	return value

@activity.defn
async def star_rating(stars):
	activity.logger.info("Star-rating activity with parameter %s" % stars)
	rating = float(stars)

	if rating >= 4:
		return "Good"
	elif rating >= 2.5:
		return "Neutral"
	elif rating < 2.5:
		return "Bad"

@activity.defn
async def quantify(ratings):
	#weighted vector of ratings [stars, title, content]
	weights =[.40, .20, .40]
	wv = [0.0,0.0,0.0]
	scores = ['','','']
	for i in range(3):
		if ratings[i] == "Good":
			scores[i] = 100
		elif ratings[i] == "Neutral":
			scores[i] = 73
		elif ratings[i] == "Bad":
			scores[i] = 0
		wv[i] = scores[i]*weights[i]

	total= 0.0
	for i in range(3):
		total = total+wv[i]
	return total

@activity.defn
async def interprete(rating):
	activity.logger.info("Interprete activity with parameter %s" % rating)
	grade = "A"
	if rating >= 97:
		grade = "A+"
	elif rating >= 93:
		grade = "A"
	elif rating >= 90:
		grade = "A-"
	elif rating >= 87:
		grade = "B+"
	elif rating >= 83:
		grade = "B"
	elif rating >= 80:
		grade = "B-"
	elif rating >= 77:
		grade = "C+"
	elif rating >= 73:
		grade = "C"
	elif rating >= 70:
		grade = "C-"
	elif rating > 67:
		grade = "D+"
	elif rating > 63:
		grade = "D"
	elif rating > 60:
		grade = "D-"
	elif rating < 60:
		grade = "F"
	return grade

@activity.defn
async def analyze(itemkeys):
	activity.logger.info("Analyze activity with len(itemkeys) %d" % len(itemkeys))
	r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
	i = 1
	total = 0
	for key in itemkeys:
		retrieved_value_str = r.get(key)
		retrieved_data = json.loads(retrieved_value_str)
		rating = retrieved_data['star']
		title = retrieved_data['title']
		content = retrieved_data['content']
		logger.info("Item: %s, Review: %s, %s, %s" % (key, rating, title, textwrap.shorten(content, width=128)))
		stars =  await star_rating(rating)
		title =  await sentiment(title)
		content = await sentiment(content)
		ratings = [stars, title, content]
		rating = await quantify(ratings)
		verdict = await interprete(rating)
		logger.info("Item: %s, Computed weighted review vector: %s, as: %s" % (key, ratings, verdict) )
		total = total + rating
		i = i+1
	result = float(total/i)
	verdict = await interprete(result)
	return result, verdict

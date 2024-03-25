from textblob import TextBlob
from temporalio import activity
from temporalio.common import RetryPolicy
import redis, json, textwrap
import logging
from openai import OpenAI
from config import REDIS_HOST, REDIS_PORT, REDIS_DB, OPENAI_API_KEY

logger = logging.getLogger(__name__)

#client = OpenAI(api_key=OPENAI_API_KEY)

@activity.defn
async def sentimentOpenAI(review_text):
	"""
	Analyzes the sentiment of the given review text using OpenAI's GPT model.
	"""
	client = OpenAI(api_key=OPENAI_API_KEY)
	try:
		chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", "content": "You are a helpful assistant. You will provide only a one word reponse to the question.",
                    "role": "user", "content": f"What is the sentiment of this review? Please give me a one word response of either Good, Bad, or Neutral.\n\nReview:\n{review_text}",
                }
            ],
            model="gpt-3.5-turbo", #for cost savings
        )
		sentiment_result = chat_completion.choices[0].message.content.strip()
		return sentiment_result
	except Exception as e:
		print(f"Error analyzing sentiment: {e}")
		return None


@activity.defn
async def sentimentTextBlob(text):
	"""
	Analyzes the sentiment of the given review title using TextBlob.
	"""
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
	#activity.logger.info("Star-rating activity with parameter %s" % stars)
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
	#activity.logger.info("Interprete activity with parameter %s" % rating)
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
	#activity.logger.info("Analyze activity with len(itemkeys) %d" % len(itemkeys))
	r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
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
		title =  await sentimentTextBlob(title)
		content = await sentimentOpenAI(content)
		ratings = [stars, title, content]
		rating = await quantify(ratings)
		verdict = await interprete(rating)
		logger.info("Item: %s, Computed weighted review vector: %s, as: %s" % (key, ratings, verdict) )
		total = total + rating
		i = i+1
	result = float(total/i)
	verdict = await interprete(result)
	return result, verdict

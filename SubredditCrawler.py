import praw
from collections import defaultdict
from BagOfWordsDB import BagOfWordsDB

class SubredditCrawler():
	def __init__(self):
		my_client_id = ''
		my_secret_id = ''
		
		my_user_agent = 'Windows: SubredditCrawler (by FourBolt)'
		self.reddit =  praw.Reddit(client_id=my_client_id,
								   client_secret=my_secret_id,
								   user_agent=my_user_agent)
		self._read_exclusion_words()
		self._db = BagOfWordsDB()		

	def _read_exclusion_words(self):
		self._exclusions = defaultdict(int)
		with open('word_exclusions.txt') as f:
			for line in f:
				self._exclusions[line.strip('\n')] = 1
	
	def gen_bag_of_words(self, subreddit_name: str, num_posts=1000, max_words=100):
		''' This function returns a list with size equal to limit, of the most common words in 
			the subreddit, reading the number of posts = num_posts
		
			== Parameters:
				subreddit_name: name of subreddit to crawl
				num_posts: number of posts to read from subreddit
				limit: max number of words to return
			== Return value:
				list of size limit
				first terms in list have highest frequency
		
		'''
		d = defaultdict(int) 

		# For each submission to the subreddit with num_posts
		for submission in self.reddit.subreddit(subreddit_name).hot(limit=num_posts):
			for word in submission.title.split(" "):
				# If each word is not exlusion, then add one
				if self._exclusions[word.lower()] != 1:
					d[word.lower()] += 1
		d = sorted(d.items(), key = lambda x: x[1], reverse=True)

		if (max_words < len(d)):
			d = d[0:max_words]	

		result = []
		for i in range(len(d)):
			result.append(d[i][0])
		return result
		
	def save_bag_of_words(self, subreddit, word_list):
		self._db.insert_subreddit(subreddit, word_list)

	def get_bag_of_words(self, subreddit):
		return self._db.get_word_list(subreddit)

	def shutdown(self):
		self._db.shutdown()

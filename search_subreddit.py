from SubredditCrawler import SubredditCrawler
import time





def get_list_of_subreddits() -> list:
	result = []
	with open('subreddit_list.txt') as of:
		for line in of:
			result.append(line.strip('\n'))	
	return result


def scrape():
	#subreddit = input("Enter subreddit to search: ")
	subreddit_list = get_list_of_subreddits()

	crawler = SubredditCrawler()
	posts = 5000
	max_words = 300 
	print("Initialized crawler...")

	errorList = [201,212,264,488,1288,1463,1489]

	size = len(subreddit_list)
	for i in errorList:
		print("Crawling " + str(i+1) + "/" + str(size) + " : " + subreddit_list[i])
		print("Crawling subreddit with posts="+str(posts)+ ', max_words=' + str(max_words))
		try:
			results = crawler.gen_bag_of_words(subreddit_list[i], num_posts=posts, max_words=max_words)
			crawler.save_bag_of_words(subreddit_list[i],results)
		except:
			print('ERROR RAISED!')
			errorList.append((i,subreddit_list[i]))
		print("Sleeping...")
		time.sleep(1)
	print(errorList)
	with open('error_list.txt','w') as f:
		for e in errorList:
			f.write(e + '\n')
	

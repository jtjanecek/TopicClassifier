from BagOfWordsDB import BagOfWordsDB


class TopicClassifier():
	def __init__(self):
		self._db = BagOfWordsDB()

	def classifyBOW(self, text):
		text = text.lower()
		best = []
		words = text.split(" ")
		for row2 in self._db:
			row = (row2[0], eval(row2[1]))
			for word in words:
				for i in range(len(row[1])):
					if row[1][i] == word:
						best.append((row[0],i))
		best = sorted(best, key=lambda x: x[1])
		for i in range(min(10,len(best))):
			print("My #" + str(i+1) + " guess is: " + best[i][0])
		return


t = TopicClassifier()
while(True):
	x = input("$: ")
	t.classifyBOW(x)

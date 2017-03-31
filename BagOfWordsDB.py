import sqlite3

class BagOfWordsDB():
    def __init__(self):
        db_name = 'bag_of_words.db'
        self._db_conn = sqlite3.connect(db_name)
        self._db_cursor = self._db_conn.cursor()

        self._db_cursor.execute("CREATE TABLE IF NOT EXISTS states(subreddit TEXT primary key, word_list TEXT)")
        self._db_conn.commit()


    def __iter__(self):
        self._db_cursor.execute('SELECT * FROM states')
        for row in self._db_cursor:
            yield row
        return self

    def insert_subreddit(self, subreddit, word_list) -> None:
        word_list = str(word_list)
        try:
            self._db_cursor.execute("INSERT INTO states VALUES (?, ?)", (subreddit, word_list))
            self._db_conn.commit()
        except:
            self._db_cursor.execute("UPDATE states SET word_list = ? WHERE subreddit = ?", (subreddit, word_list))
            self._db_conn.commit()

    def get(self, subreddit) -> list:
        self._db_cursor.execute("SELECT * FROM states WHERE subreddit = ?", (subreddit,))
        results = self._db_cursor.fetchall()
        #print(results)
        if results == []:
            return []
        return eval(results[0][1])


    def shutdown(self):
        self._db_conn.commit()
        self._db_cursor.close()
        self._db_conn.close()

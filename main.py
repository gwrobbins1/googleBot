'''
File:main.py
Data:3 December 2017
Description:Entry point to the google search reddit bot
'''
import sys
import os
import threading

from time import sleep
from logger import Logger
from reddit_bot import RedditBot
from praw.exceptions import APIException

def load():
	try:
		return [line.rstrip('\n') for line in open('comment_id_log.log','r')]
	except:
		return []

def main():
	SUBREDDIT = "all"
	SEARCH_PHRASE = 'googleSearch!'
	COMMENT_LIMIT = None
	# COMMENT_LIMIT = 500000

	prev_comment_ids = load()

	logger = Logger()
	logger.setName('google bot logger')
	logger.start()

	bot = RedditBot(SEARCH_PHRASE,logger,prev_comment_ids)
	bot.login()

	thread_num = 0
	# while True:
	# crawler = bot.crawl_comments(thread_num,SUBREDDIT,COMMENT_LIMIT)

	# try:
	# 	crawler_thread = threading.Thread(target=crawler,name="bot_thread_"+str(thread_num))
	# 	crawler_thread.start()
	# except Exception as e:
	# 	if e == APIException:
	# 		print("[EXCEPTION] rate limit hit")
	# 		sleep(100)

	# sleep(30)

	while True:
		try:
			thread_num += 1
			crawler = bot.crawl_comments(thread_num,SUBREDDIT,COMMENT_LIMIT)
			crawler_thread = threading.Thread(target=crawler,name="bot_thread_"+str(thread_num))
			crawler_thread.start()
			crawler_thread.join()
		except Exception as e:
			if e == APIException:
				print("[EXCEPTION] rate limit hit")
				sleep(100)

	#make sure logger is finished commiting logs to file
	while not logger.is_finished():
		sleep(1)

	logger.stop_thread()
	return 0

if __name__ == '__main__':
	sys.exit(main())

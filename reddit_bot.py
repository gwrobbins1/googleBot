'''
File:reddit_bot.py
Data:3 December 2017
Description: Bot that performs breath first search of reddit comments.
			provide a target string to search for and a logger. Logger
			is a seperate thread used to keep track of comments already
			replied to by bot.
'''
import praw
import config
import re
from praw.models import MoreComments
from reply import ReplyFactory

class RedditBot:

	def __init__(self,target_string,logger,prev_ids):
		self.target = target_string
		self.logger = logger
		self.prev_ids = prev_ids
		self.reply_factory = ReplyFactory()

	def login(self):
		self.reddit = praw.Reddit(username = config.username,
				password = config.password,
				client_id = config.client_id,
				client_secret = config.client_secret,
				user_agent = "google search bot v0.1")

	def crawl_comments(self,thread_num,sub,limit):
		def crawler():
			print("[INFO] Started crawler "+str(thread_num))
			processed_cnt = self.process_comment(self.reddit.subreddit(sub).comments(limit=limit))
			print("[INFO] Exiting crawler "+str(thread_num)+"\nComment count:"+str(processed_cnt))
		return crawler

	def process_comment(self,comments,cnt=0):
		for comment in comments:
			cnt += 1
			# print("[INFO] processing comment "+str(comment.id))
			replies = comment.replies.list()
			if len(replies) > 0:
				self.process_comment(self,replies,cnt)

			if not comment:
				continue
			if isinstance(comment, MoreComments):
				self.process_comment(comment.comments(),cnt)
			if comment.id in self.prev_ids:
				continue
			if self.contains_target(comment.body):
				print("[INFO] found googleSearch in comment")
				self.logger.log(comment.id)
				self.prev_ids.append(comment.id)
				query = self.get_query(comment.body)
				print("[DEBUG] query: "+query)
				reply = self.reply_factory.make(query)
				comment.reply(reply)
		return cnt
	def contains_target(self,comment):
		return not re.search(self.target,comment) == None

	def get_query(self,comment):
		#get phrase after 'google this '
		i = comment.find(self.target)
		n = len(self.target)
		return comment[i+n+1:]#plus 1 for the space

'''
File: reply.py
Date: 4 December 2017
Description: Reply, ReplyFactory, and ReplyBuilder logic
'''

from string import Template
# from  google import google
import sys
import google

#template for links inside reddit comment
TEMPLATE_STR = "* [$description]($link) \n\n"

class ReplyBuilder:
	def __init__(self,template_string):
		self.template = Template(template_string)
		self.reply = ""

	def set(self,replyDict):
		self.reply += self.template.substitute(replyDict)

	def build(self):
		reply = self.reply
		self.reply = ""
		return reply

class ReplyFactory:
	def __init__(self):
		self.builder = ReplyBuilder(TEMPLATE_STR)

	def make(self,google_query):
		search_results = google.search(google_query,stop=5)
		if not search_results:
			return 'couldn\'t find any results. revise your search'

		reply_str = ""
		for result in search_results:
			reply_str += "* " + str(result) + '\n\n'

		print("[DEBUG] reply string: "+reply_str)
		return reply_str
		# for result in search_results:
		# 	# print("name: "+ result.name)
		# 	# print("description: "+ result.description)
		# 	# print("link: "+result.link)
		# 	# print("google link: "+result.google_link)
		# 	self.builder.set(dict(link=result.link,description=result.name))
		# return self.builder.build()

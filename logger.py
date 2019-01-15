'''
File:logger.py
Data:3 December 2017
Description: Logger thread queues messages that need to be appended to the file.
			The logger should be shared between all instances of the reddit bot
			threads. The purpose of this architecture is to offload the expensive
			file write operations to it's own thread so the reddit bots are free
			to craw comments.
'''
from threading import Thread
# from Queue import Queue
import queue
from time import sleep
import os
import threading

class Logger(Thread):
	def __init__(self):
		super(Logger,self).__init__()
		self.q = queue.Queue()
		self._stopper = threading.Event()

	def log(self,item):
		self.q.put(item)

	def commit_log(self,item):
		with open('comment_id_log.log','a+') as file:
			file.write(item+'\n')

	def run(self):
		while not self.is_stopped():
			if not self.q.empty():
				item = self.q.get()
				self.commit_log(item)
				self.q.task_done()
			sleep(1)

	def stop_thread(self):
		self._stopper.set()

	def is_stopped(self):
		return self._stopper.is_set()

	def is_finished(self):
		return self.q.empty()
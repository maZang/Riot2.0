import collections

class LRUCache:
	def __init__(self, capacity):
		self.capacity = capacity
		self.cache = collections.OrderedDict()

	def find(self, key):
		try: 
			result = self.cache.pop(key)
			self.cache[key] = result
			return result
		except KeyError: 
			return False

	def place(self, key, value):
		try:
			self.cache.pop(key)
		except KeyError:
			if len(self.cache) >= self.capacity:
				self.cache.popitem(last=False)
		self.cache[key] = value

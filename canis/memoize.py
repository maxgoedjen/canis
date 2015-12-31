from functools import wraps

def memoize(f):
	cached = {}
	@wraps(f)
	def wrapped(*arg):
		key = arg
		if cached.get(key):
			return cached[key]
		uncached = f(*arg)
		cached[key] = uncached
		return uncached
	return wrapped

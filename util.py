import os
def path_filter(path, text):
	dir_list = os.listdir(path)
	ports = filter(lambda x: text in x, dir_list)
	paths = map(lambda port : os.path.join(path, port), ports)
	return paths



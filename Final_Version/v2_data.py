import pandas as pd
import numpy as np
import re

class Data_handler(object):
	"""docstring for Data_handler"""
	def __init__(self, index_start, index_end):
		self.index_start = index_start
		self.index_end = index_end
		self.read = pd.read_csv('./v2_data.csv',header=None, skip_blank_lines=True, skipinitialspace=True)
	
	# the index of each furniture in the dataset
	def index_fur(self):
		store_index = []
		store_item = []
		index = []
		list_read = list(self.read[0])
		for item in enumerate(list_read):
			store_index.append(item[0])
			store_item.append(item[1])
		length = len(store_index)
		for i in range(length):
			if (i+1) < length:
				if store_item[i] != store_item[i+1]:
					index.append(store_index[i] + 1)
		index.append(store_index[-1]+1)
		index.insert(0, store_index[0])
		return index

	# read the assembly structure into the list
	def read_csv(self):
		first = []
		self.read = self.read.fillna(value='miss')
		# get first furniture
		for j in range(self.index_start, self.index_end):
			#width of assembly tree
			for i in range(1,57):
				if self.read[i][j] != 'miss':
					first.append(self.read[i][j])

		first.insert(0, "Item")
		first.insert(0, 1)
		return first

	# filter the information read
	def Re_expression(self):
		furniture = self.read_csv()
		furniture = str(furniture)
		y_ = re.sub(r"'Step \d+'|'Step \d\w'", r"Non-terminals", furniture)
		y_ = re.sub(r" |'|\[|\]|\.0", r"", y_)
		y_ = re.split(r",", y_)
		key = y_[0::2]
		value = y_[1::2]
		reform = []
		combine = zip(key, value)
		for line in combine:
			reform.append(line)
		return reform

	# generate the self-defined grammar
	# this is the version before the first version 
	# of grammar
	def Grammar_generator(self):
		data = self.Re_expression()
		get_all_NT = []
		get_all_T = []
		for item in enumerate(data):  
		   if item[1][1] == "Non-terminals" or item[1][1] == "Item":  
		       get_all_NT.append(item[0])
		   else:
		       get_all_T.append(item[0])

		c_f_g = []
		for i in range(1,len(get_all_NT)):
			c_f_g.append(data[get_all_NT[i-1]:get_all_NT[i]+1])
		c_f_g.append(data[get_all_NT[-1]::])

		return c_f_g


if __name__ == "__main__":
	pass


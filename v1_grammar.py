import v1_data as ud
import re
import pandas as pd

class Grammar_rules(object):
	"""docstring for Grammar_rules"""
	def __init__(self):
		self.all_grammar = []
		self.get_grammar = []
		self.final_grammar = []
		self.F_index = []
		self.index_F = 1
		self.index_NT = 1
		self.read = pd.read_csv('./v1_data.csv',header=None, skip_blank_lines=True, skipinitialspace=True)

	# index of furniture in the csv file
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

	# data handler
	def all_G(self):
		# the index for each furniture
		furniture_index = self.index_fur()
		for i in range(len(furniture_index)):
			if (i+1) < len(furniture_index):
				self.all_grammar.append(ud.Data_handler(furniture_index[i],furniture_index[i+1]).Grammar_generator())
			#print(furniture_index[i-1],",",furniture_index[i])
			else:
				break

		for a in range(len(self.all_grammar)):
			for b in range(len(self.all_grammar[a])):
				for c in range(len(self.all_grammar[a][b])):
					self.all_grammar[a][b][c] = list(self.all_grammar[a][b][c])
				self.get_grammar.append(self.all_grammar[a][b])
		
		for item in self.get_grammar:
			if item not in self.final_grammar:
				self.final_grammar.append(item)
		# for item in self.final_grammar:
		# 	print(item)

		return self.get_grammar

	# re-format rules that read from dataset
	def modify_grammar_rules(self):
		rules = self.all_G()
		# simplify rules, give each Furniture a different name
		for i in range(len(rules)):
			# change name for each furniture
			if rules[i][0][1] == "Item":
				rules[i][0][1] = 'F' + str(self.index_F)
				self.index_F += 1
			# for these grs 
			else:
				pass
		# change all NT's name
		for i in range(len(rules)):
			# follow each furniture, change relevant NT's name
			if rules[i][-1][1] == "Non-terminals" and rules[i][0][1] != "Non-terminals":
				rules[i][-1][1] = 'NT_' + rules[i][0][1] + '_' + str(self.index_NT)
				self.index_NT += 1
			# ['1', 'F2'], ['4', 'shelf'], ['1', 'NT_F2_10'], ['1', 'Non-terminals'], ['16', '113301'], ['1', 'Non-terminals']]
			else:
				if rules[i][0][1] != 'F12':
					rules[i][0][1] = rules[i-1][-1][1]
				#print(rules[i])
				if rules[i][-1][1] == "Non-terminals":
					rules[i][-1][1] = rules[i][0][1][0:-1] + str(int(rules[i][0][1][-1]) + 1)
			self.index_NT = 1
		read = pd.read_csv('./v1_BoMs.csv',usecols=['Ikea ID','Name'])
		read = read.fillna(value='miss')
		id_ = []
		name_ = []
		# read csv file, store id and name into different list
		rules[102][0] = ['1','F13']
		for index,row in read.iterrows():
			id_.append(row[0])
			name_.append(row[1])
		for j in range(len(id_)):
			for i in range(len(rules)):
				for x in range(len(rules[i])):
					if rules[i][x][1] == id_[j]:
						rules[i][x][1] = name_[j]
		for i in rules:
			for j in i:
				j[0] = int(j[0])
		
		return rules
		
if __name__ == "__main__":
	pass
	Grammar_rules().modify_grammar_rules()

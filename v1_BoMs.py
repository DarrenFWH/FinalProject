import v1_data as ud
import pandas as pd
import re

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
		self.fur_name = []
		self.list_read = None

	# index of furniture in the csv file
	def index_fur(self):
		store_index = []
		store_item = []
		index = []
		self.list_read = list(self.read[0])
		for item in enumerate(self.list_read):
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

	# get the name of each furniture
	def furniture_name(self):
		fur = self.index_fur()
		fur.remove(fur[-1])
		for i in fur:
			self.fur_name.append(self.list_read[i])
		return self.fur_name

	# data handler
	def all_G(self):
		furniture_index = self.index_fur()
		for i in range(len(furniture_index)):
			if (i+1) < len(furniture_index):
				self.all_grammar.append(ud.Data_handler(furniture_index[i],furniture_index[i+1]).Grammar_generator())
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
		return self.get_grammar

	# BoMs of all furnitures
	def parts_of_furniture(self,x):
		all_rules = self.change_rules()
		for item in enumerate(all_rules):
			if item[1][0][1][0:2] != "NT":
				self.F_index.append(item[0])

		for n in range(len(self.F_index)):
			# create list dynamically
			locals()['Furniture_'+str(n)] = []
			if (n+1) < len(self.F_index):
				for i in range(self.F_index[n],self.F_index[n+1]):
					for j in range(len(all_rules[i])):
						# furniture start
						if all_rules[i][j][1][0:2] != "NT":
							locals()['Furniture_' + str(n)].append(all_rules[i][j])
				# furniture finished
			else:
				for i in range(self.F_index[n],len(all_rules)):
					for j in range(len(all_rules[i])):
						if all_rules[i][j][1][0:2] != "NT":
							locals()['Furniture_' + str(n)].append(all_rules[i][j])
		# start analyse each furniture's parts, combine
		# all same parts with different number
		length = len(locals()['Furniture_' + str(x)])
		var = locals()['Furniture_' + str(x)]
		#print("the var is>",var)
		list_number = []
		list_name = []
		list_index = []
		ld_index = []

		# store index, name, and id separately
		for i in enumerate(var):
			list_name.append(i[1][1])
			list_number.append(i[1][0])
			list_index.append(i[0])
			ld_name = []
		# find duplicated parts
		for i in range(len(list_name)):
			if list_name.count(list_name[i]) > 1:
				ld_name.append(list_name[i])
		ld_name = list(set(ld_name))

		if len(ld_name) != 0:
			for i in range(len(ld_name)):
				num = 0
				for j in range(len(list_name)):
					if list_name[j] == ld_name[i]:
						num += int(list_number[j])
				item = self.number(num, var, str(ld_name[i]))
			var = item
			return var
		else:
			return var

	# number of parts in the bag
	def number(self, input_, bag, target_part):
		part = []
		for item in bag:
			if item[1] == target_part:
				item[0] = input_
		for line in bag:
			if line not in part:
				part.append(line)
		return part

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
		
		return rules

	# grammar generalization and simplification
	def change_rules(self):
			#----------------------------------------------------------------------------------------------------#
			read = pd.read_csv('./v1_BoMs.csv',usecols=['Ikea ID','Name'])
			read = read.fillna(value='miss')
			id_ = []
			name_ = []
			# read csv file, store id and name into different list
			for index,row in read.iterrows():
				id_.append(row[0])
				name_.append(row[1])
			rules = self.modify_grammar_rules()

			# missing F13 in the rule set
			rules[102][0] = ['1','F13']
			# replace all rule's id with name
			for j in range(len(id_)):
				for i in range(len(rules)):
					for x in range(len(rules[i])):
						if rules[i][x][1] == id_[j]:
							rules[i][x][1] = name_[j]
			name_ = list(set(name_))
		
			#----------------------------------------------------------------------------------------------------#
			# All rules ID replaced by name
			#----------------------------------------------------------------------------------------------------#
			# Start simplify all rules
			# 4 types of rules:
			# NT --> part
			# NT --> part, NT
			# F --> part, NT
			# F --> part
			NT_p = []
			NT_p_index = []

			NT_p_NT = []
			NT_p_NT_index = []

			F_p_NT = []
			F_p_NT_index = []

			F_p = []
			F_p_index = []

			tl = []
			
			# rules simplification
			length = len(rules)
			for i in range(length):
				# F --> part
				if rules[i][0][1][0] == "F" and rules[i][-1][1][0:2] != "NT":
					F_p.append(rules[i][1::])
					F_p_index.append(rules[i])
				# F --> part, NT
				elif rules[i][0][1][0] == "F" and rules[i][-1][1][0:2] == "NT":
					F_p_NT.append(rules[i][1:-1])
					F_p_NT_index.append(rules[i])
				# NT --> part, NT
				elif rules[i][0][1][0:2] == "NT" and rules[i][-1][1][0:2] == "NT":
					NT_p_NT.append(rules[i][1:-1])
					NT_p_NT_index.append(rules[i])
				# NT --> part
				elif rules[i][0][1][0:2] == "NT" and rules[i][-1][1][0:2] != "NT":
					NT_p.append(rules[i][1::])
					NT_p_index.append(rules[i])

			# change name for NT --> part, NT
			store_NT_p_NT = []
			for i in NT_p_NT:
				if self.match_item(i, NT_p_NT_index) not in store_NT_p_NT and self.match_item(i, NT_p_NT_index) != None:
					store_NT_p_NT.append(self.match_item(i, NT_p_NT_index))
			for item in store_NT_p_NT:
				# rules have NT_p_NT format, put into the list
				# start changing the name
				for line in range(len(item)):
					index = rules.index(item[line])
					# only change the head of the rule
					# change the head of rule
					rules[index][0][1] = str(rules[index][0][1][0:4]) + "_" + str(item[line][1][1])
					# change last rule's tail
					rules[index-1][-1][1] = str(rules[index][0][1][0:4]) + "_" + str(item[line][1][1])

			# chage name for F --> part, NT
			store_F_p_NT = []
			for i in F_p_NT:
				if self.match_item(i, F_p_NT_index) not in store_F_p_NT and self.match_item(i, F_p_NT_index) != None:
					store_F_p_NT.append(self.match_item(i, F_p_NT_index))

			for item in store_F_p_NT:
				for line in range(len(item)):
					index = rules.index(item[line])
					# change the head of rule
					rules[index][0][1] = str(rules[index][0][1][0]) + "_" + str(item[line][1][1])
					# change the tail of rule
					rules[index][-1][1] = str(rules[index][-1][1][0:4]) + "_" + str(item[line][1][1])
					# chenge next rule's head
					rules[index+1][0][1] = str(rules[index][-1][1][0:4]) + "_" + str(item[line][1][1])

			# number from str -> int
			for i in rules:
				for j in i:
					j[0] = int(j[0])
			leng = len(rules)

			# two rules apply same part
			# combine them
			index_rpR_3 = []
			index_rpR_4 = []
			for name in range(len(name_)):
				for i in range(len(rules)):
					x = 3
					if len(rules[i]) == x:
						if i+1 < len(rules):
							if rules[i][1][1] == rules[i+1][1][1] and rules[i][0][1] == rules[i+1][0][1]:
								if rules[i] not in index_rpR_3:
									index_rpR_3.append(rules[i])
									rules[i+1][1][0] = int(rules[i+1][1][0]) + int(rules[i][1][0])
					if len(rules[i]) == 4:
						if i+1 < len(rules):
							if rules[i][1][1] == rules[i+1][1][1] and rules[i][0][1] == rules[i+1][0][1]:
								if rules[i] not in index_rpR_4:
									index_rpR_4.append(rules[i])
									rules[i+1][1][0] = int(rules[i+1][1][0]) + int(rules[i][1][0])
									rules[i+1][2][0] = int(rules[i+1][2][0]) + int(rules[i][2][0])

			for r in index_rpR_3:
				rules.remove(r)
			for r in index_rpR_4:
				rules.remove(r)

			# for rules contain trunnion
			# rename the rule for better results
			for it in range(len(rules)):
				for itt in rules[it]:
					if itt[1] == "trunnion" and rules[it][0][1][5::] == "trunnion":
						rules[it-1][-1][1] = str(rules[it-1][-1][1]) + "_" + str(rules[it][1][0])
						rules[it][0][1] = str(rules[it][0][1]) + "_" + str(rules[it][1][0])

			return rules

	# store the last part in each furniture
	def last_part(self):
		rules = self.change_rules()
		last_part = []
		for i in rules:
			if "F" not in i[-1][1]:
				last_part.append(i[-1])
		return last_part

	# function handle rules has format
	# F --> part, NT 
	def match_item(self, part, rules):
		rule_list = []
		for i in range(len(rules)):
			if part == rules[i][1:-1]:
				rule_list.append(rules[i])
		# pick replicated rules:
		if len(rule_list) != 1:
			return rule_list


if __name__ == "__main__":
	pass
	Grammar_rules().change_rules()
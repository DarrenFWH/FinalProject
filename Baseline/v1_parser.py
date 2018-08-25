import v1_BoMs as gib
import v1_grammar as gi

class match_rules(object):
	def __init__(self):
		self.store_rules = []
		self.store_used_tree = []
		self.record = []
		self.i = 0
		self.x = 1
		self.rules_del = []
		self.last_part = gib.Grammar_rules().last_part()

	# S is a string, NT
	# bag contains multiple parts id or name
	def match(self, S, rules, bag, furniture_index):
		i = 0
		# for i in range(len(rules)):
		while i < len(rules):
			# match the head of each rule
			if S == rules[i][0] and rules[i] not in self.rules_del: # ["1","F1"] == ["1","F1"] 
				#print("<><>",rules[i])
				store_parts = []
				# copy bag
				bag_ = bag
				# number & name in store_parts
				sp_name = []
				sp_num = []
				# number & name in rules
				r_name = []
				r_num = []
				# number & name in bag_
				bag_part = []
				bag_num = []
				for item_in_each_rule in rules[i]: # ['1', 'F1'] ['4', 'shelf'] ['1', 'NT_F1_1']
					# parts in the bag
					for b in range(len(bag_)):
						# find part in both rules and bag_
						if item_in_each_rule[1] == bag_[b][1]:
							if item_in_each_rule not in store_parts:
								store_parts.append(item_in_each_rule) # store parts in bag into a list	
						else:
							continue

				# store number & name of store_parts separately
				for sp in store_parts:
					sp_num.append(sp[0])
					sp_name.append(sp[1])	

				for b in bag_:
					bag_part.append(b[1])
				
				# store number & name of rules separately
				for r in rules[i]:
					r_num.append(r[0])
					r_name.append(r[1])
				
				if len(bag_) != 0:
					# rule can be applied if all 
					# parts both in rule and bag
					if rules[i] not in self.rules_del:
						if len(self.store_rules) != 0:
							if rules[i][0] == self.store_rules[-1][-1]:
								# for all rules have structure: NT --> part, NT
								if sp_name == r_name[1:-1]:
									self.handle_bag(bag_, store_parts, sp_num, bag_part, sp_name, rules, rules[i-1])
								if rules[i] not in self.store_rules:
									self.store_rules.append(rules[i])
								S = rules[i][-1]
								rules.remove(rules[i])
								self.match(S, rules, bag_, furniture_index)
						else:
							if sp_name == r_name[1:-1]:
								self.handle_bag(bag_, store_parts, sp_num, bag_part, sp_name, rules, rules[i-1])
							if rules[i] not in self.store_rules:
								self.store_rules.append(rules[i])
							S = rules[i][-1]
							rules.remove(rules[i])
							self.match(S, rules, bag_, furniture_index)
					else:
						pass

				# for all rules have structure: NT --> part
				if sp_name == r_name[1::]:
					self.handle_bag(bag_, store_parts, sp_num, bag_part, sp_name, rules, rules[i-1])

				# for the first version of grammar
				# all parts will be consumed after 
				# one time iteration
				if len(bag_) == 0:
					self.assembly_tree(self.store_rules,furniture_index)
					exit()
			i+=1

	# deal with parts in bag
	def handle_bag(self, bag_, store_parts, sp_num, bag_part, sp_name, rules_i, rules_i_1):
		for bp in bag_:
			#if bp[1] not in bag_part:
			bag_part.append(bp[1])

		bag_index = []
		for item_sp in range(len(store_parts)):
			if store_parts[item_sp][1] in bag_part:
				bag_index.append(bag_part.index(store_parts[item_sp][1]))

			for bi in bag_index:
				# part still in the bag
				if bag_[bi][0] != 0:
					if bag_[bi][0] - sp_num[item_sp] >= 0:
						bag_[bi][0] -= sp_num[item_sp]
						# after subtract number of part from the 
						# first matched part, remove the index
						bag_index.remove(bag_index[0])
					else:
						continue

				# delete the part if all be consumed
				if bag_[bi][0] == 0:
					bag_part.remove(bag_part[bi])
					bag_.remove(bag_[bi])
				else: 
					pass

			for bi_ in bag_:
				if bi_[0] == 0:
					bag_.remove(bi_)
					bag_part.remove(bi_[1])

		if len(bag_) != 0:
			if bag_[0][0] == 0:
				bag_.remove(bag_[0])
				bag_part.remove(bag_part[0])
			else:
				pass
		return bag_

	# print the results one by one
	def assembly_tree(self, RulesTree, furniture_index):
		tree = []
		#for item in self.store_rules:
		lenth = len(RulesTree)
		for i in range(lenth):
			if i < lenth-1:
				if RulesTree[i][-1] == RulesTree[i+1][0]:
					# form the tree
					if RulesTree[i][0][1][0] == "F":
						tree.append(RulesTree[i][0])
						tree.append(RulesTree[i][1:-1])
					else:
						tree.append(RulesTree[i][1:-1])
			else:
				tree.append(RulesTree[i][1::])

		fur_name = gib.Grammar_rules().furniture_name()
		print("The furniture is:",fur_name[furniture_index])
		print("-"*50) # tree[i]
		for i in range(1,len(tree)):
			print("Step",len(tree)-i,":", tree[i])
		print("-"*50)
		if furniture_index == 11:
			print("Step 1:",tree[0])
		exit()

if __name__ == "__main__":
	#pass
	get_input = input("Please choose an index of BoMs from 0-21:")
	get_input = int(get_input)
	if get_input < 0 or get_input > 20:
		print("Error, please run the program again.")
	else:
		furniture_index = get_input
	#furniture_index = 20
	all_rules = gi.Grammar_rules().modify_grammar_rules()
	part = gib.Grammar_rules().parts_of_furniture(furniture_index)
	S = [1, 'F'+str(furniture_index+1)]
	part.remove(part[0])
	bag = part
	bag_copy = part
	print("The BoMs are:\n",part, S)
	print("-"*50)
	match_rules().match(S, all_rules, bag, furniture_index)
	exit()



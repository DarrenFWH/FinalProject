# 最终版的代码 为了扩展可能性 所以对bag的数量没有精确的控制
# 因为design space中数量并不是决定性的 使用什么part才是最重要的
import v2_grammar as gib
import copy
import random as rd

class match_rules(object):
	def __init__(self):
		self.store_rules = []
		self.store_used_tree = []
		self.i = 0
		self.x = 1
		self.rules_del = []
		self.last_part = gib.Grammar_rules().last_part()

	# S is a string, NT
	# bag contains multiple parts id or name
	def match(self, S, rules, bag, furniture_index):
		i = 0
		while i < len(rules):
			# match the head of each rule
			if S == rules[i][0] and rules[i] not in self.rules_del : # ["1","F1"] == ["1","F1"] 
				# print("<><>",rules[i])
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
				
				# for all rules have structure: NT --> part, NT
				if sp_name == r_name[1:-1]:
					self.handle_bag(bag_, store_parts, sp_num, bag_part)
				# store number & name of rules separately
				for r in rules[i]:
					r_num.append(r[0])
					r_name.append(r[1])

				# judge the parts in rule
				def bag_judger():
					Rname = r_name[1:-1]
					Rnum = r_num[1:-1]
					for p in bag_:
						for r in range(len(Rname)):
							if Rname[r] == p[1]:
								x = p[0]-Rnum[r] 
								if x < 0:
									self.rules_del.append(rules[i])
									continue
				if len(bag_) != 0:
					# rule can be applied if all 
					# parts both in rule and bag
					if rules[i] not in self.rules_del:
						if len(self.store_rules) != 0:
							if set(r_name[1:-1]).issubset(set(bag_part)):
								if rules[i][0] == self.store_rules[-1][-1]:
									bag_judger()
									self.store_rules.append(rules[i])
									S = rules[i][-1]
									rules.remove(rules[i])
									self.match(S, rules, bag_, furniture_index)
							# put unsatisfied rule into list
							else:
								self.rules_del.append(rules[i])
								rules.remove(rules[i])
								continue
						# first rule 
						else:
							if sp_name == r_name[1:-1]:
								self.handle_bag(bag_, store_parts, sp_num, bag_part)
							if rules[i] not in self.store_rules:
								self.store_rules.append(rules[i])
							# print("applu rule1:",rules[i])
							S = rules[i][-1]
							rules.remove(rules[i])
							self.match(S, rules, bag_, furniture_index)
					else:
						pass

				if sp_name == r_name[1::]:
					self.handle_bag(bag_, store_parts, sp_num, bag_part)

				#print(bag_, len(bag_))
				if len(bag_) == 0:
					self.assembly_tree(self.store_rules)
					exit()
				# the tree is not consume all parts, but still
				# right, more possibility can be found
				else:
					# add the last rule in the tree to the list
					print("---"*10)
					if self.store_rules[-1] != self.store_rules[0]:
						if self.store_rules[-1] not in self.rules_del:
							self.rules_del.append(self.store_rules[-1])
					#re-import the gramamr
					rules = gib.Grammar_rules().change_rules()
					#rules.reverse()
					#rd.shuffle(rules)
					temp_store = []
					# copy the parse tree every time
					temp = copy.copy(self.store_rules)
					# store the parse tree properly
					if temp not in self.store_used_tree:
						if temp[-1][-1] in self.last_part:
							self.store_used_tree.append(temp)
					# re-import the bag
					bag_ = gib.Grammar_rules().parts_of_furniture(furniture_index)
					bag_.remove(bag_[0])

					self.store_rules.clear()
					# initial S again, for the next iteration
					S = temp[self.i][-1]
					self.store_rules.append(temp[0])
					# always delete the parts in the first rule
					def bag_del_first():
						part = []
						for i in self.store_rules[0][1:-1]:
							part.append(i)
						for b in bag_:
							for p in part:
								if p[1] == b[1]:
									b[0] -= p[0]
					bag_del_first()

					print("... The %dth iteration, please wait"%(self.x))
					self.x+=1
					self.match(S, rules, bag_, furniture_index)
					#----------------------------------------------------------------------------------------------------#
					return self.output(self.store_used_tree)
			i+=1
	
	# prepare to print all results
	def output(self, all_r):
		print("the output:")
		for ar in all_r:
			self.assembly_tree(ar)
		exit()

	# deal with parts in bag
	def handle_bag(self, bag_, store_parts, sp_num, bag_part):
		for bp in bag_:
			bag_part.append(bp[1])

		bag_index = []
		for item_sp in range(len(store_parts)):
			if store_parts[item_sp][1] in bag_part:
				bag_index.append(bag_part.index(store_parts[item_sp][1]))

			for bi in bag_index:
				# parts still in bag
				if bag_[bi][0] != 0:
					if bag_[bi][0] - sp_num[item_sp] >= 0:
						bag_[bi][0] -= sp_num[item_sp]
						# after subtract number of part from the 
						# first matched part, remove the index
						bag_index.remove(bag_index[0])
					else:
						continue
				# delete part if 0 of part remain in the bag
				if bag_[bi][0] == 0:
					bag_part.remove(bag_part[bi])
					bag_.remove(bag_[bi])
				else: 
					pass
			# delete part if 0 of part remain in the bag
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
	def assembly_tree(self, RulesTree):
		tree = []
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

		#for item in tree:
		print("-"*50)
		fur_name = gib.Grammar_rules().furniture_name()
		print("The furniture is:",fur_name[furniture_index])
		print("-"*50)
		for i in range(1,len(tree)):
			print("Step",len(tree)-i,":", tree[i])
		if furniture_index == 11:
			print("Step 1:",tree[0])
		print("-"*50)
		return

if __name__ == "__main__":
	furniture_index = 0
	all_rules = gib.Grammar_rules().change_rules()
	#all_rules.reverse()
	#rd.shuffle(all_rules)
	part = gib.Grammar_rules().parts_of_furniture(furniture_index)
	S = part[0]
	part.remove(part[0])
	bag = part
	bag_copy = part
	print("The BoMs are:\n",part)
	match_rules().match(S, all_rules, bag, furniture_index)



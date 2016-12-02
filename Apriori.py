#!/usr/bin/python
# -*- coding: utf-8 -*-
from pprint import pprint



#Global Vars
DIR = './'
out_put_file_str = 'output.txt'

DEBUG = False

def write_output(msg):
	with open(DIR + out_put_file_str, 'a') as f:
		f.write(msg)


def generate_L1(transactions,ts):
	L1_cnt = dict()
	min = ts*len(transactions)
	for trans in transactions:
		for item in trans:
			if (item,) in L1_cnt:
				L1_cnt[(item,)] += 1
				# print(type( (item,) ))
			else:
				L1_cnt[(item,)] = 1
	L1_list = []
	for item in L1_cnt:
		if L1_cnt[item]>= min:
			L1_list.append(item)
	# print('***')
	# print(L1_list)
	L1_list = sorted(L1_list) # sorted by the item name.
	return L1_list, L1_cnt # not that un qualified items are not deleted yet. 

def generate_Lk(transactions, Lk_1_map, Lk_1_list,ts):
	if DEBUG:
		print('')
	cand = set()
	min = ts*len(transactions)

	# Lk should be sorted by from inside to out side by the item name
	for i in range(len(Lk_1_list)):
		if len(Lk_1_list[i]) <= 0:
			raise Exception()
		elif len(Lk_1_list[i]) == 1:
			for j in range(i+1,len(Lk_1_list)):
				cand.add((Lk_1_list[i][0],Lk_1_list[j][0]))
		else:
			for j in range(i+1,len(Lk_1_list)):
				if Lk_1_list[i][-2] == Lk_1_list[j][-2]:
					t_list = list(Lk_1_list[i])
					t_list.append(Lk_1_list[j][-1])
					cand.add(tuple(t_list))
				else:
					break
	if DEBUG:
		print('Test: candidate set: ')
		print(cand)
	if len(cand) == 0:
		if DEBUG:
			print('Test: set is empty time to return')
		return [],[]
	# prune
	to_remove = []
	for itemset in cand:
		#if DEBUG:
		# 	print('Test: itemset')
		# 	print(itemset)
		for item in itemset:
			t_list = list(itemset)
			t_list.remove(item)
			t_list = tuple(t_list)
			# if DEBUG:
			# 	print('Test: t_list')
			# 	print(t_list)
			if t_list not in Lk_1_map:
				to_remove.append(itemset)
				break
	for itemset in to_remove:
		cand.remove(itemset)
	if DEBUG:
		print('Test: candidate set after prune, time to return')
		print(cand)
	# finished prune

	if len(cand) == 0:
		if DEBUG:
			print('Test: set became empty after prune')
		return [],[]
	Lk_dict = dict()
	for trans in transactions:
		for itemset in cand:
			qualified = True
			for item in itemset:
				if item not in trans:
					# if DEBUG:
					# 	print(str(item)+" not in "+str(trans))
					qualified = False
					break
			if qualified:
				if itemset in Lk_dict:
					Lk_dict[itemset] += 1
				else:
					Lk_dict[itemset] = 1
	Lk_list = []
	for item in Lk_dict:
		if Lk_dict[item]>= min:
			Lk_list.append(item)
	Lk_list = sorted(Lk_list) # sorted by the item name.
	
	if DEBUG:
		print("After support elimination: ")
		print("Test: ")
		print(Lk_dict)
		print(Lk_list)
	# return Lk_list, Lk_dict#
	Lk__1_list, Lk__1_dict = generate_Lk(transactions, Lk_dict, Lk_list,ts)

	# return a list of lk list and a list of lk dictionaries
	Lk__1_list.insert(0, Lk_list)
	Lk__1_dict.insert(0,Lk_dict)
	 # a list of Lk
	return Lk__1_list, Lk__1_dict


def eliminate_by_confidence(transactions, itemset_lists, tc):
	# compute the confidence first
	conf_dict=dict()
	for itemset_list in itemset_lists:
		if len(itemset_list) == 0 or len(itemset_list[0]) == 1:
			continue
		for itemset in itemset_list:
			for RHS_item in itemset:
				LHS_cnt = 0
				RHS_cnt = 0
				# remove this item
				LHS = list(itemset)
				LHS.remove(RHS_item)
				for trans in transactions:
					trans_set = set(trans)
					if trans_set >= set(LHS):# if the transaction contains the LHS
						LHS_cnt += 1
						if RHS_item in trans_set:
							RHS_cnt += 1
				conf_dict[(tuple(LHS),RHS_item)] = float(RHS_cnt)/LHS_cnt
	rule_list = []
	for rule in conf_dict: # rule is (tuple(LHS),RHS_item)
		if conf_dict[rule] >= tc:
			rule_list.append(rule)
	return rule_list,conf_dict

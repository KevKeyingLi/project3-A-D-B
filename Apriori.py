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

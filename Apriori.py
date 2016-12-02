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

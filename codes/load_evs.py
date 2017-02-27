# coding: utf-8 
import numpy as np
import matplotlib.pyplot as plt
from compiler.ast import flatten #doesnt work with python 3<
import copy
import random
import math
import csv
import time
import string
import re

class EVs:

	def __init__(self,arrival,departure,consumption,marginal_values):
		self.arrival=arrival
		self.departure=departure
		self.consumption=consumption
		self.marginal_values=marginal_values



decode_time=[12,13,14,15,16,17,18,19,20,21,22,23,0,1,2,3,4,5,6,7,8,9,10,11]

with open('beta_ev_dataset.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile,quoting=csv.QUOTE_MINIMAL)
	my_list=[]
	for row in spamreader:
		my_list.append(row)
			
csvfile.close()
		


#print my_list[0]

full_EVlist=[]
for i in range(0,len(my_list),2):
	values=[]
	for j in range(len(my_list[i+1])):
		values.append(float(my_list[i+1][j]))
	full_EVlist.append(EVs(decode_time[int(float(my_list[i][0]))],decode_time[int(float(my_list[i][1]))],int(my_list[i][2]),values))


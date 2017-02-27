# coding: utf-8 
import numpy as np
import matplotlib.pyplot as plt
from compiler.ast import flatten #doesnt work with python 3=<
import copy
import random
import math
import time


class EVs:

	def __init__(self):
		self.arrival=self.get_arrival()
		self.departure=self.get_departure()
		self.consumption=self.get_consumption()
		self.marginal_values=self.get_marginal_values()
		
	def get_arrival(self):
		self.arrival = np.random.randint(24) #default value = 23
		return self.arrival
		
	def get_departure(self):
		self.departure = np.random.randint(self.arrival,24) #default value = 23
		return self.departure
	
	def get_consumption(self):
		self.consumption = np.random.randint(1,6) #default value = 6
		return self.consumption

	def get_marginal_values(self):
		marg_rand=np.random.randint(1,7) #interval {1,2,3,....20}
		va1=np.random.exponential(scale=1.0)
		r_cons = np.random.uniform(0,va1,size=marg_rand-1)
		self.marginal_values=sorted(np.append(r_cons,va1),reverse = True)
		return self.marginal_values

	def print_EVs(self):
		print vars(self)


#EVlist, denotes an agents type Θ (theta) according to literature
#Supply-----> S
#Endowment-----> k


#genereta N EVs
def generate(N):
	
	EVlist = []
	
	#synthetic setup vehicle setting 
	for i in range(N):
		EVlist.append(EVs())
	
	#D.Parkes paper p.189 example vehicle setting, for experimentation and error correction
	
	#evs1=EVs()
	#evs1.arrival=1
	#evs1.departure=3
	#evs1.consumption=1
	#evs1.marginal_values=[10,4,2]

	#EVlist.append(evs1)
	#evs2=EVs()
	#evs2.arrival=1
	#evs2.departure=3
	#evs2.consumption=1
	#evs2.marginal_values=[9,3,1]

	#EVlist.append(evs2)
	#evs3=EVs()
	#evs3.arrival=1
	#evs3.departure=3
	#evs3.consumption=2
	#evs3.marginal_values=[8,6,5]
	#EVlist.append(evs3)
	
	return EVlist

#Greedy Allocation Algorithm
def greedy_allocation(EVlist,S,endowment,t):
	#creates a multiset of reported active marginal values for active agents
	V=[]
	for ev in range(len(EVlist)):
			if(EVlist[ev].arrival<=t and EVlist[ev].departure>=t):
				if (S>=EVlist[ev].consumption):
					query_cons=EVlist[ev].consumption
				else:
					query_cons=S
				V.append(EVlist[ev].marginal_values[:query_cons])
	#then updates an agents endowment
	V_help=sorted(list(flatten(V)),reverse=True) #make list of lists, flat array
	for s in range(S):	#for every unit of electricity
		if V_help:
			max_v=max(list(flatten(V_help)))	#finds max from flat array
			for ev in range(len(EVlist)):
				if max_v in EVlist[ev].marginal_values:
					#add endowment
					endowment[ev]+=1
					#remove values from agent
					V_help.pop(0) #in case of s>1
					EVlist[ev].marginal_values.pop(0)
	#return endowment as journal guides	
	if empty(V):
		V.append([0])
	return (endowment,flatten(V))						
	
	
	
def add_zeros(S,V):

	if(S>len(V)):
		V = (V + [0] * S)[:S]
	return V

def externality(V_zero,S,r): 
	max_Vs = sorted(V_zero,reverse=True)[:S]
	min_Vr = sorted(max_Vs)[:r]
	return min_Vr
		
def marginal_payments(externality,payment_vector):
	payment_vector.append(externality)
	return sorted(list(flatten(payment_vector)),reverse=True)
			
def empty(seq):
	try:
		return all(map(empty, seq))
	except TypeError:
		return False
		
def run_market_without_i(temp_EVlist,S,agent,temp_k,t,payment_vector):
	current_price=0
	copy_EVlist=copy.deepcopy(temp_EVlist)
	
	if copy_EVlist:
		r=copy_EVlist[agent].consumption
		copy_EVlist.pop(agent)
	else:
		return current_price

	for time in range(temp_EVlist[agent].arrival,t+1):
		run_variable=greedy_allocation(copy_EVlist,S,temp_k,time)[1]

	run_variable=add_zeros(S,run_variable)
	run_varibale=externality(run_variable,S,r)
	current_price=marginal_payments(run_varibale,payment_vector)
	current_price=map(lambda x: 0 if x<0 else x, current_price)
	return current_price
	
	
#On-Departure Cancellation(OD)
def on_departure_cancellation(EVlist,S):
	start_time = time.clock()
	#k initialization
	k=np.zeros(len(EVlist))
	k=[0] * len(EVlist)
	count_cancel=0;
	#a couple of evlist copies for flexibility
	temp_EVlist=copy.deepcopy(EVlist) #create a new list in order to run the market without i agent
	temp1_EVlist=copy.deepcopy(EVlist) #create a new list in order to keep(save) initial EV list 
	
	#k variables for flexibility
	temp_k=copy.deepcopy(k)
	temp1_k=copy.deepcopy(k)  #greedy allocation
	k_next=[]
	
	#payment variables
	payment_vector=[]
	agent_payment=np.empty((len(EVlist), 0)).tolist() #list of lists with each agents payment vector
	final_agent_payment=np.empty((len(EVlist), 0)).tolist() #list of lists with each agents payment vector
	final_x_payment=[0] * len(EVlist)
	
	for t in range(0,24):

		#run greedy allocation
		k_next.append(greedy_allocation(temp1_EVlist,S[t],temp1_k,t)[0][:])
		for agent in range(len(EVlist)):
			if(EVlist[agent].arrival<=t and EVlist[agent].departure>=t):

				temp_EVlist=copy.deepcopy(EVlist)
				for ev in range(len(temp_EVlist)):
					if ev != agent:
						l=len(temp_EVlist[ev].marginal_values)	
						temp_EVlist[ev].marginal_values=temp_EVlist[ev].marginal_values[k_next[t-1][ev]:l]	
				#run market without agent i
				i_payment = run_market_without_i(temp_EVlist,S[t],agent,temp_k,t,payment_vector) #but...we remove him afterwords
				agent_payment[agent].append(i_payment)

				#if agent is departing
				if EVlist[agent].departure==t:
					
					k[agent]=k_next[t][agent]
					final_agent_payment[agent]=sorted(flatten(agent_payment[agent])) #fix sorting

					#print "#2 agent: ",agent," marginal_values = ", EVlist[agent].marginal_values
					if EVlist[agent].marginal_values and k[agent]!=0:

						while EVlist[agent].marginal_values[(k[agent]-1)]<final_agent_payment[agent][(k[agent]-1)]:

							#cancel units when necessary
							#k(endowment) below zero is not acceptable
							if k[agent]==0:
								break
							else: 
								print "cancellation"
								count_cancel+=1
								k[agent]-=1
						

						#final payment for agent i. agent is charged according to his endowment
						final_x_payment[agent]=sum(final_agent_payment[agent][:k[agent]])

				payment_vector=[]

	return (k , count_cancel)
	
#Immediate Cancellation(ID)
def immediate_cancellation(EVlist,S):
	start_time = time.clock()
	k=np.zeros(len(EVlist))
	k=[0] * len(EVlist)
	count_cancel=0;
	#a couple of evlist copies for flexibility
	temp_EVlist=copy.deepcopy(EVlist) 
	temp1_EVlist=copy.deepcopy(EVlist) 
	
	#k variables for flexibility
	temp_k=copy.deepcopy(k)
	temp1_k=copy.deepcopy(k)  #greedy allocation
	k_next=[]
	
	#payment variables
	payment_vector=[]
	agent_payment=np.empty((len(EVlist), 0)).tolist() 
	final_agent_payment=np.empty((len(EVlist), 0)).tolist() 
	final_x_payment=[0] * len(EVlist)
	
	for t in range(0,24):
		#run greedy allocation

		k_next.append(greedy_allocation(temp1_EVlist,S[t],temp1_k,t)[0][:])
		for agent in range(len(EVlist)):

			if(EVlist[agent].arrival<=t and EVlist[agent].departure>=t):

				temp_EVlist=copy.deepcopy(EVlist)

				for ev in range(len(temp_EVlist)):
					if ev != agent:
						l=len(temp_EVlist[ev].marginal_values)
						temp_EVlist[ev].marginal_values=temp_EVlist[ev].marginal_values[k_next[t-1][ev]:l]	
			
				temp_k=copy.deepcopy(k_next[t-1])

				i_payment = run_market_without_i(temp_EVlist,S[t],agent,temp_k,t,payment_vector) #we remove him afterwords	
	
				agent_payment[agent].append(i_payment)
				final_agent_payment[agent]=sorted(flatten(agent_payment[agent])) #fix sorting
				if EVlist[agent].marginal_values and k_next[t][agent]!=0:
					
					while EVlist[agent].marginal_values[k_next[t][agent]-1]<final_agent_payment[agent][k_next[t][agent]-1]:

						'''cancel units when necessary
						k(endowment) below zero is not acceptable'''
						if k_next[t][agent]==0:
							break
						else:
							print " cancelation"
							k_next[t][agent]-=1
							count_cancel+=1;
							#update reseted quantities
							temp1_k[agent]=copy.deepcopy(k_next[t][agent])
							temp1_EVlist[agent].marginal_values=EVlist[agent].marginal_values[k_next[t][agent]:]			
							#temp1_EVlist=copy.deepcopy(EVlist)	
	
				if EVlist[agent].departure==t:
					
					#final payment for agent i. agent is charged according to his endowment
					k[agent]=k_next[t][agent]
					final_x_payment[agent]=sum(final_agent_payment[agent][:k[agent]])
				payment_vector=[]
				
	return (k , count_cancel)

results=[]
count=[]
for run in range(100):
	EVlist=generate(200)
	thefile = open('EVlist.txt', 'w')
	thefile1 = open('ΙΜ_cancels.txt', 'w')
	for temp_ev in range(len(EVlist)):
		thefile.write("Agent %d\n" %temp_ev)
		thefile.write("\n")
		thefile.write("Arrival : %s\n" % EVlist[temp_ev].arrival)
		thefile.write("Departure : %s\n" % EVlist[temp_ev].departure)
		thefile.write("Consumption : %s\n" % EVlist[temp_ev].consumption)
		thefile.write("Marginal Values : %s\n" % EVlist[temp_ev].marginal_values)
		thefile.write("\n")
		thefile.write("********************************************************\n")


	S=[20]*24

	run=on_departure_cancellation(EVlist,S)
	#run=immediate_cancellation(EVlist,S)
	results.append(float(sum(run[0])*100/sum(S)))
	print run[0]
	count.append(run[1])
	print results
print "burn vector",count

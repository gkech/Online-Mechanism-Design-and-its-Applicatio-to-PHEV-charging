import matplotlib.pyplot as plt

'''
Supply Initialization Module....for flexible resetting!
Each electricity unit equals to 3KWh for PHEV charging. We simulate a small neighbourhood of 30 households (weekday in high summer)
In our experiments, we vary supply (high and low).
High_supply = 615Kwh available for charging. 
Low_supply = 99Kwh available for charging. 
In both cases, a subset of supply is allocated to each hour with respect to the maximum supply (High or Low)
'''

decode_time=[12,13,14,15,16,17,18,19,20,21,22,23,0,1,2,3,4,5,6,7,8,9,10,11]
time=range(0, 24)
high_supply=[10,10,11,12,12,12,12,11,9,8,8,8,8,8,8,9,9,8,6,6,6,7,5,5]
high_supply_adjustment=[8,8,8,9,9,8,6,6,6,7,5,5,10,10,11,12,12,12,12,11,9,8,8,8]
low_supply=	[2,2,4,4,4,4,4,4,2,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,]
low_supply_adjustment=[1,1,1,1,1,0,0,0,0,0,0,0,2,2,4,4,4,4,4,4,2,0,0,0]
#for i in range(24):
	#print time[i],"go to",high_supply[i]
	#print 

plt.step(time, high_supply,time,low_supply)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

#uncomment below to joint-plot supply
plt.ylabel('Units (3kWh each)')
plt.show()

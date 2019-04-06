import math
from operator import attrgetter 

def get_time_slice(total, n) :

	mean = math.floor(total/n)

	return mean

class Process :
	def __init__(self, name = None, burst = 0, arrival = 0, rr = 0, rbt = 0, uwt = 0):
		self.name = name
		self.burst = burst  	#burst time
		self.arrival = arrival	#arrival time
		self.rr = rr 			#response ratio
		self.rbt = burst 		#remaining burst time, initialised to burst time
		self.uwt = 0 - arrival 	#updated waiting time

	def __lt__(self,other) :
		if self.arrival < other.arrival :
			return True
		else :
			return False

	def __gt__(self,other) :
		if self.arrival > other.arrival :
			return True
		else :
			return False

def HRRN(process_list):
	n = len(process_list)
	time=0
	cs=0
	rQueue=sorted(process_list) #Ready queue
	completed=[]
	
	while rQueue!=[]:
		skip=None
		print("\nTime:", time)
		#quantum time
		quantum=math.ceil(sum(process.rbt for process in rQueue)/len(rQueue))
		print("Quantum:", quantum)
		#calculating response ratios
		print("RRs:")
		for process in rQueue:
			#if process not in skip:
			rr=(process.uwt+process.rbt)/process.rbt 
			print(process.name, rr)
			process.rr=rr
		


		#selecting process with the highest reponse ratio
		HRR=max(rQueue, key=attrgetter('rr')) 
		

		print("-> %s added." % HRR.name) 
		

		print("RBT:", HRR.rbt)

		if (HRR.rbt<=quantum):
			print("%s is complete." % HRR.name)
			#removing completed processes
			rQueue.remove(HRR)
			time+=HRR.rbt 	
			completed.append(HRR)
			time_passed=HRR.rbt



		else:
			#updating remaining burst time
	
			HRR.rbt-=quantum
			time+=quantum
			print("Incomplete >> RBT:", HRR.rbt)
			time_passed=quantum

		#update waiting times of all other process

	
		for process in rQueue:
			if process != HRR:	 
				print(process.name)
				process.uwt+=time_passed
				

	
					
		
		cs+=1

		print("\nName\tUWT\tRBT\tRR")
		for process in process_list:
			for p in rQueue:
				if process.name==p.name:
					process=p
					break 
			else:
				for p in completed:
					if process.name==p.name:
						process=p
						break

			print(process.name+"\t"+str(process.uwt)+"\t"+str(process.rbt)+"\t"+str(process.rr))


	print("\nWaiting Times:")
	for process in completed:
		print(process.name, process.uwt)
	
	avg_wt=sum(process.uwt for process in completed)/n
	avg_tat=(sum(process.uwt for process in completed)+sum(process.burst for process in completed))/n
	print("\nAverage waiting time: \t\t\t%f" % avg_wt)
	print("Average turnaround time: \t\t%f" % avg_tat)
	print("Total number of context switches: \t%d" % int(cs - 1))



process_list = []
process_list.append(Process('P1',80,0))
process_list.append(Process('P2',72,2))
process_list.append(Process('P3',65,3))
process_list.append(Process('P4',50,4))
process_list.append(Process('P5',43,5))
#time_slice = math.floor((3+6+4+5+2)/5)
#print(time_slice)

HRRN(process_list)

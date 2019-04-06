import math
from operator import attrgetter 
import time as t
import copy

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
		self.uwt = 0   		    #updated waiting time

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


def HRRN(static_process_list,verbose=False):
	n = len(static_process_list)
	cs=0
	process_list=sorted(static_process_list) 
	time=process_list[0].arrival #assigning time to the shortest arrival time of all processes
	completed=[]
	#rQueue=copy.deepcopy(process_list) 
	rQueue=list(filter(lambda obj : obj.arrival <= time, process_list))

	while process_list!=[]:
	
		print("\nTime:", time)
		#quantum time
		quantum=math.floor(sum(process.rbt for process in process_list)/len(process_list))
		print("Quantum:", quantum)
		#calculating response ratios
		print("RRs:")
		for process in rQueue:
			rr=(process.uwt+process.rbt)/process.rbt 
			print(process.name, rr)
			process.rr=rr
		


		#selecting process with the highest reponse ratio
		start=t.perf_counter()
		HRR=max(rQueue, key=attrgetter('rr')) 
		end=t.perf_counter()
		perf=end-start

		print("-> %s added." % HRR.name) 
		

		print("RBT:", HRR.rbt)

		if (HRR.rbt<=quantum):
			print("%s is complete." % HRR.name)
			#removing completed processes
			rQueue.remove(HRR)
			process_list.remove(HRR)
			time+=HRR.rbt 	
			completed.append(HRR)
			time_passed=HRR.rbt
			rQueue=list(filter(lambda obj : obj.arrival <= time, process_list)) #updating rqueue



		else:
			#updating remaining burst time
	
			HRR.rbt-=quantum
			time+=quantum
			print("Incomplete >> RBT:", HRR.rbt)
			time_passed=quantum
			rQueue=list(filter(lambda obj : obj.arrival <= time, process_list)) #updating rqueue

		#update waiting times of all other process

	
		for process in rQueue:
			if process != HRR:	 
				process.uwt+=time_passed
				

	
					
		
		cs+=1

	if verbose==True:
		print("\n\t\tName\tUWT\tRBT\tRR")
		for process in static_process_list:
			for p in rQueue:
				if process.name==p.name:
					process=p
					print('Arrived',end='>\t')
					break 
			else:
				for p in completed:
					if process.name==p.name:
						process=p
						print('Completed',end='>\t')
						break
				else:
					print('Not Arrived', end='>\t')

			print(process.name+"\t"+str(process.uwt)+"\t"+str(process.rbt)+"\t"+str(process.rr))


		print("\nWaiting Times:")
		for process in completed:
			print(process.name, process.uwt)


			avg_wt=sum(process.uwt for process in completed)/n
			avg_tat=(sum(process.uwt for process in completed)+sum(process.burst for process in completed))/n
			print("\nAverage waiting time: \t\t\t%f" % avg_wt)
			print("Average turnaround time: \t\t%f" % avg_tat)
			print("Total number of context switches: \t%d" % int(cs - 1))
			print("Seconds taken for max function: \t%f" % perf)


if __name__ == '__main__':
	process_list = []
	process_list.append(Process('P1',80,0))
	process_list.append(Process('P2',72,2))
	process_list.append(Process('P3',65,3))
	process_list.append(Process('P4',50,4))
	process_list.append(Process('P5',43,5))
	#time_slice = math.floor((3+6+4+5+2)/5)
	#print(time_slice)

	HRRN(process_list, verbose=True)


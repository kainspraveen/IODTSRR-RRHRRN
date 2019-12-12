import math
from operator import attrgetter 
import time as t
import copy

class Process:
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


def printer(info, flag=True,end='\n',flush=True):
	if flag==True:
		print(info,end=end,flush=flush)

def HRRN(static_process_list,verbose=True,performance_mode=False):
	n = len(static_process_list)
	cs=-1
	process_list=sorted(static_process_list) 
	time=process_list[0].arrival #assigning time to the shortest arrival time of all processes
	completed=[]
	#rQueue=copy.deepcopy(process_list) 
	rQueue=list(filter(lambda obj : obj.arrival <= time, process_list))
	

	while process_list!=[]:
		if rQueue==[]:
			process_list.sort() 
			time=process_list[0].arrival #assigning time to the shortest arrival time of all processes
			rQueue=list(filter(lambda obj : obj.arrival <= time, process_list))
		printer("\nTime: %d" % time,verbose)
		#quantum time
		quantum=math.floor(sum(process.rbt for process in process_list)/len(process_list))
		printer("Quantum: %d" % quantum,verbose)
		#calculating response ratios
		printer("RRs:", verbose)
		for process in rQueue:
			rr=(process.uwt+process.rbt)/process.rbt 
			printer(process.name+':'+str(rr), verbose)
			process.rr=rr
		


		#selecting process with the highest reponse ratio
		start=t.perf_counter()
		HRR=max(rQueue, key=attrgetter('rr')) 
		end=t.perf_counter()
		perf=end-start

		printer("-> %s added." % HRR.name, verbose) 
		

		printer("RBT: %d" % HRR.rbt, verbose)

		if (HRR.rbt<=quantum):
			printer("%s is complete." % HRR.name, verbose)
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
			printer("Incomplete >> RBT: %d" % HRR.rbt, verbose)
			time_passed=quantum
			rQueue=list(filter(lambda obj : obj.arrival <= time, process_list)) #updating rqueue

		#update waiting times of all other process


		for process in rQueue:
			if process != HRR:	 
				process.uwt+=time_passed

					
		
		cs+=1
	avg_wt=sum(process.uwt for process in completed)/n
	avg_tat=(sum(process.uwt for process in completed)+sum(process.burst for process in completed))/n
	
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



		print("\nAverage waiting time: \t\t\t%f" % avg_wt)
		print("Average turnaround time: \t\t%f" % avg_tat)
		print("Total number of context switches: \t%d" % cs)
		print("Seconds taken for max function: \t%f" % perf)

	if performance_mode==True:
		return [avg_wt,avg_tat,cs]

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


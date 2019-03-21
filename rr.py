import math

class Process : #process block stores details of the process
	def __init__(self, name = None, burst = 0, arrival = 0):
		self.name = name
		self.burst = burst
		self.arrival = arrival

	def __lt__(self,other) : #operator overloading for sorting
		if self.arrival < other.arrival :
			return True
		else :
			return False

	def __gt__(self,other) : #operator overloading for sorting
		if self.arrival > other.arrival :
			return True
		else :
			return False


def round_robin(process_list, time_slice) :

	process_list.sort() #sorts according to the arrival time
	time = 0			#time counter
	process_count = 0	#keeps track of the next process to be added to the que based on arrival time
	n = len(process_list)

	#print('time: ',time)

	que = [] #schedule que

	for i in range(len(process_list)) : #for adding all the processes having arrival time 0 to the scheduling que

		if process_list[i].arrival <= time : # adds the process to scheduling que  when its time for it to arrive
			print("process ", process_list[process_count].name, ' added')
			que.append(process_list[i])

		
		else :
			process_count = i 
			break

		print('time: ',time)
		#time += 1


	#print(que)

	'''for i in que :
		print(i.name)'''



	while que != [] : #run when until que is empty

		process = que.pop(0)
		print(process.name, ' ', process.burst)


		if process.burst <= time_slice : #executes process until it gets finished (burst time remaining is < time slice)

			for i in range(process.burst) : #increment time counter
				time += 1
				print('time: ',time)


				if (process_count < n) and (process_list[process_count].arrival <= time) : #if process list not empty and its time for arrival of new process add it to scheduling que
					print("process ", process_list[process_count].name, ' added')
					que.append(process_list[process_count])
					process_count+=1


			continue

		for i in range(time_slice) : #for case when remainig burst time is greater than  time slice
			time += 1
			print('time: ',time)
			process.burst -= 1


			if (process_count < n) and (process_list[process_count].arrival <= time) :
				print("process ", process_list[process_count].name, ' added')
				que.append(process_list[process_count])
				process_count += 1


		#print(process.name, ' ', process.burst)

		que.append(process)



process_list = []
process_list.append(Process('A',3,0))
process_list.append(Process('B',6,2))
process_list.append(Process('C',4,4))
process_list.append(Process('D',5,6))
process_list.append(Process('E',2,8))
time_slice = math.floor((3+6+4+5+2)/5)
print(time_slice)

round_robin(process_list, time_slice)

import math

def get_time_slice(total, n) :

	mean = math.floor(total/n)

	return mean

class Process :
	def __init__(self, name = None, burst = 0, arrival = 0):
		self.name = name
		self.burst = burst
		self.arrival = arrival

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


def round_robin(process_list, time_slice) :

	process_list.sort()
	time = 0
	process_count = 0
	n = len(process_list)
	total = 0

	for i in process_list :
		total += i.burst


	#print('time: ',time)

	que = []

	for i in range(len(process_list)) :

		if process_list[i].arrival <= time :
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



	while que != [] :

		print("				total: ",total)
		print("				num: ", n)


		time_slice = get_time_slice(total, n)
		print("time slice: ", time_slice)

		process = que.pop(0)
		print(process.name, ' ', process.burst)


		if process.burst <= time_slice :

			for i in range(process.burst) :
				time += 1
				print('time: ',time)


				if (process_count < n) and (process_list[process_count].arrival <= time) :
					print("process ", process_list[process_count].name, ' added')
					que.append(process_list[process_count])
					process_count+=1


			total -= process.burst
			n-=1




			continue

		for i in range(time_slice) :
			time += 1
			print('time: ',time)
			process.burst -= 1


			if (process_count < n) and (process_list[process_count].arrival <= time) :
				print("process ", process_list[process_count].name, ' added')
				que.append(process_list[process_count])
				process_count += 1


		#print(process.name, ' ', process.burst)
		total -= time_slice

		que.append(process)



process_list = []
process_list.append(Process('A',3,0))
process_list.append(Process('B',6,2))
process_list.append(Process('C',4,4))
process_list.append(Process('D',5,6))
process_list.append(Process('E',2,8))
time_slice = math.floor((3+6+4+5+2)/5)
#print(time_slice)

round_robin(process_list, time_slice)

import dqrr
import hrrn


class process :

	def __init__(self, name="", arrival=0, burst=0):
		self.name = name
		self.arrival = arrival
		self.burst = burst



process_list = []

def init_MyThread(process_list) :

	thread_list = []

	for i in process_list :
		obj = dqrr.MyThread(i.name, i.burst, i.arrival)

		thread_list.append(obj)

	return thread_list


def init_Process(process_list) :

	Process_list = []

	for i in process_list :
		obj = hrrn.Process(name = i.name, burst = i.burst, arrival = i.arrival)

		Process_list.append(obj)

	return thread_list

thread_list = []
Process_list = []

thread_list = init_MyThread(process_list)
Process_list = init_Process(process_list)

def turnaround_time() :
	pass




print("dqrr")
#dqrr.iodstrr_thread(thread_list)
print("hrrn")

hrrn.HRRN(Process_list)


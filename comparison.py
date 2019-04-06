import dqrrr
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
		obj = dqrrr.MyThread(i.name, i.burst, i.arrival)

		thread_list.append(obj)


def init_Process(process_list) :

	Process_list = []

	for i in process_list :
		obj = hrrn.Process(name = i.name, burst = i.burst, arrival = i.arrival)

		Process_list.append(obj)



dqrrr.iodstrr_thread(thread_list)

dqrrr.HRRN(Process_list)
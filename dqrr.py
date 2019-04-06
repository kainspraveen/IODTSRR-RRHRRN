from threading import Thread
import time
import random
import queue
from statistics import median
from math import floor



class MyThread:
	def __init__(self,id,burst,start):
		self.ID = id
		self.Name = None
		self.burst = burst
		self.start = start
		self.rburst=burst
		self.waiting=None
		self.TurnAround=None
                        

threads=[]

class DQRR :

	def __init__(self) :

		self.threads = []
		self.t = 0
		self.mark = 0
		self.rem_bt = []


	def task(self):
		while(True):
			for i in range(self.mark,len(self.threads)):
						if(self.threads[i].start <= self.t):
							self.rem_bt.append(self.threads[i])
							self.mark=i
			#print("__*__")
			if(self.mark==len(self.threads)-1):
				break

	def fill_threadList(self) :

		'''for i in range(10):
			self.threads.append(MyThread(i,random.randint(2,25),random.randint(0,6)))
			#print("proceess ", i, " : ", threads[len(threads)-1:].burst, " , ", threads[len(threads)-1:].start)

		for i in self.threads:
			print(i.burst, i.start)'''

		self.threads.append(MyThread(1,30,0))
		self.threads.append(MyThread(2,42,0))
		self.threads.append(MyThread(3,50,0))
		self.threads.append(MyThread(4,85,0))
		self.threads.append(MyThread(5,97,0))

	#task_thread = []

	def apply_cpu_time(self,quantum):
		
		temp_rem_bt = []

		i =0
		j= len(self.rem_bt) - 1

		for k in range(len(self.rem_bt)) :

			if k%2 == 0 :

				temp_rem_bt.append(self.rem_bt[i])
				i+=1

			else :
				temp_rem_bt.append(self.rem_bt[j])
				j-=1


		print(list(map(lambda a : a.ID, temp_rem_bt))) 

		done = True

		for i in range(len(temp_rem_bt)):

			if(temp_rem_bt[i].rburst > 0): 
				done = False
                #print("**")  
                  
				if (temp_rem_bt[i].rburst > quantum):   
					self.t += quantum   
					temp_rem_bt[i].rburst -= quantum  
                  
 
				else:  
					self.t = self.t + temp_rem_bt[i].rburst 
					temp_rem_bt[i].waiting = self.t - temp_rem_bt[i].burst 
					temp_rem_bt[i].rburst = 0

		return done


	def iodstrr(self):
		#rem_bt=[]

	    #for i in range(len(threads)):
	    #	rem_bt[i]=threads[i].burst
	    
		#t=0
	    #readyq=[]
		self.threads.sort(key=lambda t : t.start)
		#mark=0

		thread=Thread(target=self.task, args=())
		#task_thread.append(thread)
		thread.daemon = True
		thread.start()

		while(True):
			done=True


			#thread.join()

			'''for i in range(self.mark,len(self.threads)):
				if(self.threads[i].start <= self.t):
					print("process: ", self.threads[i].rburst )
					self.rem_bt.append(self.threads[i])
					self.mark=i'''

			if(len(self.rem_bt)==0):
				self.t+=1
				continue

			self.rem_bt=list(filter(lambda a: a.rburst != 0, self.rem_bt))
	    	#rem_bt.sort(key = lambda x : x.rburst, rem_bt)

			

			temp=[i.rburst for i in self.rem_bt]
			if(len(self.rem_bt) != 0):
				print(len(temp))
				print(temp)

				quantum=floor(median(temp))

			print("quantum: ", quantum)



			self.rem_bt.sort(key= lambda rem_burst : rem_burst.rburst)
	    	

			done = self.apply_cpu_time(quantum)

			if(done == True):
				break
				


			if(done == True):
				break


		print("TurnAround Times:")
		j=1
		wait=0
		turn=0
		
		for i in self.threads:
			print("Process", j," : ", end="")
			print(i.burst+i.waiting)
			turn+=(i.burst+i.waiting)
			j+=1

		print("Waiting Times: ")
		j=1
		for i in self.threads:
			print("Process", j, ":", end="")
			print(i.waiting)
			wait+=i.waiting
			j+=1

		wait=wait/len(self.threads)
		turn=turn/len(self.threads)
		print("Average Waiting Time :", wait)
		print("Average TurnAround Time: ", turn)

'''new=Thread(target=iodstrr, args=(threads,))
new.start()
new.join()'''

'''print("\n\n")
print(len(task_thread))
for i in task_thread :
	print(i.name)'''
  


obj = DQRR()
obj.fill_threadList()
obj.iodstrr()


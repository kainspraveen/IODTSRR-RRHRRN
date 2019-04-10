from threading import Thread
import time
import random
import queue
from statistics import median
from math import floor
from copy import deepcopy
import threading
from operator import attrgetter
lock = threading.Lock()
from err import printer

class MyThread:
	def __init__(self,id= "",burst = 0,start = 0):
		self.ID = id
		self.Name = None
		self.burst = burst
		self.start = start
		self.rburst=burst
		self.waiting=None
		self.TurnAround=None
                        

#threads=[]

class DQRR :

	def __init__(self, threads = [],verbose=False) :

		self.threads = deepcopy(threads)
		self.t = 0
		self.mark = 0
		self.rem_bt = []

		self.wait=0
		self.turn=0
		self.CS = -1

		self.counter = 0
		self.processNum = len(self.threads)
		self.verbose=verbose

		#self.insertQue_thread=Thread(target=self.task, args=())


	def task(self):
		while(True):
			#printer(self.threads)
			for i in range(self.mark,len(self.threads)):
				#lock.acquire()
				if(self.threads[i].start <= self.t):
					self.rem_bt.append(self.threads[i])
					self.mark=i
				#lock.release()
			#printer("__*__")
			if(self.mark==self.processNum-1):
				break

	def fill_threadList(self) :



		self.threads.append(MyThread(1,80,0))
		self.threads.append(MyThread(2,72,2))
		self.threads.append(MyThread(3,65,3))
		self.threads.append(MyThread(4,50,4))
		self.threads.append(MyThread(5,43,5))

	



		#self.threads.append(MyThread(1,26,6))
		#self.threads.append(MyThread(2,82,70))
		#self.threads.append(MyThread(3,70,75))
		#self.threads.append(MyThread(4,31,80))
		#self.threads.append(MyThread(5,40,100))

		self.processNum = len(self.threads)

		#self.t = self.threads[0].start
		#self.rem_bt.append(self.threads[0])

	#task_thread = []

	def apply_cpu_time(self,quantum,que_copy):
		
		temp_rem_bt = []

		i =0
		j= len(self.rem_bt) - 1

		for k in range(len(self.rem_bt)) :

			if k%2 == 0 :

				temp_rem_bt.append(self.rem_bt[i])
				i+=1

			if i >= j :
				continue

			else :
				temp_rem_bt.append(self.rem_bt[j])
				j-=1


		printer(list(map(lambda a : a.ID, temp_rem_bt)),flag=self.verbose) 

		self.CS += len(temp_rem_bt)

		done = True

		for i in range(len(temp_rem_bt)):

			if(temp_rem_bt[i].rburst > 0): 
				done = False
                #printer("**")  
                  
				if (temp_rem_bt[i].rburst > quantum):   
					self.t += quantum   
					temp_rem_bt[i].rburst -= quantum  
                  
 
				else:  
					self.t = self.t + temp_rem_bt[i].rburst 
					temp_rem_bt[i].waiting = self.t - temp_rem_bt[i].burst - temp_rem_bt[i].start
					temp_rem_bt[i].rburst = 0
					que_copy.remove(temp_rem_bt[i])



		#return done


	def pushQue(self,que_copy) :

		for i in que_copy :
			if i.start <= self.t :
				self.rem_bt.append(i)



	def iodstrr(self):
		#rem_bt=[]

	    #for i in range(len(threads)):
	    #	rem_bt[i]=threads[i].burst
	    
		#t=0
	    #readyq=[]
		self.threads.sort(key=lambda t : t.start)
		#mark=0

		que_copy = self.threads[:]

		
		#task_thread.append(thread)


		cs = 0

		#for m in range(10):
		while True:
			done=False

			#printer("iodstrr")
			#printer(self.rem_bt)

			#thread.join()


			'''for i in range(self.mark,len(self.threads)):
				if(self.threads[i].start <= self.t):
					printer("process: ", self.threads[i].rburst )
					self.rem_bt.append(self.threads[i])
					self.mark=i'''

			#lock.acquire()
			self.pushQue(que_copy)

			printer("ready que: ",end='',flag=self.verbose)
			printer(list(map(lambda x: x.ID, self.rem_bt)),flag=self.verbose)

			if(len(self.rem_bt)==0):



				self.t+=1
				
				continue

			#lock.release()
			
			#printer("iodstrr")

			self.rem_bt=list(filter(lambda a: a.rburst != 0, self.rem_bt))
	    	#rem_bt.sort(key = lambda x : x.rburst, rem_bt)

			

			temp=[i.rburst for i in self.rem_bt]
			if(len(self.rem_bt) != 0):
				printer("length of readyq: ", end='',flag=self.verbose)
				printer(len(temp),flag=self.verbose)
				printer("burst times in ready q : ",end='',flag=self.verbose)
				printer(temp,flag=self.verbose)

				quantum=floor(median(temp))

			printer("quantum: %d " %  quantum,flag=self.verbose)



			self.rem_bt.sort(key= lambda rem_burst : rem_burst.rburst)
	    	

			#done = self.apply_cpu_time(quantum)

			self.apply_cpu_time(quantum,que_copy)

			#cs +=1
			if que_copy == [] :
				done = True

			if(done == True):
				break
				





	def stats(self) :

		j=1

		
		for i in self.threads:

			self.turn+=(i.burst+i.waiting)
			j+=1


		
		j=1
		for i in self.threads:

			self.wait+=i.waiting
			#printer(i.waiting)
			j+=1

		self.wait=self.wait/len(self.threads)
		self.turn=self.turn/len(self.threads)

		printer("avgWT\tavgTAT\tCSs",flag=self.verbose)
		printer(str(self.wait)+"\t"+str(self.turn)+"\t"+str(self.CS),flag=self.verbose)

		return [self.wait,self.turn,self.CS]


'''new=Thread(target=iodstrr, args=(threads,))
new.start()
new.join()'''

'''printer("\n\n")
printer(len(task_thread))
for i in task_thread :
	printer(i.name)'''
  


'''obj = DQRR()
obj.fill_threadList()
#obj.insertQue_thread.start()
obj.iodstrr()
#time.sleep(10)
printer(obj.stats())'''

if __name__ == '__main__':
	obj = DQRR(verbose=True)
	obj.fill_threadList()
	obj.iodstrr()
	obj.stats()
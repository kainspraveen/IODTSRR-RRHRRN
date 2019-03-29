import threading
import time
import random
import queue
import time
from statistics import median



class MyThread:
	def __init__(self,id,burst,start):
		self.ThreadID = id
		self.Name = None
		self.burst = burst
		self.start = start
		self.rburst=burst
		self.waiting=None
		self.TurnAround=None
                        

threads=[]
for i in range(10):
	threads.append(MyThread(i,random.randint(0,25),random.randint(0,6)))



def iodtsrr(threads):
	rem_bt=[]

    #for i in range(len(threads)):
    #	rem_bt[i]=threads[i].burst
    
	t=0
    #readyq=[]
	threads.sort(key=lambda t : t.start)
	mark=0

	while(True):
		done=True

		for i in range(mark,len(threads)):
			if(threads[i].start <= t):
				rem_bt.append(threads[i])
				mark=i
				
		if(len(rem_bt)==0):
			t+=1
			continue

		rem_bt=list(filter(lambda a: a.rburst != 0, rem_bt))
    	#rem_bt.sort(key = lambda x : x.rburst, rem_bt)
		temp=[i.rburst for i in rem_bt]
		if(len(rem_bt) != 0):
			quantum=median(temp)



		rem_bt.sort(key= lambda rem_bt : rem_bt.rburst)
    	
    	#present=0
		for i in range(len(rem_bt)):

			if(rem_bt[i].rburst > 0): 
				done = False
                #print("**")  
                  
				if (rem_bt[i].rburst > quantum):   
					t += quantum   
					rem_bt[i].rburst -= quantum  
                  
 
				else:  
					t = t + rem_bt[i].rburst 
					rem_bt[i].waiting = t - rem_bt[i].burst 
					rem_bt[i].rburst = 0

		if(done == True):
			break

	print("TurnAround Times:")
	j=1
	wait=0
	turn=0
	for i in threads:
		print("Process", j," : ", end="")
		print(i.burst+i.waiting)
		turn+=(i.burst+i.waiting)
		j+=1

	print("Waiting Times: ")
	j=1
	for i in threads:
		print("Process", j, ":", end="")
		print(i.waiting)
		wait+=i.waiting
		j+=1

	wait=wait/len(threads)
	turn=turn/len(threads)
	print("Average Waiting Time :", wait)
	print("Average TurnAround Time: ", turn)

iodtsrr(threads)

  
  
  

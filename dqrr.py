from threading import Thread
import time
import random
import queue
import time
from statistics import median



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
def task(mark, threads,t,rem_bt):
	while(True):
		for i in range(mark,len(threads)):
					if(threads[i].start <= t):
						rem_bt.append(threads[i])
						mark=i
		#print("__*__")
		if(mark==len(threads)-1):
			break

for i in range(10):
	threads.append(MyThread(i,random.randint(2,25),random.randint(0,6)))
	#print("proceess ", i, " : ", threads[len(threads)-1:].burst, " , ", threads[len(threads)-1:].start)

for i in threads:
	print(i.burst, i.start)


def iodstrr(threads):
	rem_bt=[]

    #for i in range(len(threads)):
    #	rem_bt[i]=threads[i].burst
    
	t=0
    #readyq=[]
	threads.sort(key=lambda t : t.start)
	mark=0

	while(True):
		done=True


		thread=Thread(target=task, args=(mark,threads, t,rem_bt))
		thread.daemon = True
		thread.start()
		#thread.join()

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

			#time.sleep(100)

		if(done == True):
			break
			


		if(done == True):
			break




def iodstrr_thread(threads) :
	new=Thread(target=iodstrr, args=(threads,))
	new.start()
	new.join()


iodstrr_thread(threads)


  
  




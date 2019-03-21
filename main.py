import threading
import time
import random
import queue
import time
from statistics import median

class myThread(threading.Thread):
  def __init__(self, threadID, name,start, burst):
    threading.Thread.__init__(self):
      self.threadID = threadID
      self.name = name
      self.burst = burst
      self.start = start
      
  def run(self):
     pass
     
threads=[]
for i in range(10):
  threads.append(myThread(i, str(i),random.randint(0,6),random.randint(5,25)))



def iodstrr(threads):
  q=Queue.PriorityQueue(len(threads))
  
  for i in threads:
    q.put(i.burst, i)
  
  temp = []
  for i in threads:
    temp.append(threads.burst)
  
  TimeQuantum=median(temp)
  while(True):
    start=time.time()
    for i in threads:
      if(i.start == time.time()-start):
        i.run()
    
  
  
  

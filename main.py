import threading
import time
import random
import queue

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
  
  
  
  

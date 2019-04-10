import threading
from threading import Thread
import time
import queue
#from statistics import median
from math import floor
import os

from err import ERR, Process, printer

from dqrr import MyThread, DQRR
import pandas as pd
import random
import math
from copy import deepcopy



def process_generator(n=100,behaviour='inc',arrival_times=False, verbose=True):
	err_list=[]
	dqrr_list=[]
	
	err_avg_WTs=[]
	err_avg_TATs=[]
	err_CSs=[]

	dqrr_avg_WTs=[]
	dqrr_avg_TATs=[]
	dqrr_CSs=[]

	Pnames=[]
	pperc=0
	processes=[]
	printer("Generating...")
	if behaviour=='inc':
		g_burst=1
		
	elif behaviour=='dec':
		g_burst=n*4+1
	g_arrival=0
	for i in range(n):
		if behaviour=='inc':
			g_burst+=random.randint(1,4)

		elif behaviour=='rand':
			g_burst=random.randint(1,100)

		elif behaviour=='dec':
			g_burst-=random.randint(1,4)

		else:
			print("Invalid argument provided.")
			exit()
		if arrival_times!=False:
			g_arrival+=random.randint(1,4)

		Pname='P'+str(i+1)
		Pnames.append(Pname)

		processes.append(i+1)


		err_list.append(Process(Pname,g_burst,g_arrival))
		dqrr_list.append(MyThread(id = Pname, burst = g_burst,start = g_arrival))

		err_perf=ERR(err_list,verbose=False,performance_mode=True)

		obj = DQRR(deepcopy(dqrr_list))
		#obj.insertQue_thread.daemon = True
		#obj.insertQue_thread.start()

		obj.iodstrr()

		dqrr_perf = obj.stats()
		
		perc=math.ceil(((i+1)/n)*100)

		if pperc!=perc:
			pperc=perc
			printer("█", end='')

		err_avg_WTs.append(err_perf[0])
		err_avg_TATs.append(err_perf[1])
		err_CSs.append(err_perf[2])

		dqrr_avg_WTs.append(dqrr_perf[0])
		dqrr_avg_TATs.append(dqrr_perf[1])
		dqrr_CSs.append(dqrr_perf[2])

	data=pd.DataFrame({
						'no_of_processes' : processes,
						'err_avg_wait_time' : err_avg_WTs,
					 	'err_avg_turnaround_time' : err_avg_TATs,	
						'err_context_switches' : err_CSs,
						'dqrr_avg_wait_time' : dqrr_avg_WTs,
						'dqrr_avg_turnaround_time' : dqrr_avg_TATs,	
						'dqrr_context_switches' : dqrr_CSs,
					   })
	if arrival_times==False:
		arrival_state='z'
	else:
		arrival_state='nz'
	
	Fname=str(n)+'_'+behaviour+'_'+arrival_state+'.csv'
	printer("\n%s generated." % Fname, verbose)
	data.to_csv('CSVs/'+Fname, index=False)
	

if __name__ == '__main__':
	os.makedirs('CSVs')
	n=int(input("Enter number of processes to generate: "))
	comb=input("Generate for all behaviours? [Y/n]: ")
	if comb=='y' or comb=='Y':
		behs=['inc','dec','rand']
		arrives=[True,False]
		for beh in behs:
			for arrive in arrives:
				process_generator(n,behaviour=beh,arrival_times=arrive)
	else:
		beh=input("Specify burst generation behaviour [inc,dec,rand]:")
		arrive=input("Arrival times? [Y/n]: ")
		if arrive=='y' or arrive=='Y':
			arrive=True
		else: 
			arrive=False
		process_generator(n,behaviour=beh,arrival_times=arrive)	

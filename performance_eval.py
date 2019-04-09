from hrrn import HRRN, Process, printer
import pandas as pd
import random
import math

def process_generator(n=100,behaviour='inc',arrival_times=False, verbose=True):
	process_list=[]
	avg_WTs=[]
	avg_TATs=[]
	CSs=[]
	Pnames=[]
	pperc=0
	printer("Generating...")
	if behaviour=='inc':
		g_burst=1
	elif behaviour=='dec':
		g_burst=n*4+1
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
		if arrival_times==False:
			g_arrival=0
		else:
			g_arrival=random.randint(1,100)
		Pname='P'+str(i+1)
		Pnames.append(Pname)

		process_list.append(Process(Pname,g_burst,g_arrival))
		perf=HRRN(process_list,verbose=False,performance_mode=True)
		
		
		
		perc=math.ceil(((i+1)/n)*100)

		if pperc!=perc:
			pperc=perc
			printer("█", end='')

		avg_WTs.append(perf[0])
		avg_TATs.append(perf[1])
		CSs.append(perf[2])

	data=pd.DataFrame({'process_name' : Pnames,
					   'avg_wait_time' : avg_WTs,
					   'avg_turnaround_time' : avg_TATs,	
					   'context_switches' : CSs})
	if arrival_times==False:
		arrival_state='z'
	else:
		arrival_state='nz'
	
	Fname=str(n)+'_'+behaviour+'_'+arrival_state+'.csv'
	printer("\n%s generated." % Fname, verbose)
	data.to_csv(Fname, index=False)
	
if __name__ == '__main__':
	n=int(input("Enter number of processes to generate: "))
	comb=input("Generate for all behaviours? [Y/n]: ")
	if comb=='y' or comb=='Y':
		behs=['inc','dec','rand']
		arrives=[True,False]
		for beh in behs:
			for arrive in arrives:
				process_list=process_generator(n,behaviour=beh,arrival_times=arrive)
	else:
		beh=input("Specify burst generation behaviour [inc,dec,rand]:")
		arrive=input("Arrival times? [Y/n]: ")
		if arrive=='y' or arrive=='Y':
			arrive=True
		else: 
			arrive=False
		process_list=process_generator(n,behaviour=beh,arrival_times=arrive)
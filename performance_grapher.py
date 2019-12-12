import threading
from threading import Thread
import time
import random
import queue
from statistics import median
from math import floor
from err import ERR, Process, printer
from dqrr import MyThread, DQRR
import pandas as pd
import math
from copy import deepcopy
import seaborn as sns
import os
import matplotlib.pyplot as plt



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
	data.to_csv('Data/'+Fname, index=False)

	TATcols=['dqrr_avg_turnaround_time', 'err_avg_turnaround_time','no_of_processes']
	WTcols=['dqrr_avg_wait_time', 'err_avg_wait_time','no_of_processes']
	CScols=['dqrr_context_switches', 'err_context_switches','no_of_processes']

	df=data
	cols=df.columns

	df_TAT=pd.DataFrame(df[TATcols])
	df_WT=pd.DataFrame(df[WTcols])
	df_CS=pd.DataFrame(df[CScols])

	printer("████████████████████", end='')

	df_TAT.rename(columns={'dqrr_avg_turnaround_time':'Dynamic Quantum Re-adjusted Round Robin', 'err_avg_turnaround_time':'Enhanced Reactive Ratio'}, inplace=True)
	df_WT.rename(columns={'dqrr_avg_wait_time':'Dynamic Quantum Re-adjusted Round Robin', 'err_avg_wait_time':'Enhanced Reactive Ratio'}, inplace=True)
	df_CS.rename(columns={'dqrr_context_switches':'Dynamic Quantum Re-adjusted Round Robin', 'err_context_switches':'Enhanced Reactive Ratio'}, inplace=True)


	df_TAT_melted=pd.melt(df_TAT, id_vars='no_of_processes', value_name='time',var_name='Algorithms')
	df_WT_melted=pd.melt(df_WT, id_vars='no_of_processes', value_name='time',var_name='Algorithms')
	df_CS_melted=pd.melt(df_CS, id_vars='no_of_processes', value_name='switches',var_name='Algorithms')

	printer("████████████████████", end='')

	#TAT

	sns.set(style='whitegrid', font='Calibri',palette='Reds_r')
	TATplot=sns.lineplot(x='no_of_processes',y='time', hue='Algorithms', style='Algorithms', data=df_TAT_melted)


	TATtitle=Fname.split('_')
	TATtitle.append('| Turn Around Time')
	TATtitle=' '.join(TATtitle)
	TATplot.set_title(TATtitle)

	TATfig=TATplot.get_figure()
	TATname=Fname+'_TAT.png'
	TATfig.savefig('Graphs/'+TATname)
	plt.clf()

	printer("████████████████████", end='')

	#WT

	sns.set(style='whitegrid', font='Calibri',palette='Greens_r')
	WTplot=sns.lineplot(x='no_of_processes',y='time', hue='Algorithms', style='Algorithms', data=df_WT_melted)

	WTtitle=Fname.split('_')
	WTtitle.append('| Waiting Time')
	WTtitle=' '.join(WTtitle)
	WTplot.set_title(WTtitle)

	WTfig=WTplot.get_figure()
	WTname=Fname+'_WT.png'
	WTfig.savefig('Graphs/'+WTname)
	plt.clf()

	printer("████████████████████", end='')

	#CS

	sns.set(style='whitegrid', font='Calibri',palette='Blues_r')
	CSplot=sns.lineplot(x='no_of_processes',y='switches', hue='Algorithms', style='Algorithms', data=df_CS_melted)

	CStitle=Fname.split('_')
	CStitle.append('| Context Switches')
	CStitle=' '.join(CStitle)
	CSplot.set_title(CStitle)

	CSfig=CSplot.get_figure()
	CSname=Fname+'_CS.png'
	CSfig.savefig('Graphs/'+CSname)
	plt.clf()

	printer("████████████████", end='')

	
	print("\n%s, %s, %s graphed.\n" % (TATname, WTname, CSname))
	
if __name__ == '__main__':
	#os.remove('Data')
	#os.remove('Graphs')
	os.makedirs('Data')
	os.makedirs('Graphs')
	n=int(input("Enter number of processes to generate: "))
	comb=input("Generate for all behaviours? [Y/n]: ")
	if comb=='y' or comb=='Y':
		printer("Generating...")
		behs=['inc','dec','rand']
		arrives=[True,False]
		for beh in behs:
			for arrive in arrives:
				process_generator(n,behaviour=beh,arrival_times=arrive)
	else:
		beh=input("Specify burst generation behaviour [inc,dec,rand]:")
		arrive=input("Arrival times? [Y/n]: ")
		printer("Generating...")
		if arrive=='y' or arrive=='Y':
			arrive=True
		else: 
			arrive=False
		process_generator(n,behaviour=beh,arrival_times=arrive)	

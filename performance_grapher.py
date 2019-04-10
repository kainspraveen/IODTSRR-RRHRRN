import threading
from threading import Thread
import time
import random
import queue
from statistics import median
from math import floor
from hrrn import HRRN, Process, printer
from dqrr import MyThread, DQRR
import pandas as pd
import math
from copy import deepcopy
import seaborn as sns
import os
import matplotlib.pyplot as plt



def process_generator(n=100,behaviour='inc',arrival_times=False, verbose=True):
	hrrn_list=[]
	dqrr_list=[]
	
	hrrn_avg_WTs=[]
	hrrn_avg_TATs=[]
	hrrn_CSs=[]

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

	start_skip=True

	
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
		if start_skip==True:
			g_arrival=0
			start_skip=False
		Pname='P'+str(i+1)
		Pnames.append(Pname)

		processes.append(i+1)


		hrrn_list.append(Process(Pname,g_burst,g_arrival))
		dqrr_list.append(MyThread(id = Pname, burst = g_burst,start = g_arrival))

		hrrn_perf=HRRN(hrrn_list,verbose=False,performance_mode=True)

		obj = DQRR(deepcopy(dqrr_list))
		obj.insertQue_thread.daemon = True
		obj.insertQue_thread.start()
		obj.iodstrr()

		dqrr_perf = obj.stats()


		
		perc=math.ceil(((i+1)/n)*100)

		if pperc!=perc:
			pperc=perc
			printer("█", end='')

		hrrn_avg_WTs.append(hrrn_perf[0])
		hrrn_avg_TATs.append(hrrn_perf[1])
		hrrn_CSs.append(hrrn_perf[2])

		dqrr_avg_WTs.append(dqrr_perf[0])
		dqrr_avg_TATs.append(dqrr_perf[1])
		dqrr_CSs.append(dqrr_perf[2])

	data=pd.DataFrame({
						'no_of_processes' : processes,
						'hrrn_avg_wait_time' : hrrn_avg_WTs,
					 	'hrrn_avg_turnaround_time' : hrrn_avg_TATs,	
						'hrrn_context_switches' : hrrn_CSs,
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
	data.to_csv(Fname, index=False)

	TATcols=['dqrr_avg_turnaround_time', 'hrrn_avg_turnaround_time','no_of_processes']
	WTcols=['dqrr_avg_wait_time', 'hrrn_avg_wait_time','no_of_processes']
	CScols=['dqrr_context_switches', 'hrrn_context_switches','no_of_processes']

	df=data
	cols=df.columns

	df_TAT=pd.DataFrame(df[TATcols])
	df_WT=pd.DataFrame(df[WTcols])
	df_CS=pd.DataFrame(df[CScols])

	printer("████████████████████", end='')

	df_TAT.rename(columns={'dqrr_avg_turnaround_time':'DQRR', 'hrrn_avg_turnaround_time':'HRRN'}, inplace=True)
	df_WT.rename(columns={'dqrr_avg_wait_time':'DQRR', 'hrrn_avg_wait_time':'HRRN'}, inplace=True)
	df_CS.rename(columns={'dqrr_context_switches':'DQRR', 'hrrn_context_switches':'HRRN'}, inplace=True)


	df_TAT_melted=pd.melt(df_TAT, id_vars='no_of_processes', value_name='time',var_name='Algorithms')
	df_WT_melted=pd.melt(df_WT, id_vars='no_of_processes', value_name='time',var_name='Algorithms')
	df_CS_melted=pd.melt(df_CS, id_vars='no_of_processes', value_name='switches',var_name='Algorithms')

	printer("████████████████████", end='')
	#TAT
	#plt.figure()
	sns.set(style='whitegrid', font='Calibri',palette='Reds_r')
	TATplot=sns.lineplot(x='no_of_processes',y='time', hue='Algorithms', style='Algorithms', data=df_TAT_melted)


	TATtitle=Fname.split('_')
	TATtitle.append('| Turn Around Time')
	TATtitle=' '.join(TATtitle)
	TATplot.set_title(TATtitle)

	TATfig=TATplot.get_figure()
	TATname=Fname+'_TAT.png'
	TATfig.savefig(TATname)
	plt.clf()

	printer("████████████████████", end='')

	#WT
	#plt.figure()
	sns.set(style='whitegrid', font='Calibri',palette='Greens_r')
	WTplot=sns.lineplot(x='no_of_processes',y='time', hue='Algorithms', style='Algorithms', data=df_WT_melted)

	WTtitle=Fname.split('_')
	WTtitle.append('| Waiting Time')
	WTtitle=' '.join(WTtitle)
	WTplot.set_title(WTtitle)

	WTfig=WTplot.get_figure()
	WTname=Fname+'_WT.png'
	WTfig.savefig(WTname)
	plt.clf()

	printer("████████████████████", end='')

	#CS
	#plt.figure()
	sns.set(style='whitegrid', font='Calibri',palette='Blues_r')
	CSplot=sns.lineplot(x='no_of_processes',y='switches', hue='Algorithms', style='Algorithms', data=df_CS_melted)

	CStitle=Fname.split('_')
	CStitle.append('| Context Switches')
	CStitle=' '.join(CStitle)
	CSplot.set_title(CStitle)

	CSfig=CSplot.get_figure()
	CSname=Fname+'_CS.png'
	CSfig.savefig(CSname)
	plt.clf()

	printer("████████████████", end='')
	
	print("\n%s, %s, %s graphed.\n" % (TATname, WTname, CSname))
	
if __name__ == '__main__':
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

import schedulers
import err
import matplotlib.pyplot as plt 
import random
import pandas as pd 
import numpy as np 


def process_gen(exp_name,n=10,gap=4) :

	inc =[]
	dec = []
	rand = []

	t_asc = random.randint(10,20)
	t_dec = n*gap+1

	for i in range(n) :
		inc.append(t_asc)
		dec.append(t_dec)
		rand.append(random.randint(10,130))
		t_asc+=random.randint(1,gap)
		t_dec-=random.randint(1,gap)

	
	return {'inc':inc,'dec':dec,'rand':rand}

def get_results(proc_lists,scheduler):
	return scheduler.run(proc_lists)


def graph(n,gap,exp_name) :


	inc_iodtsrr_results = [] 
	inc_hrrn_results = []
	inc_errn_results = []
	inc_errnx_results = []

	dec_iodtsrr_results = []
	dec_hrrn_results = []
	dec_errn_results = []
	dec_errnx_results = []

	rand_iodtsrr_results =[]
	rand_hrrn_results = []
	rand_errn_results = []
	rand_errnx_results = []

	for i in range(5,n+1,1) :

		proc_lists = process_gen(exp_name, i,gap)

		print('No of Processes: ',i)

		inc_iodtsrr_results.append(get_results([schedulers.BaseProcess('P'+str(i+1),proc_lists['inc'][i]) for i in range(len(proc_lists['inc']))],schedulers.IODTSRR()))
		inc_hrrn_results.append(get_results([schedulers.Process('P'+str(i+1),proc_lists['inc'][i]) for i in range(len(proc_lists['inc']))],schedulers.HRRN()))
		inc_errn_results.append(get_results([schedulers.ProcessEnh('P'+str(i+1),proc_lists['inc'][i]) for i in range(len(proc_lists['inc']))],schedulers.HRRN()))
		inc_errnx_results.append(get_results([err.Process('P'+str(i+1),proc_lists['inc'][i]) for i in range(len(proc_lists['inc']))],err.ERRN()))

		dec_iodtsrr_results.append(get_results([schedulers.BaseProcess('P'+str(i+1),proc_lists['dec'][i]) for i in range(len(proc_lists['dec']))],schedulers.IODTSRR()))
		dec_hrrn_results.append(get_results([schedulers.Process('P'+str(i+1),proc_lists['dec'][i]) for i in range(len(proc_lists['dec']))],schedulers.HRRN()))
		dec_errn_results.append(get_results([schedulers.ProcessEnh('P'+str(i+1),proc_lists['dec'][i]) for i in range(len(proc_lists['dec']))],schedulers.HRRN()))
		dec_errnx_results.append(get_results([err.Process('P'+str(i+1),proc_lists['dec'][i]) for i in range(len(proc_lists['dec']))],err.ERRN()))

		rand_iodtsrr_results.append(get_results([schedulers.BaseProcess('P'+str(i+1),proc_lists['rand'][i]) for i in range(len(proc_lists['rand']))],schedulers.IODTSRR()))
		rand_hrrn_results.append(get_results([schedulers.Process('P'+str(i+1),proc_lists['rand'][i]) for i in range(len(proc_lists['rand']))],schedulers.HRRN()))
		rand_errn_results.append(get_results([schedulers.ProcessEnh('P'+str(i+1),proc_lists['rand'][i]) for i in range(len(proc_lists['rand']))],schedulers.HRRN()))
		rand_errnx_results.append(get_results([err.Process('P'+str(i+1),proc_lists['rand'][i]) for i in range(len(proc_lists['rand']))],err.ERRN()))


	inc_iodtsrr_results = np.asarray(inc_iodtsrr_results)
	inc_hrrn_results =  np.asarray(inc_hrrn_results)
	inc_errn_results =  np.asarray(inc_errn_results)
	inc_errnx_results = np.asarray(inc_errnx_results)

	dec_iodtsrr_results = np.asarray(dec_iodtsrr_results)
	dec_hrrn_results =  np.asarray(dec_hrrn_results)
	dec_errn_results = np.asarray(dec_errn_results)
	dec_errnx_results = np.asarray(dec_errnx_results)

	rand_iodtsrr_results = np.asarray(rand_iodtsrr_results)
	rand_hrrn_results =  np.asarray(rand_hrrn_results)
	rand_errn_results = np.asarray(rand_errn_results)
	rand_errnx_results = np.asarray(rand_errnx_results)

	print(inc_errnx_results.shape)



	x = list(range(5,n+1,1))

	plt.title('inc/avg_turnaround')
	plt.xlabel('No of Process')
	plt.ylabel('time(secs)')
	iodtsrr, = plt.plot(x,inc_iodtsrr_results[:,0],'b')
	hrrn, = plt.plot(x,inc_hrrn_results[:,0],'g')
	errn, = plt.plot(x,inc_errn_results[:,0],'r')
	errnx, = plt.plot(x,inc_errnx_results[:,0],'c')
	plt.legend((iodtsrr,hrrn,errn,errnx),('iodtsrr','hrrn','errn','errnx'))
	#plt.plot(x,inc_iodtsrr_results[:,0],'b',x,inc_hrrn_results[:,0],'g',x,inc_errn_results[:,0],'r')
	#plt.show()
	plt.savefig(exp_name + 'inc_avg_turnaround.png')
	plt.close()

	plt.title('inc/avg_wait')
	plt.xlabel('No of Process')
	plt.ylabel('time(secs)')
	iodtsrr, = plt.plot(x,inc_iodtsrr_results[:,1],'b')
	hrrn, = plt.plot(x,inc_hrrn_results[:,1],'g')
	errn, = plt.plot(x,inc_errn_results[:,1],'r')
	errnx, = plt.plot(x,inc_errnx_results[:,1],'c')
	plt.legend((iodtsrr,hrrn,errn,errnx),('iodtsrr','hrrn','errn','errnx'))
	#plt.show()
	plt.savefig(exp_name + 'inc_avg_wait.png')
	plt.close()

	plt.title('inc/CS')
	plt.xlabel('No of Process')
	plt.ylabel('context switches')
	iodtsrr, = plt.plot(x,inc_iodtsrr_results[:,2],'b')
	hrrn, = plt.plot(x,inc_hrrn_results[:,2],'g')
	errn, = plt.plot(x,inc_errn_results[:,2],'r')
	errnx, = plt.plot(x,inc_errnx_results[:,2],'c')
	plt.legend((iodtsrr,hrrn,errn,errnx),('iodtsrr','hrrn','errn','errnx'))
	#plt.show()
	plt.savefig(exp_name + 'inc_CS.png')
	plt.close()




	plt.title('dec/avg_turnaround')
	plt.xlabel('No of Process')
	plt.ylabel('time(secs)')
	iodtsrr, = plt.plot(x,dec_iodtsrr_results[:,0],'b')
	hrrn, = plt.plot(x,dec_hrrn_results[:,0],'g')
	errn, = plt.plot(x,dec_errn_results[:,0],'r')
	errnx, = plt.plot(x,dec_errnx_results[:,0],'c')
	plt.legend((iodtsrr,hrrn,errn,errnx),('iodtsrr','hrrn','errn','errnx'))
	#plt.show()
	plt.savefig(exp_name + 'dec_avg_turnaround.png')
	plt.close()

	plt.title('dec/avg_wait')
	plt.xlabel('No of Process')
	plt.ylabel('time(secs)')
	iodtsrr, = plt.plot(x,dec_iodtsrr_results[:,1],'b')
	hrrn, = plt.plot(x,dec_hrrn_results[:,1],'g')
	errn, = plt.plot(x,dec_errn_results[:,1],'r')
	errnx, = plt.plot(x,dec_errnx_results[:,1],'c')
	plt.legend((iodtsrr,hrrn,errn,errnx),('iodtsrr','hrrn','errn','errnx'))
	#plt.show()
	plt.savefig(exp_name + 'dec_avg_wait.png')
	plt.close()

	plt.title('dec/CS')
	plt.xlabel('No of Process')
	plt.ylabel('context switches')
	iodtsrr, = plt.plot(x,dec_iodtsrr_results[:,2],'b')
	hrrn, = plt.plot(x,dec_hrrn_results[:,2],'g')
	errn, = plt.plot(x,dec_errn_results[:,2],'r')
	errnx, = plt.plot(x,dec_errnx_results[:,2],'c')
	plt.legend((iodtsrr,hrrn,errn,errnx),('iodtsrr','hrrn','errn','errnx'))
	#plt.show()
	plt.savefig(exp_name + 'dec_CS.png')
	plt.close()




	plt.title('rand/avg_turnaround')
	plt.xlabel('No of Process')
	plt.ylabel('time(secs)')
	iodtsrr, = plt.plot(x,rand_iodtsrr_results[:,0],'b')
	hrrn, = plt.plot(x,rand_hrrn_results[:,0],'g')
	errn, = plt.plot(x,rand_errn_results[:,0],'r')
	errnx, = plt.plot(x,rand_errnx_results[:,0],'c')
	plt.legend((iodtsrr,hrrn,errn,errnx),('iodtsrr','hrrn','errn','errnx'))
	#plt.show()
	plt.savefig(exp_name + 'rand_avg_turnaround.png')
	plt.close()

	plt.title('inc/avg_wait')
	plt.xlabel('No of Process')
	plt.ylabel('time(secs)')
	iodtsrr, = plt.plot(x,rand_iodtsrr_results[:,1],'b')
	hrrn, = plt.plot(x,rand_hrrn_results[:,1],'g')
	errn, = plt.plot(x,rand_errn_results[:,1],'r')
	errnx, = plt.plot(x,rand_errnx_results[:,1],'c')
	plt.legend((iodtsrr,hrrn,errn,errnx),('iodtsrr','hrrn','errn','errnx'))
	#plt.show()
	plt.savefig(exp_name + 'rand_avg_wait.png')
	plt.close()

	plt.title('inc/CS')
	plt.xlabel('No of Process')
	plt.ylabel('context switches')
	iodtsrr, = plt.plot(x,rand_iodtsrr_results[:,2],'b')
	hrrn, = plt.plot(x,rand_hrrn_results[:,2],'g')
	errn, = plt.plot(x,rand_errn_results[:,2],'r')
	errnx, = plt.plot(x,rand_errnx_results[:,2],'c')
	plt.legend((iodtsrr,hrrn,errn,errnx),('iodtsrr','hrrn','errn','errnx'))
	#plt.show()
	plt.savefig(exp_name + 'rand_CS.png')
	plt.close()



def main():
	
	graph(100,4,'data/exp1')

if __name__ == '__main__':
	main()





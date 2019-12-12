import copy
import math

class BaseProcess :

	def __init__(self,name='',burst_t = 0):
		self.name = name
		self.rbt = burst_t
		self.bt = burst_t
		self.wait_t = 0


	def res_ratio(self,len_q):
		pass

	def get_rbt(self,proc) :
		return proc.rbt

class Process(BaseProcess) :

	def res_ratio(self,len_q):
		return (self.wait_t+self.rbt)/self.rbt


class ProcessEnh(BaseProcess) :

	def res_ratio(self,len_q):		
		return (self.wait_t*math.log(len_q)+self.rbt*self.rbt)/math.log(self.rbt+1)


		

class IODTSRR :
	def __init__(self):
		self.ready_Q = []
		self.remain_Q = []


	def run(self,proc_list):
		
		self.ready_Q = copy.copy(proc_list)
		self.ready_Q.sort(key=Process().get_rbt)
		time = 0
		cs=0
		wait_t=0

		while(True):
			n=len(self.ready_Q)

			#print('n',n,'n//2',n//2,'n%2',n%2,'(n//2)-1',(n//2)-1,'n//2',n//2,'round((self.ready_Q[(n//2)-1].rbt+self.ready_Q[n//2].rbt)/2)',round((self.ready_Q[(n//2)-1].rbt+self.ready_Q[n//2].rbt)/2))

			self.qt = self.ready_Q[n//2].rbt if(n%2==1) else round((self.ready_Q[(n//2)-1].rbt+self.ready_Q[n//2].rbt)/2)

			while(self.ready_Q != []) :

				proc = self.ready_Q.pop(0)

				proc.rbt-=self.qt
				time+=self.qt

				for i in self.ready_Q:
					wait_t+=self.qt

				if(proc.rbt > self.qt) :

					self.remain_Q.append(proc)
				else :
					time+=proc.rbt
					for i in self.ready_Q:
						wait_t+=proc.rbt


				#print(time,proc.name)
				cs+=1


			if(self.remain_Q == []) :
				break

			self.ready_Q = copy.copy(self.remain_Q)
			self.ready_Q.sort(key=Process().get_rbt)
			self.remain_Q = []

		avg_wt = wait_t/len(proc_list)
		avg_turn = (wait_t+time)/len(proc_list)

		#print("avg_wt: ",avg_wt, "avg_turn: ", avg_turn,"CS: ",cs)

		return (avg_turn,avg_wt,cs)


class HRRN :

	def __init__(self):
		self.ready_Q = []

	def run(self,proc_list):
		
		self.ready_Q = 	copy.copy(proc_list)

		time=0
		wt = 0
		cs =0
		self.qt = 0
		while self.ready_Q != []:

			self.qt = round(sum(list(map(lambda x : x.rbt,self.ready_Q)))/len(self.ready_Q))

			resRat = [i.res_ratio(len(self.ready_Q)) for i in self.ready_Q]
			#print("response ratio: ",resRat)

			hrr = max(range(len(self.ready_Q)),key = lambda i :self.ready_Q[i].res_ratio(len(self.ready_Q)))

			proc = self.ready_Q.pop(hrr)
			exec_time = 0

			proc.rbt-=self.qt
			exec_time+=self.qt

			#print(list(map(lambda x: x.rbt, self.ready_Q)))

			if proc.rbt > 0 :
				for i in self.ready_Q :
					i.wait_t+=exec_time
					wt+=exec_time
				self.ready_Q.append(proc)


			else :
				exec_time+=proc.rbt

				for i in self.ready_Q :
					i.wait_t+=exec_time
					wt+=exec_time

			time+= exec_time
			cs+=1

			#print(time,proc.name,exec_time,self.qt)


		avg_wt = wt/len(proc_list)
		avg_turn = (wt+time)/len(proc_list)


		#print("avg_wt:",avg_wt,"avg_turn:",avg_turn,"CS:",cs)

		return (avg_turn,avg_wt,cs)



def main():

	RBTs = [140,75,320,280,125]
	RBTrand = [92,70,35,40,80]
	RBTasc = [30,42,50,85,97]
	RBTdesc = [80,72,65,50,43]

	scheduler = IODTSRR()
	scheduler1 = HRRN()

	print("Ascending")
	proc_list = [BaseProcess('P'+str(i+1),RBTasc[i]) for i in range(len(RBTasc))]
	proc_list1 = [Process('P'+str(i+1),RBTasc[i]) for i in range(len(RBTasc))]
	proc_list2 = [ProcessEnh('P'+str(i+1),RBTasc[i]) for i in range(len(RBTasc))]

	print("IODTSRR")
	scheduler.run(proc_list)
	print()
	print("HRRN")
	scheduler1.run(proc_list1)
	print()
	print("EHRRN")
	scheduler1.run(proc_list2)
	print()
	print()

	print("Descending")
	proc_list = [BaseProcess('P'+str(i+1),RBTdesc[i]) for i in range(len(RBTdesc))]
	proc_list1 = [Process('P'+str(i+1),RBTdesc[i]) for i in range(len(RBTdesc))]
	proc_list2 = [ProcessEnh('P'+str(i+1),RBTdesc[i]) for i in range(len(RBTdesc))]
	print("IODTSRR")
	scheduler.run(proc_list)
	print()
	print("HRRN")
	scheduler1.run(proc_list1)
	print()
	print("EHRRN")
	scheduler1.run(proc_list2)
	print()
	print()

	print("Random")
	proc_list = [BaseProcess('P'+str(i+1),RBTrand[i]) for i in range(len(RBTrand))]
	proc_list1 = [Process('P'+str(i+1),RBTrand[i]) for i in range(len(RBTrand))]
	proc_list2 = [ProcessEnh('P'+str(i+1),RBTrand[i]) for i in range(len(RBTrand))]
	print("IODTSRR")
	scheduler.run(proc_list)
	print()
	print("HRRN")
	scheduler1.run(proc_list1)
	print()
	print("EHRRN")
	scheduler1.run(proc_list2)
	print()
	print()

if __name__ == '__main__':
	main()

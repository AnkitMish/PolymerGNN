from mpi4py import MPI
import sys, os

size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()



batch = 6488

ffile = open('step_num.txt', 'r')
ffile_Br = open('Br_step_num.txt', 'r')

steps = {}
steps_Br = {}

for line in ffile.readlines():
	line = line.strip().split()
	id = int(line[0])
	step = int(line[1])
	steps[id] = step 

for line in ffile_Br.readlines():
	line = line.strip().split()
	id = int(line[0])
	step = int(line[1])
	steps_Br[id] = step 

for i in range(size):
	if rank == i:
		rank1 = rank+1+batch
		command = '/usr/bin/bash run.sh %d' %(rank1)
		os.system(command)
		"""		
		if rank1 in steps:
			os.system('rm -rf %d/ZeroE; rm -rf %d/FiniteE' %(rank1,rank1))
			os.system('cp -r 36/ZeroE %d/.' %rank1)
			os.system('cp -r 36/FiniteE %d/.' %rank1)

			os.system('mv %d/ZeroE/DAT %d/ZeroE/DAT1; rm -rf %d/ZeroE/DAT; mkdir %d/ZeroE/DAT' %(rank1, rank1, rank1, rank1))
			os.system('cp %d/DAT/%09d.bin %d/ZeroE/DAT/rxff.bin' %(rank1, steps[rank1]+100000, rank1))
			
			#os.system('mv %d/FiniteE/X/DAT %d/FiniteE/X/DAT1; rm -rf %d/FiniteE/X/DAT; mkdir %d/FiniteE/X/DAT' %(rank1, rank1, rank1, rank1))
			os.system('cp %d/DAT/%09d.bin %d/FiniteE/X/DAT/rxff.bin' %(rank1, steps[rank1]+100000, rank1))

			#os.system('mv %d/FiniteE/Y/DAT %d/FiniteE/Y/DAT1; rm -rf %d/FiniteE/Y/DAT; mkdir %d/FiniteE/Y/DAT' %(rank1, rank1, rank1, rank1))
			os.system('cp %d/DAT/%09d.bin %d/FiniteE/Y/DAT/rxff.bin' %(rank1, steps[rank1]+100000, rank1))
	
			#os.system('mv %d/FiniteE/Z/DAT %d/FiniteE/Z/DAT1; rm -rf %d/FiniteE/Z/DAT; mkdir %d/FiniteE/Z/DAT' %(rank1, rank1, rank1, rank1))		
			os.system('cp %d/DAT/%09d.bin %d/FiniteE/Z/DAT/rxff.bin' %(rank1, steps[rank1]+100000, rank1))

		if rank1 in steps_Br:
			os.system('cp ../Br/RUNS/%d/pqeq.txt %d/ZeroE/pqeq.txt' %(rank1, rank1))
			os.system('cp ../Br/RUNS/%d/ffield %d/ZeroE/ffield' %(rank1, rank1))
		
			os.system('cp ../Br/RUNS/%d/pqeq.txt %d/FiniteE/X/pqeq.txt' %(rank1, rank1))
			os.system('cp ../Br/RUNS/%d/ffield %d/FiniteE/X/ffield' %(rank1, rank1))

			os.system('cp ../Br/RUNS/%d/pqeq.txt %d/FiniteE/Y/pqeq.txt' %(rank1, rank1))
			os.system('cp ../Br/RUNS/%d/ffield %d/FiniteE/Y/ffield' %(rank1, rank1))

			os.system('cp ../Br/RUNS/%d/pqeq.txt %d/FiniteE/Z/pqeq.txt' %(rank1, rank1))
			os.system('cp ../Br/RUNS/%d/ffield %d/FiniteE/Z/ffield' %(rank1, rank1))
		"""
		

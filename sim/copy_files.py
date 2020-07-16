from mpi4py import MPI
import sys, os

rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

batch = 6400

ffile = open('step_num.txt', 'r')
ffile_Br = open('Br_step_num.txt', 'r')


steps = {}
steps_Br = {}

for line in ffile.readlines():
	line = line.strip().split()
	id = int(line[0])
	start = int(line[1])
	end = int(line[2])
	chain_length = int(line[3])
	lata, latb, latc = float(line[4]), float(line[5]), float(line[6])
	steps[id] = (start+100000, start+100500, chain_length, lata, latb, latc)

for i in range(size):

	if rank == i:
		j = i + 1 + batch
		if j in steps:

			(start, end, chain_length, lata, latb, latc) = steps[j]
			id = j
			print(j, start, end, chain_length, lata, latb, latc)
			os.system('cd %d/ZeroE; python3 dipoleMoment.py %d %d %d' %(id, start, end, chain_length))

			print('===========================================FiniteE/X================= %d ==============================================' %id)
			os.system('cd %d/FiniteE/X; python3 dipoleMoment.py %d %d %d' %(id, start, end, chain_length))

			print('===========================================FiniteE/Y================= %d ==============================================' %id)
			os.system('cd %d/FiniteE/Y; python3 dipoleMoment.py %d %d %d ' %(id, start, end, chain_length))

			print('==================================--=======FiniteE/Z================= %d ==============================================' %id)
			os.system('cd %d/FiniteE/Z; python3 dipoleMoment.py %d %d %d ' %(id, start, end, chain_length))

			print('===========================================ComputeEps================= %d ==============================================' %id)
			os.system('rm %d/out' %id)
			os.system('cd %d ; python3 computeDielectric.py %12.6f %12.6f %12.6f > out' %(id,lata, latb, latc))

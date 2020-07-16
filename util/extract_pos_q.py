import sys, os
import numpy as np
from os import path

counter = 0
tot_atoms_in_xyz_file = []

ffile = open('map_qchem_to_rxmd.txt', 'w')

with open("tot_atoms.txt", "r") as read_file:

	for line in read_file.readlines():
		line = line.strip().split()
		tot_atoms_in_xyz_file.append(int(line[1]))

for i in range(1,11110):

	if not path.exists("QCHEM/%d/POFNB.out" %i): 
		continue


	with open("QCHEM/%d/POFNB.out" %i, "r") as read_data:

		data = [line.strip() for line in read_data]	

		if '**  OPTIMIZATION CONVERGED  **' in data and 'Summary of Natural Population Analysis:' in data:

			counter += 1

			pos_counter_start = data.index('**  OPTIMIZATION CONVERGED  **') + 5
			pos_counter_end = pos_counter_start + tot_atoms_in_xyz_file[i-1] 

			q_counter_start = data.index('Summary of Natural Population Analysis:') + 6
			q_counter_end = q_counter_start + tot_atoms_in_xyz_file[i-1] 

			atoms, q = [], []

			for j in range(pos_counter_start, pos_counter_end):
				data[j] = data[j].split()
				atoms.append([data[j][1], float(data[j][2]), float(data[j][3]), float(data[j][4])])

			for j in range(q_counter_start, q_counter_end):
				q.append(float(data[j][7:16]))

			atoms = np.array(atoms)
			q = np.array(q)

			atoms_q = np.c_[atoms,q]

			assert atoms_q.shape[0] == tot_atoms_in_xyz_file[i-1], "NUmber of atoms mismatch in %d" %i

			os.system('cp QCHEM/SMILES/SMILES/smiles_%d.smi QCHEM/NEW_SMILES/smiles_%d.smi' %(i, counter))

			ffile.write('%5d	%5d\n' %(i, counter))

			with open("XYZ/%d.xyz" %counter, "w") as write_xyz:

				write_xyz.write("%d\n\n" %tot_atoms_in_xyz_file[i-1])
			
				for pos_q in atoms_q:
					write_xyz.write('%s %12.6f %12.6f %12.6f %12.6f\n' %(pos_q[0], float(pos_q[1]), float(pos_q[2]), float(pos_q[3]), float(pos_q[4])))

				print('%6d %6d   sum of charges = %3.2f' %(i, counter, np.sum(q)))

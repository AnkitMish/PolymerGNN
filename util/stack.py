import sys
import numpy as np

fileName = sys.argv[1]
writeFileDescriptor = sys.argv[2]
NumberOfRepeatUnitsInALayer = int(sys.argv[3])
DesiredTotalNumberOfAtoms = int(sys.argv[4])
mass = {"C": 12, "H": 1, "O": 16, "N": 14, "S": 32, "F": 18}
Nstacks = 0

#------------------------------ Read fileName and store the values
read_file = open(fileName, 'r')
natoms = int(read_file.readline())
read_file.readline()
positions = np.zeros((natoms,3))
atom_type = [0]*natoms
for i in range(natoms):
	line = read_file.readline()
	line = line.strip().split()
	atom_type[i] = line[0]
	x, y, z = float(line[1]), float(line[2]), float(line[3])
	positions[i][0], positions[i][1], positions[i][2] = x, y, z


#----------------- Variables for all writing out the entire stacked system --------------
NumAtomsInAStack = natoms * NumberOfRepeatUnitsInALayer * NumberOfRepeatUnitsInALayer
Nstacks = int(DesiredTotalNumberOfAtoms/NumAtomsInAStack)
stacked_positions = np.zeros((natoms*NumberOfRepeatUnitsInALayer*NumberOfRepeatUnitsInALayer*Nstacks, 3))
stacked_atom_type = [0]*natoms*NumberOfRepeatUnitsInALayer*NumberOfRepeatUnitsInALayer*Nstacks

la = np.max(positions[:,0]) - np.min(positions[:,0]) + 2.0
lb = np.max(positions[:,1]) - np.min(positions[:,1]) + 2.0
lc = np.max(positions[:,2]) - np.min(positions[:,2]) + 2.0

cell_constant = [[la,0],[lb,1],[lc,2]]
sorted_cell   = sorted(cell_constant, key = lambda x: x[0], reverse=True)
first_dir = sorted_cell[0][1]
second_dir= sorted_cell[1][1]
third_dir = sorted_cell[2][1]

cell_constant[second_dir][0] = cell_constant[first_dir][0]
# Center of the lowest stack ----------------------------------------------------------
center = [0,0,0]
center[first_dir]  = (cell_constant[first_dir][0]*NumberOfRepeatUnitsInALayer)/2.0
center[second_dir] = (cell_constant[second_dir][0]*NumberOfRepeatUnitsInALayer)/2.0
center[third_dir]  = (cell_constant[third_dir][0])/2.0
new_center = [0,0,0]
#------------- Move the positions array to origin --------------------------------------
for i in range(3): positions[:,i] -= (np.min(positions[:,i]) - 1.0)
positions[:,second_dir] += (sorted_cell[0][0] - sorted_cell[1][0])/2.0

#------------- Rotation matrix ---------------------------------------------------------
theta = [0,0,0]
theta[third_dir] = np.pi / 2.0
Rx = np.array([[1,0,0],[0,np.cos(theta[0]),-np.sin(theta[0])],[0,np.sin(theta[0]),np.cos(theta[0])]])
Ry = np.array([[np.cos(theta[1]),0,np.sin(theta[1])], [0,1,0], [-np.sin(theta[1]), 0, np.cos(theta[1])]])
Rz = np.array([[np.cos(theta[2]),-np.sin(theta[2]),0],[np.sin(theta[2]),np.cos(theta[2]),0],[0,0,1]])

R  = np.dot(np.dot(Rx,Ry),Rz)

#---------------------------------------------------------------------------------------
#----------------- Populate a single stack ---------------------------------------------
big_counter = 0
counter = 0


for i in range(Nstacks):
	for j in range(NumberOfRepeatUnitsInALayer):
		for k in range(NumberOfRepeatUnitsInALayer):
			counter = 0
			for l in range(natoms):
				stacked_positions[big_counter,first_dir] = positions[counter,first_dir] + k * cell_constant[first_dir][0]
				stacked_positions[big_counter,second_dir]= positions[counter,second_dir] + j * cell_constant[first_dir][0]
				stacked_positions[big_counter,third_dir] = positions[counter,third_dir] + i * cell_constant[third_dir][0]
				stacked_atom_type[big_counter] = atom_type[counter]
				if i % 2 == 1:
					stacked_positions[big_counter] = np.dot(R, stacked_positions[big_counter])
				#print(big_counter, Nstacks, NumberOfRepeatUnitsInALayer, natoms, Nstacks*(NumberOfRepeatUnitsInALayer^2)*natoms)
				counter += 1
				big_counter += 1
				
	new_center[0] = np.mean(stacked_positions[i*NumAtomsInAStack:(i+1)*NumAtomsInAStack,0])
	new_center[1] = np.mean(stacked_positions[i*NumAtomsInAStack:(i+1)*NumAtomsInAStack,1])
	new_center[2] = np.mean(stacked_positions[i*NumAtomsInAStack:(i+1)*NumAtomsInAStack,2])

	for m in range(3): stacked_positions[i*NumAtomsInAStack:(i+1)*NumAtomsInAStack,m] += center[m] - new_center[m]

	# Displace the cell in stacking direction to get stacked layers
	stacked_positions[i*NumAtomsInAStack:(i+1)*NumAtomsInAStack,third_dir] += i * cell_constant[third_dir][0]


#-------------- Write out the stacked coordinates ----------------------------------------
output = open('Stack_%s.xyz' %writeFileDescriptor, 'w')
output.write('%d\n' %(NumAtomsInAStack*Nstacks))
L = [0,0,0]
dL = 1.0
L[first_dir] = cell_constant[first_dir][0] * NumberOfRepeatUnitsInALayer
L[second_dir] = cell_constant[second_dir][0] * NumberOfRepeatUnitsInALayer
L[third_dir] = cell_constant[third_dir][0] * Nstacks
output.write('%12.6f %12.6f %12.6f %12.6f %12.6f %12.6f\n' %(L[0] + 2*dL,L[1] + 2*dL,L[2] + 2*dL,90.0,90.0,90.0))
total_mass = 0
for i in range(NumAtomsInAStack * Nstacks):
	total_mass += mass[stacked_atom_type[i]]
	output.write('%s  %12.6f  %12.6f  %12.6f \n' %(stacked_atom_type[i], stacked_positions[i][0] + dL, stacked_positions[i][1] + dL, stacked_positions[i][2] + dL))

density = (10^7 * total_mass)/(6.022*(L[0]+2*dL)*(L[1]+2*dL)*(L[2]+2*dL))
print('Density: %12.6f gm/cc' %density)
print('Total Atoms: %d' %(NumAtomsInAStack * Nstacks))
print('Stacking direction: %d' %third_dir)
print('Cell Constants: %12.6f %12.6f %12.6f ' %(L[0]+2*dL,L[1]+2*dL,L[2]+2*dL))

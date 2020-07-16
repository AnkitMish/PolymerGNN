from ovito.modifiers import *
from ovito.io import *
from ovito.vis import *
import os, sys
import numpy as np

#bond cutoff for all atom types
bond_cutoff = 1.6

# Reading sys.argv[1] by specifying appropriate column mapping
fname = sys.argv[1]
frames = import_file(fname, columns = ["Particle Type", "Position.X", "Position.Y", "Position.Z", "Charge", "label"], multiple_frames = False)
frames.add_to_scene()

# Setting up the active viewport
active_viewport = frames.source.dataset.viewports.active_vp
active_viewport.type = Viewport.Type.ORTHO
active_viewport.zoom_all()

frames.source.dataset.viewports.maximized_vp = frames.source.dataset.viewports.active_vp
frames.source.cell.display.enabled = False

# Some computation to get atom_types
ptp = frames.source.particle_properties.particle_type.array
ptp = frames.source.particle_properties.particle_type
particles_list = ptp.array
atom_type_map = {}

for ptype in ptp.type_list:
        atom_type_map[ptype.id] = ptype.name

atom_types = list(atom_type_map.values())

# Specifying bond cutoffs for different bonds
bonds = CreateBondsModifier()
bonds.mode = bonds.Mode.Pairwise
for i in range(len(atom_types)):
	for j in range(len(atom_types)):
		if atom_types[i] == 'H':
			if atom_types[j] != 'H':
				bonds.set_pairwise_cutoff(atom_types[i],atom_types[j],1.2)
		elif atom_types[j] == 'H':
			if atom_types[i] != 'H':
				bonds.set_pairwise_cutoff(atom_types[j],atom_types[i],1.2)
		else:
			bonds.set_pairwise_cutoff(atom_types[i],atom_types[j],bond_cutoff)

bonds.set_pairwise_cutoff('C','S', 2.0)
bonds.set_pairwise_cutoff('C','Cl', 2.0)
bonds.set_pairwise_cutoff('C','Br', 2.0)

bonds.set_pairwise_cutoff('H','H', 0.0)
frames.modifiers.append(bonds)
data = frames.compute()
frames.output.bonds.display.width = 0.10


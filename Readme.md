## Dielectric Polymer using Graph Convolution Networks

There is a great deal of interest in designing and identifying new dielectric polymer materials that exhibit high power density as they have many applications in modern electronics system. 
However, designing such polymers with desired properties is a challenging task due to combinatorial large search space. 
Polynorbornene (PNB) is one such important amorphous polymer system, which has potential applications as a high energy density polymer due to its high breakdown strength with low dielectric loss and high thermal stability. Moreover, electrical properties of PNB can be significantly enhanced by incorporation of defects or synthesis with controlled crystallinity by hydrogenation reaction, which involves experimental synthesis and characterization of combinatorial large number of polymer systems to identify potential candidates. Here, we propose a deep learning-based graph convolutional neural network (GNN) model that can identify polymer systems capable of exhibiting increased energy and power density. The GNN model is trained to predict dielectric constant for a polymer, where the training data for the high frequency dielectric constant of the PNB polymers are computed via ab-initio molecular dynamics simulation. Our model can significantly aid experimental synthesis of potentially new dielectric polymer materials which is otherwise difficult using simplistic statistical procedures.


### Workflow for dielectric constant estimation

![Workflow](https://github.com/AnkitMish/PolymerGNN/blob/master/img/Workflow.jpg)
<br>

Computational framework of polymer dielectric-behavior estimate. It can be divided into two parts (a) Synthesis of amorphous polymer system. SMILES string and Open Babel are used to create a single polymer chain. Multiple polymer chains are placed at sufficiently large distance from each chain in a simulation system. The simulation system is subjected to a number of consolidation and relaxation steps until the system reaches to a desired density.  (b) ReaxPQ+ model development that involves various QM-based calculations and validations such as atomic polarization and charges for constituent atomic species, and dielectric constant estimate.


### GNN for polymer prediction

![GNN](https://github.com/AnkitMish/PolymerGNN/blob/master/img/GNN.jpg)

The calculated dielectric constant values are used to train a Graph Neural Networks (GNN). Each Polymer is mapped to a 20 dimensional vector based on various physical and graph related property. The GNN is trained corresponding to many polymer structures and their dielectric properties. The resultant trained GNN predicts important polymers and their underlying functional group which can result in good dielectric properties.




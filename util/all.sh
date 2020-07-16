
for i in `seq 1 1 11109`; do
rm -rf $i
mkdir $i

if [ -f submit$i.sh ] ; then 
	rm submit$i.sh
fi

cat > submit$i.sh << EOF
#!/bin/bash
#SBATCH --ntasks=12 
#SBATCH --account=lc_pv
#SBATCH --partition=priya
#SBATCH --time=3:00:00
#SBATCH --job-name=$i
##SBATCH --mem-per-cpu=32gb
#SBATCH --export=none


source /usr/usc/intel/default/setup.sh
source /usr/usc/openmpi/default/setup.sh.intel

export QC=/usr/usc/qchem/5.0
export QCAUX=\$QC/qcaux
export QCPLATFORM=LINUX_Ix86_64
export QCRSH=ssh
export PATH=\$QC/bin:\$PATH
export QCSCRATCH=\$TMPDIR

ulimit -s unlimited

echo "starting simulation **************************************"
date
qchem -save -nt 12 POFNB.in POFNB.out POFNB.save
date
echo "simulation finished **************************************"
echo

EOF
echo $i
mv submit$i.sh SUBMIT/.
done

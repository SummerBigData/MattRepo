#PBS -N finalWeightsMNISTSize10000Patches15x15L0.0001B0.5Rho0.01HL100
#PBS -l walltime=03:00:00
#PBS -l nodes=1:ppn=1
#PBS -l mem=16GB
#PBS -j oe

# uncomment if using qsub
if [ -z "$PBS_O_WORKDIR" ] 
then
        echo "PBS_O_WORKDIR not defined"
else
        cd $PBS_O_WORKDIR
        echo $PBS_O_WORKDIR
fi
#
# Setup GPU code
module load python/2.7.8
#
# This is the command the runs the python script
python -u sae.py 0.0001 0.01 0.5 >& output_logs/finalWeightsMNISTSize10000Patches15x15L0.0001B0.5Rho0.01HL100.log

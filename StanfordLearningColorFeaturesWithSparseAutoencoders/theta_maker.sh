#PBS -N lcfsaeSize100000L3e-3B5Rho0.035
#PBS -l walltime=01:30:00
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
python -u lcfsae.py 30000 35 500 >& output_logs/outputLcfsaeSize100000L3e-3B5Rho0.035.log

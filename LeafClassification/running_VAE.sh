#PBS -N VAE_dim50_nn_E400
#PBS -l walltime=05:00:00
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

# Setup GPU code
# module load python/2.7.8
source activate local
# This is the command the runs the python script
python -u VAE_modified.py 0 0 400 128 >& VAE_dim50_nn_E400.log

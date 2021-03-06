#PBS -N softmaxMNISTsize60000Rho0.1Beta0.5Lamb0.000000001DiffsaeL0.03
#PBS -l walltime=01:00:00
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
python -u softmax_regression2MNIST.py 1 >& softmaxMNISTsize60000Rho0.1Beta0.5Lamb0.000000001DiffsaeL0.03.log

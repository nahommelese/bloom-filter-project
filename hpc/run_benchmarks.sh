#!/bin/bash -l

#SBATCH --job-name=bloom_filter

#SBATCH --clusters=wice

#SBATCH --partition=batch

#SBATCH --account=lp_h_ds_students

#SBATCH --output=results/data/hpc_job_output_%j.txt

#SBATCH --error=results/data/hpc_job_error_%j.txt

#SBATCH --time=00:30:00

#SBATCH --ntasks=1

#SBATCH --cpus-per-task=1

#SBATCH --mem-per-cpu=2G



module --force purge



source "$VSC_DATA/miniconda3/etc/profile.d/conda.sh"

conda activate bloom-filter-project



cd "$SLURM_SUBMIT_DIR"



set -euo pipefail



python -m pytest -q

python -m experiments.benchmark_performance

python -m experiments.experiment_false_positive_rate

python -m experiments.experiment_compression_rate

python -m experiments.experiment_hash_distribution

python -m experiments.generate_plots --prefix hpc



echo "Bloom filter benchmarks completed successfully."

#!/bin/bash
#SBATCH --job-name=bloom_filter
#SBATCH --output=results/data/hpc_job_output.txt
#SBATCH --error=results/data/hpc_job_error.txt
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G

module purge
module load Miniconda3
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate bloom-filter-project
set -euo pipefail
python -m pytest -q
python -m experiments.benchmark_performance
python -m experiments.experiment_false_positive_rate
python -m experiments.experiment_compression_rate
python -m experiments.experiment_hash_distribution
python -m experiments.generate_plots --prefix hpc
echo 'Bloom filter benchmarks completed successfully.'

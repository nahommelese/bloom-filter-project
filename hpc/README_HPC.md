# HPC instructions

The final benchmarks must be run on the HPC infrastructure.

```bash
git clone https://github.com/YOUR_USERNAME/bloom-filter-project.git
cd bloom-filter-project
module avail
module load Miniconda3
conda env create -f environment.yml
sbatch hpc/run_benchmarks.sh
squeue -u "$USER"
```

After completion, commit the authentic HPC outputs:

```bash
git add results/data/hpc_* results/figures/hpc_*
git commit -m "Add HPC benchmark outputs and figures"
git push
```

Adjust the module name if your VSC cluster uses a different Conda module.

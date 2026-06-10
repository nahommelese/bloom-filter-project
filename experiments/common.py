import random, string
from pathlib import Path
PROJECT_ROOT=Path(__file__).resolve().parents[1]
RESULTS_DATA=PROJECT_ROOT/'results'/'data'; RESULTS_FIGURES=PROJECT_ROOT/'results'/'figures'
RESULTS_DATA.mkdir(parents=True,exist_ok=True); RESULTS_FIGURES.mkdir(parents=True,exist_ok=True)
def generate_words(count, seed=42, length=16):
    rng=random.Random(seed); alphabet=string.ascii_lowercase
    return [''.join(rng.choice(alphabet) for _ in range(length)) for _ in range(count)]
def generate_dna(count, seed=42, length=60):
    rng=random.Random(seed); return [''.join(rng.choice('ACGT') for _ in range(length)) for _ in range(count)]

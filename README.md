# Bloom Filter Project

**Author:** Nahom Melese Geremw  
**Course:** Concepts of Data Science 2025–2026

## Overview

This repository contains an object-oriented Python implementation of a Bloom filter, correctness tests, hash-distribution tests for words and DNA sequences, performance benchmarks, false-positive experiments, a compression experiment, plotting utilities, and an HPC batch script.

## Basic usage

```python
from bloom_filter import BloomFilter
bloom = BloomFilter(expected_items=10_000, false_positive_rate=0.01)
bloom.add("apple")
print("apple" in bloom)
```

## Design

For expected items `n` and target false-positive rate `p`:

```text
m = ceil(-(n * ln(p)) / (ln(2)^2))
k = round((m / n) * ln(2))
h_i(x) = (h1(x) + i * h2(x)) mod m
```

## Complexity

| Operation        | Expected time |        Space |
| ---------------- | ------------: | -----------: |
| Initialisation   |        `O(m)` |  `O(m)` bits |
| Insert one item  |        `O(k)` | `O(1)` extra |
| Query one item   |        `O(k)` | `O(1)` extra |
| Insert `n` items |       `O(nk)` |  `O(m)` bits |

For a fixed target false-positive rate, `k` is approximately constant, so insertion and queries are effectively constant-time per item.

## Tests

```bash
python -m pytest -q
```

The tests cover argument validation, no false negatives, memory allocation, multiple input types, valid hash positions, and distribution checks for words and DNA strings.

## Local preview experiments

```bash
python -m experiments.benchmark_performance --sizes 1000,5000,10000 --repeats 2 --output results/data/local_preview_performance.csv
python -m experiments.experiment_false_positive_rate --expected-items 10000 --query-count 10000 --output results/data/local_preview_false_positive_rate.csv
python -m experiments.experiment_compression_rate --expected-sizes 1000,10000,100000 --output results/data/local_preview_compression_rate.csv
python -m experiments.experiment_hash_distribution --item-count 5000 --output results/data/local_preview_hash_distribution.csv
python -m experiments.generate_plots --prefix local_preview
```

## HPC benchmarks

Run authentic final benchmarks on the HPC infrastructure:

```bash
sbatch hpc/run_benchmarks.sh
```

See `hpc/README_HPC.md` for details.

## Experiments and expected interpretation

- Hash positions are tested for natural-language-like words and DNA sequences.
- Insertion and search runtime should grow approximately linearly with the number of processed items.
- False-positive rates are measured below, at, and above the designed filter capacity.
- Compression is evaluated as a function of expected item count and target false-positive rate.

## Final conclusions

The Bloom filter provides memory-efficient membership checks by accepting a controlled probability of false positives. It must show no false negatives for inserted values. Update this section with numerical observations after running the HPC benchmarks.
The HPC benchmark completed successfully. The results show that insertion and membership-query times increase as the number of processed items increases. The observed false-positive rate stays close to the target rate when the number of inserted items is near the expected capacity. When more items are inserted than the Bloom filter was designed for, the false-positive rate increases. The compression experiment shows that lower false-positive-rate targets require more memory, which reduces the compression advantage.

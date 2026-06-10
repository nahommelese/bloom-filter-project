import random
from collections import Counter
from bloom_filter import BloomFilter

def bucket_counts(values, bucket_count=50):
    bloom=BloomFilter(max(1,len(values)),0.01); c=Counter()
    for value in values:
        for pos in bloom.hash_positions(value): c[pos % bucket_count] += 1
    return [c[i] for i in range(bucket_count)]

def relative_spread(counts):
    mean=sum(counts)/len(counts); return (max(counts)-min(counts))/mean

def test_word_hash_positions_are_valid():
    bloom=BloomFilter(500,0.01)
    for word in ['apple','banana','transport','science','bloom-filter']:
        assert all(0 <= p < bloom.bit_count for p in bloom.hash_positions(word))

def test_dna_hash_positions_are_valid():
    bloom=BloomFilter(500,0.01); rng=random.Random(42)
    for _ in range(100):
        seq=''.join(rng.choice('ACGT') for _ in range(40))
        assert all(0 <= p < bloom.bit_count for p in bloom.hash_positions(seq))

def test_word_distribution_not_pathological():
    assert relative_spread(bucket_counts([f'word-{i}' for i in range(5000)])) < 0.40

def test_dna_distribution_not_pathological():
    rng=random.Random(123); vals=[''.join(rng.choice('ACGT') for _ in range(60)) for _ in range(5000)]
    assert relative_spread(bucket_counts(vals)) < 0.40

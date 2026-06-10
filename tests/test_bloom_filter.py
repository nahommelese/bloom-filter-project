import math
import pytest
from bloom_filter import BloomFilter

def test_invalid_expected_items():
    with pytest.raises(ValueError): BloomFilter(0, 0.01)
    with pytest.raises(ValueError): BloomFilter(-1, 0.01)
    with pytest.raises(TypeError): BloomFilter(100.0, 0.01)

def test_invalid_false_positive_rate():
    with pytest.raises(ValueError): BloomFilter(100, 0)
    with pytest.raises(ValueError): BloomFilter(100, 1)

def test_inserted_items_have_no_false_negatives():
    bloom=BloomFilter(1000,0.01); items=[f'word-{i}' for i in range(1000)]; bloom.update(items)
    assert all(x in bloom for x in items)

def test_contains_method_matches_operator():
    bloom=BloomFilter(10,0.05); bloom.add('apple'); assert bloom.contains('apple') and ('apple' in bloom)

def test_memory_matches_bit_count():
    bloom=BloomFilter(1000,0.01); assert bloom.memory_bytes == math.ceil(bloom.bit_count/8)

def test_fill_ratio():
    bloom=BloomFilter(100,0.01); bloom.update([f'x-{i}' for i in range(50)]); assert 0 < bloom.fill_ratio <= 1

def test_multiple_types():
    bloom=BloomFilter(10,0.01); vals=['abc', b'abc', 123, ('A',1)]; bloom.update(vals); assert all(v in bloom for v in vals)

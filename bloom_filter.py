"""Reusable Bloom filter implementation.

The implementation uses double hashing:
    h_i(x) = (h1(x) + i * h2(x)) mod m
"""
from __future__ import annotations
import hashlib
import math
from dataclasses import dataclass
from typing import Any, Iterable

@dataclass(frozen=True)
class BloomFilterParameters:
    expected_items: int
    false_positive_rate: float
    bit_count: int
    hash_count: int

class BloomFilter:
    """Space-efficient probabilistic membership data structure."""
    def __init__(self, expected_items: int, false_positive_rate: float) -> None:
        if not isinstance(expected_items, int) or isinstance(expected_items, bool):
            raise TypeError('expected_items must be an integer')
        if expected_items <= 0:
            raise ValueError('expected_items must be greater than zero')
        if not isinstance(false_positive_rate, (int, float)) or isinstance(false_positive_rate, bool):
            raise TypeError('false_positive_rate must be numeric')
        if not 0 < float(false_positive_rate) < 1:
            raise ValueError('false_positive_rate must be between 0 and 1')
        self.expected_items = expected_items
        self.false_positive_rate = float(false_positive_rate)
        self.bit_count = self.calculate_bit_count(expected_items, self.false_positive_rate)
        self.hash_count = self.calculate_hash_count(self.bit_count, expected_items)
        self._bytes = bytearray((self.bit_count + 7) // 8)
        self.items_added = 0

    @staticmethod
    def calculate_bit_count(expected_items: int, false_positive_rate: float) -> int:
        return max(1, math.ceil(-(expected_items * math.log(false_positive_rate)) / (math.log(2) ** 2)))

    @staticmethod
    def calculate_hash_count(bit_count: int, expected_items: int) -> int:
        return max(1, round((bit_count / expected_items) * math.log(2)))

    @property
    def parameters(self) -> BloomFilterParameters:
        return BloomFilterParameters(self.expected_items, self.false_positive_rate, self.bit_count, self.hash_count)

    @staticmethod
    def _normalise_item(item: Any) -> bytes:
        if isinstance(item, bytes): return item
        if isinstance(item, str): return item.encode('utf-8')
        return repr(item).encode('utf-8')

    def _hash_pair(self, item: Any) -> tuple[int, int]:
        data = self._normalise_item(item)
        h1 = int.from_bytes(hashlib.blake2b(data, digest_size=16, person=b'bloom-h1').digest(), 'big')
        h2 = int.from_bytes(hashlib.blake2b(data, digest_size=16, person=b'bloom-h2').digest(), 'big')
        return h1, h2 or 1

    def hash_positions(self, item: Any) -> tuple[int, ...]:
        h1, h2 = self._hash_pair(item)
        return tuple((h1 + i * h2) % self.bit_count for i in range(self.hash_count))

    def _set_bit(self, position: int) -> None:
        byte_index, bit_index = divmod(position, 8)
        self._bytes[byte_index] |= 1 << bit_index

    def _get_bit(self, position: int) -> bool:
        byte_index, bit_index = divmod(position, 8)
        return bool(self._bytes[byte_index] & (1 << bit_index))

    def add(self, item: Any) -> None:
        for position in self.hash_positions(item): self._set_bit(position)
        self.items_added += 1

    def update(self, items: Iterable[Any]) -> None:
        for item in items: self.add(item)

    def __contains__(self, item: Any) -> bool:
        return all(self._get_bit(position) for position in self.hash_positions(item))

    def contains(self, item: Any) -> bool:
        return item in self

    @property
    def memory_bytes(self) -> int:
        return len(self._bytes)

    @property
    def set_bit_count(self) -> int:
        return sum(byte.bit_count() for byte in self._bytes)

    @property
    def fill_ratio(self) -> float:
        return self.set_bit_count / self.bit_count

    def estimated_false_positive_rate(self, inserted_items: int | None = None) -> float:
        n = self.items_added if inserted_items is None else inserted_items
        return (1 - math.exp(-(self.hash_count * n) / self.bit_count)) ** self.hash_count

    def __len__(self) -> int:
        return self.items_added

    def __repr__(self) -> str:
        return (f'BloomFilter(expected_items={self.expected_items}, false_positive_rate={self.false_positive_rate}, '
                f'bit_count={self.bit_count}, hash_count={self.hash_count}, items_added={self.items_added})')

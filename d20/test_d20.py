import pytest
from typing import List
from math import sqrt

# Move these functions to your main solution file
def fifty_factors(n: int) -> List[int]:
    factors = []
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            if n // i <= 50:  # Check if this is within first 50 multiples of i
                factors.append(i)
            if i != n // i and n // (n // i) <= 50:  # Same check for the paired factor
                factors.append(n // i)
    return sorted(factors)

def calculate_presents(house: int) -> int:
    return 11 * sum(fifty_factors(house))

# Test cases
@pytest.mark.parametrize("house,expected_factors", [
    (1, [1]),                  # Base case: only elf 1
    (2, [1, 2]),              # Two elves
    (3, [1, 3]),              # Prime number house
    (4, [1, 2, 4]),           # Power of 2
    (6, [1, 2, 3, 6]),        # Multiple factors
])
def test_small_houses(house: int, expected_factors: List[int]):
    """Test factor calculation for small house numbers"""
    assert fifty_factors(house) == expected_factors

@pytest.mark.parametrize("house,expected_presents", [
    (1, 11),      # House 1: 11 * (1)
    (2, 33),      # House 2: 11 * (1 + 2)
    (3, 44),      # House 3: 11 * (1 + 3)
    (4, 77),      # House 4: 11 * (1 + 2 + 4)
])
def test_present_calculation(house: int, expected_presents: int):
    """Test present calculation for known cases"""
    assert calculate_presents(house) == expected_presents

def test_elf_delivery_limit():
    """Test that elves stop delivering after their 50th house"""
    # House 100 should include Elf 2 (50th house for Elf 2)
    assert 2 in fifty_factors(100)
    
    # House 102 should NOT include Elf 2 (51st house for Elf 2)
    assert 2 not in fifty_factors(102)

@pytest.mark.parametrize("house", [50, 100, 150, 200])
def test_factor_validity(house: int):
    """Test that all returned factors are valid and within 50-house limit"""
    factors = fifty_factors(house)
    for factor in factors:
        # Verify it's a real factor
        assert house % factor == 0
        # Verify it's within the 50-house limit
        assert house // factor <= 50

def test_large_numbers():
    """Test handling of larger house numbers"""
    house = 1000
    factors = fifty_factors(house)
    # Verify factors are sorted
    assert factors == sorted(factors)
    # Verify no factors exceed the house number
    assert all(f <= house for f in factors)
    # Verify 50-house limit
    assert all(house // f <= 50 for f in factors)

# Optional: Performance test
@pytest.mark.slow
def test_performance():
    """Test performance with larger numbers"""
    house = 10000
    start = pytest.importorskip("time").time()
    factors = fifty_factors(house)
    end = pytest.importorskip("time").time()
    assert end - start < 1.0  # Should complete in under 1 second
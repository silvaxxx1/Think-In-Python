#!/usr/bin/env python3
"""
julia1.py — Baseline Julia set implementation from HPP Chapter 2.

WHAT THIS SCRIPT DEMONSTRATES:
    - A CPU-bound calculation with unpredictable complexity
    - Baseline timing with print statements
    - Sanity check (assert) to catch optimization bugs

PROFILING COMMANDS TO RUN:

    1. Basic timing (baseline):
       $ python julia1.py

    2. cProfile — find which function is slow:
       $ python -m cProfile -s cumulative julia1.py

    3. Save profile data for visualization:
       $ python -m cProfile -o profile.stats julia1.py
       $ snakeviz profile.stats

    4. Line-by-line timing (requires line_profiler):
       $ kernprof -l -v julia1_lineprofiler.py  # See separate script

    5. Memory profiling (requires memory_profiler):
       $ python -m memory_profiler julia1_memoryprofiler.py  # See separate script

EXPECTED OUTPUT (on a typical laptop):
    Length of x: 1000
    Total elements: 1000000
    calculate_z_serial_purepython took ~8 seconds
"""

import time
import math

# ============================================================================
# CONSTANTS — The complex plane region we're exploring
# ============================================================================
# x1, x2: left and right boundaries of the complex plane
# y1, y2: bottom and top boundaries
# The Julia set for c = -0.62772 - 0.42193j has interesting structure
# with both quick and slow regions — perfect for profiling.
# ============================================================================
x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
c_real, c_imag = -0.62772, -0.42193


def calculate_z_serial_purepython(maxiter, zs, cs):
    """
    CPU-bound calculation — this is what we'll profile.

    For each complex coordinate z, iterates:
        z = z*z + c
    until either:
        - |z| >= 2 (escapes to infinity) OR
        - max iterations reached

    RETURNS:
        List of iteration counts per coordinate.
        White regions in the output = many iterations = expensive.
    """
    output = [0] * len(zs)   # Pre-allocate result list

    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]

        # The inner loop — this is where most CPU time is spent
        # Note: Python's dynamic dispatch means even n += 1 is expensive
        while abs(z) < 2 and n < maxiter:
            z = z * z + c
            n += 1
        output[i] = n

    return output


def calc_pure_python(desired_width, max_iterations):
    """
    Set up the problem and run the calculation.

    This function:
        1. Builds coordinate grids (x and y)
        2. Creates lists of complex numbers (zs and cs)
        3. Times the calculation
        4. Verifies correctness with assert

    The zs and cs lists are deliberately stored separately to simulate
    real-world data pipelines and to demonstrate memory profiling.
    """
    # Build coordinate grids
    x_step = (x2 - x1) / desired_width
    y_step = (y1 - y2) / desired_width

    x = []
    y = []
    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step
    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step

    # Build zs (coordinates) and cs (constant for all points)
    # Note: cs doesn't need to be a list — it's the same value repeated.
    # We keep it as a list to simulate a real-world scenario where
    # each data point might have different parameters.
    zs = []
    cs = []
    for ycoord in y:
        for xcoord in x:
            zs.append(complex(xcoord, ycoord))
            cs.append(complex(c_real, c_imag))

    print(f"Length of x: {len(x)}")
    print(f"Total elements: {len(zs)}")

    # Time the calculation
    start_time = time.time()
    output = calculate_z_serial_purepython(max_iterations, zs, cs)
    end_time = time.time()

    print(f"calculate_z_serial_purepython took {end_time - start_time:.3f} seconds")

    # Sanity check — the sum is deterministic for the given constants
    # If this assert fails, we've broken the algorithm during optimization.
    assert sum(output) == 33219980

    return output


if __name__ == "__main__":
    # Run with 1000x1000 grid (1,000,000 points) and max 300 iterations
    # This takes ~8 seconds on a modern laptop.
    calc_pure_python(desired_width=1000, max_iterations=300)

    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("  $ python -m cProfile -s cumulative julia1.py")
    print("  $ python -m cProfile -o profile.stats julia1.py && snakeviz profile.stats")
    print("=" * 60)
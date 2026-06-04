#!/usr/bin/env python3
"""
julia1_memoryprofiler.py — Julia set with @profile for memory_profiler.

WHAT THIS SCRIPT DEMONSTRATES:
    - Line-by-line memory usage
    - Memory over time with mprof
    - The overhead of storing zs and cs lists separately

PROFILING COMMANDS TO RUN:

    1. Install memory_profiler:
       $ pip install memory_profiler psutil

    2. Line-by-line memory profile:
       $ python -m memory_profiler julia1_memoryprofiler.py

    3. Memory over time (samples by time, not by line):
       $ mprof run python julia1_memoryprofiler.py
       $ mprof plot

    4. Debug OOM with pdb (drops into debugger when memory exceeds limit):
       $ python -m memory_profiler --pdb-mem=1024 julia1_memoryprofiler.py

INTERPRETING THE OUTPUT (from HPP Chapter 2, Example 2-10):

    Line #   Mem usage    Increment   Line Contents
    ==============================================
        12   133.973 MiB   7.609 MiB   output = [0] * len(zs)
        41   125.961 MiB   0.000 MiB   for ycoord in y:
        42   125.961 MiB   0.258 MiB       for xcoord in x:
        43   125.961 MiB   0.512 MiB           zs.append(complex(xcoord, ycoord))

    KEY INSIGHTS:
    - output list allocation: +7.6 MB
    - zs and cs lists: 48 MB → 125 MB (+77 MB total)
    - Not the exact sizes — just how much the process grew

    OPTIMIZATION (shown in Chapter 11):
    - Remove zs and cs lists, calculate coordinates on the fly
    - Drops RAM from 140 MB to 60 MB (Figure 2-8)
"""

import time
import math

x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
c_real, c_imag = -0.62772, -0.42193


# ============================================================================
# NO-OP @profile DECORATOR
# ============================================================================
# Same pattern as line_profiler — makes the script work everywhere.
# ============================================================================
if 'memory_profiler' not in dir() and 'profile' not in dir():
    def profile(func):
        return func


@profile
def calculate_z_serial_purepython(maxiter, zs, cs):
    """CPU-bound calculation — decorated for memory_profiler."""
    output = [0] * len(zs)   # ← Line 12: +7.6 MB

    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]

        while abs(z) < 2 and n < maxiter:
            z = z * z + c
            n += 1
        output[i] = n

    return output


@profile
def calc_pure_python(desired_width, max_iterations):
    """Set up the problem and run the calculation — decorated for memory_profiler."""
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

    # These two lists are the main memory hogs
    # Removing them (calculating coordinates on the fly) cuts RAM in half
    zs = []   # ← Line ~39: memory starts at 48 MB
    cs = []   # ← Line ~40
    for ycoord in y:          # ← Line ~41
        for xcoord in x:      # ← Line ~42
            zs.append(complex(xcoord, ycoord))   # ← +0.5 MB per iteration
            cs.append(complex(c_real, c_imag))   # ← +0.5 MB per iteration

    print(f"Length of x: {len(x)}")
    print(f"Total elements: {len(zs)}")

    start_time = time.time()
    output = calculate_z_serial_purepython(max_iterations, zs, cs)
    end_time = time.time()

    print(f"calculate_z_serial_purepython took {end_time - start_time:.3f} seconds")

    assert sum(output) == 33219980 if desired_width == 1000 else True
    return output


if __name__ == "__main__":
    # Use smaller grid for faster profiling (250x250 = 62,500 points)
    # Full 1000x1000 takes 2 hours to profile with memory_profiler!
    calc_pure_python(desired_width=250, max_iterations=300)

    print("\n" + "=" * 60)
    print("HOW TO RUN THIS SCRIPT:")
    print("  $ python -m memory_profiler julia1_memoryprofiler.py")
    print()
    print("  $ mprof run python julia1_memoryprofiler.py")
    print("  $ mprof plot")
    print()
    print("WHAT TO LOOK FOR:")
    print("  - The zs.append and cs.append lines show large Increment values")
    print("  - mprof plot shows memory over time with function entry/exit brackets")
    print("  - Peak memory happens before garbage collection (dashed vertical line)")
    print("=" * 60)
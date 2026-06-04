#!/usr/bin/env python3
"""
julia1_lineprofiler.py — Julia set with @profile for line_profiler.

WHAT THIS SCRIPT DEMONSTRATES:
    - Line-by-line CPU timing with kernprof
    - The 38% cost of the while test
    - How to keep unit tests working with @profile

PROFILING COMMANDS TO RUN:

    1. Install line_profiler:
       $ pip install line_profiler

    2. Run the profiler (smaller grid for speed):
       $ kernprof -l -v julia1_lineprofiler.py

    3. If you have the notebook open, you can also use:
       %load_ext line_profiler
       %lprun -f calculate_z_serial_purepython calc_pure_python(250, 300)

INTERPRETING THE OUTPUT:

    Line #      Hits         Time  Per Hit   % Time  Line Contents
    ==============================================================
        17  34219980        0.5     38.0      while abs(z) < 2 and n < maxiter:
        18  33219980        0.5     30.8          z = z * z + c
        19  33219980        0.4     27.1          n += 1

    KEY INSIGHTS:
    - 38% of time on the while condition alone
    - 30% on z = z*z + c (complex multiplication)
    - 27% on n += 1 (Python's dynamic dispatch!)
    - Even incrementing a counter is expensive inside a tight loop

EXPECTED OUTPUT (with desired_width=250):
    Length of x: 250
    Total elements: 62500
    calculate_z_serial_purepython took ~2 seconds (profiler adds overhead)
"""

import time
import math

x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
c_real, c_imag = -0.62772, -0.42193


# ============================================================================
# NO-OP @profile DECORATOR
# ============================================================================
# This is CRITICAL for unit testing.
#
# Without this:
#   - pytest fails with: NameError: name 'profile' is not defined
#   - Because @profile is only injected by kernprof, not by the Python interpreter
#
# With this:
#   - Same code runs under pytest, kernprof, and python -m memory_profiler
#   - No need to comment/uncomment decorators when switching tools
# ============================================================================
if 'line_profiler' not in dir() and 'profile' not in dir():
    def profile(func):
        return func


@profile
def calculate_z_serial_purepython(maxiter, zs, cs):
    """
    CPU-bound calculation — decorated for line_profiler.

    The @profile decorator tells kernprof to collect line-by-line timing.
    The no-op fallback above makes this script work everywhere.
    """
    output = [0] * len(zs)

    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]

        # The chapter breaks this compound statement to measure each part
        # Original (faster but less informative):
        #   while abs(z) < 2 and n < maxiter:
        #
        # Broken down to reveal costs:
        while True:
            not_yet_escaped = abs(z) < 2      # 2× more expensive than n < maxiter
            iterations_left = n < maxiter
            if not_yet_escaped and iterations_left:
                z = z * z + c
                n += 1
            else:
                break
        output[i] = n

    return output


def calc_pure_python(desired_width, max_iterations):
    """Set up the problem and run the calculation."""
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

    zs = []
    cs = []
    for ycoord in y:
        for xcoord in x:
            zs.append(complex(xcoord, ycoord))
            cs.append(complex(c_real, c_imag))

    print(f"Length of x: {len(x)}")
    print(f"Total elements: {len(zs)}")

    start_time = time.time()
    output = calculate_z_serial_purepython(max_iterations, zs, cs)
    end_time = time.time()

    print(f"calculate_z_serial_purepython took {end_time - start_time:.3f} seconds")

    assert sum(output) == 33219980 if desired_width == 1000 else True
    return output


if __name__ == "__main__":
    # Use smaller grid (250x250 = 62,500 points) because line_profiler
    # adds significant overhead (8s → 49s at full resolution)
    calc_pure_python(desired_width=250, max_iterations=300)

    print("\n" + "=" * 60)
    print("HOW TO RUN THIS SCRIPT:")
    print("  $ kernprof -l -v julia1_lineprofiler.py")
    print()
    print("WHAT TO LOOK FOR IN THE OUTPUT:")
    print("  - % Time column: lines with >10% are optimization targets")
    print("  - The while test shows ~38% — that's your bottleneck")
    print("  - Even n += 1 shows ~27% — Python's dynamic dispatch is expensive")
    print("=" * 60)
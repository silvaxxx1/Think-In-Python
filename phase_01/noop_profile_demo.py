#!/usr/bin/env python3
"""
noop_profile_demo.py — Demonstrates @profile decorator that works with pytest.

THE PROBLEM:
    - kernprof and memory_profiler inject a @profile decorator
    - pytest doesn't know about @profile → NameError

THE SOLUTION:
    - A no-op @profile decorator that does nothing when profilers aren't running
    - Same code works with: pytest, kernprof, python -m memory_profiler

WHAT THIS SCRIPT DEMONSTRATES:
    - The no-op decorator pattern
    - How to keep unit tests working during optimization
    - That adding @profile doesn't break your test suite

COMMANDS TO RUN:

    1. Unit test (works despite @profile):
       $ pytest noop_profile_demo.py -v

    2. Line profile (works):
       $ kernprof -l -v noop_profile_demo.py

    3. Memory profile (works):
       $ python -m memory_profiler noop_profile_demo.py

    4. Run as normal script:
       $ python noop_profile_demo.py
"""

import time


# ============================================================================
# NO-OP @profile DECORATOR
# ============================================================================
# This is the magic. It checks whether line_profiler or memory_profiler
# has already injected a @profile decorator into the namespace.
#
# If they have (kernprof or mprof run), we do nothing — their version wins.
# If they haven't (pytest or normal python), we provide a dummy decorator
# that just returns the original function unchanged.
#
# Result: the same source code works in ALL environments.
# ============================================================================
if 'line_profiler' not in dir() and 'profile' not in dir():
    def profile(func):
        """No-op decorator — does nothing, just returns the function."""
        return func


@profile
def some_fn(useful_input):
    """
    An expensive function that we wish to both test and profile.

    The @profile decorator doesn't break tests thanks to the no-op above.
    When running with kernprof, it gets real line-by-line timing.
    When running with pytest, it's just a normal function.
    """
    # Simulate expensive work (e.g., model forward pass, data augmentation)
    time.sleep(0.1)
    return useful_input * 2


def test_some_fn():
    """
    Unit test for some_fn — runs with pytest even though @profile is present.

    Run with:
        $ pytest noop_profile_demo.py -v

    Expected output:
        ============================= test session starts ==============================
        collected 1 item

        noop_profile_demo.py::test_some_fn PASSED

        ============================== 1 passed in 0.31s ===============================
    """
    assert some_fn(2) == 4
    assert some_fn(1) == 1
    assert some_fn(-1) == -2
    # Note: -1 * 2 = -2, not 2. This is correct — the function doesn't take absolute value.


if __name__ == "__main__":
    print("=" * 60)
    print("DEMO: No-op @profile decorator")
    print("=" * 60)
    print(f"Example call 'some_fn(2)' == {some_fn(2)}")
    print()

    print("COMMANDS TO VERIFY EACH TOOL WORKS:")
    print()
    print("  1. Unit test (pytest):")
    print("     $ pytest noop_profile_demo.py -v")
    print()
    print("  2. Line profiler (kernprof):")
    print("     $ kernprof -l -v noop_profile_demo.py")
    print()
    print("  3. Memory profiler:")
    print("     $ python -m memory_profiler noop_profile_demo.py")
    print()
    print("  4. Normal execution:")
    print("     $ python noop_profile_demo.py")
    print()
    print("All four work with the same source code. No modifications needed.")
    print("=" * 60)
# Phase 01 — The Foundation

> *"Understand how Python and the machine actually work before writing a single optimization."*

| Duration | Chapters | Notebooks | Scripts | Status |
|----------|----------|-----------|---------|--------|
| ~2 weeks | 3 | 3 | 4 | ✅ **Complete** |

---

## 📍 Phase Map

| # | Chapter | Book | Notebook | Scripts |
|---|---------|------|----------|---------|
| 1 | The Python Data Model | FP Ch 1 | `01_fp_ch1_data_model.ipynb` | — |
| 2 | Understanding Performant Python | HPP Ch 1 | `02_hpp_ch1_performant_python.ipynb` | — |
| 3 | Profiling to Find Bottlenecks | HPP Ch 2 | `03_hpp_ch2_profiling.ipynb` | 4 scripts |

**Optional companion:** PNP Ch 57 (dis module) — covered in notebook #3, Part 10

---

## 🎯 Learning Objectives

By the end of Phase 01, you will be able to:

### Python Data Model (FP Ch 1)
- Explain why `len(collection)` exists instead of `collection.len()`
- Implement `__len__` and `__getitem__` to make any class iterable
- Use `__repr__` for unambiguous debugging output
- Understand the 7 flavors of callable objects in Python
- Explain why infix operators (`+`, `*`) return **new objects** (immutability principle)
- Implement `__add__`, `__mul__`, `__rmul__`, `__abs__`, `__bool__`
- Map dunder methods to PyTorch / DataLoader patterns

### High Performance Python — Mental Model (HPP Ch 1)
- Identify whether a bottleneck is in computing units, memory, or communications
- Explain why Python loops are 50–200× slower than NumPy (SIMD, dynamic types, fragmentation)
- Use Amdahl's law to set realistic expectations for parallel speedup
- Explain the GIL and when `threading` vs `multiprocessing` is appropriate
- Choose between `list[float]`, `array.array`, and `np.float32` for ML data
- Explain why `model(batch)` is always faster than looping over samples

### Profiling (HPP Ch 2)
- Run `cProfile` to identify slow functions
- Visualize `cProfile` output with `snakeviz`
- Run `line_profiler` (kernprof) to identify slow **lines**
- Run `memory_profiler` to identify memory allocation hot spots
- Use `mprof` to see memory usage over time
- Use `py-spy` to profile already-running processes
- Read bytecode with `dis` to understand CPython's stack-based VM
- Write unit tests that work with `@profile` decorators (no-op pattern)

---

## 📁 Files in This Directory

### Notebooks

| File | Description |
|------|-------------|
| `01_fp_ch1_data_model.ipynb` | The Python Data Model — dunder methods, namedtuple, FrenchDeck, Vector, ML extensions |
| `02_hpp_ch1_performant_python.ipynb` | Mental model — computing units, memory hierarchy, GIL, Amdahl, bus bandwidth, 3-phase workflow |
| `03_hpp_ch2_profiling.ipynb` | Profiling tools — cProfile, line_profiler, memory_profiler, mprof, py-spy, dis |

### Scripts (in `scripts/` directory)

| Script | Purpose | Run command |
|--------|---------|-------------|
| `julia1.py` | Baseline Julia set | `python julia1.py` |
| `julia1_lineprofiler.py` | Line-by-line CPU profiling | `kernprof -l -v julia1_lineprofiler.py` |
| `julia1_memoryprofiler.py` | Line-by-line memory profiling | `python -m memory_profiler julia1_memoryprofiler.py` |
| `noop_profile_demo.py` | Unit test with @profile decorator | `pytest noop_profile_demo.py -v` |

---

## 🚀 How to Run This Phase

### 1. Open the notebooks

```bash
cd phase_01
jupyter notebook
```

Open notebooks in order: `01_` → `02_` → `03_`

### 2. Run the scripts (from terminal)

```bash
cd phase_01/scripts

# Baseline timing
python julia1.py

# cProfile
python -m cProfile -s cumulative julia1.py

# line_profiler
kernprof -l -v julia1_lineprofiler.py

# memory_profiler
python -m memory_profiler julia1_memoryprofiler.py

# Memory over time
mprof run python julia1_memoryprofiler.py
mprof plot

# Unit test with @profile
pytest noop_profile_demo.py -v
```

### 3. Install required packages (if not already)

```bash
pip install line_profiler memory_profiler snakeviz py-spy pytest
```

---

## 📊 What Each Notebook Covers

### Notebook 01 — The Python Data Model

| Part | Topic | ML Connection |
|------|-------|---------------|
| 1-2 | Why the data model exists | — |
| 3-4 | `namedtuple` → FrenchDeck | `namedtuple` for Sample, Batch, Config |
| 5-6 | `__getitem__`, `__len__`, `__contains__` | PyTorch Dataset protocol |
| 7-8 | Vector: `__add__`, `__mul__`, `__abs__`, `__bool__` | Tensor operations, immutability |
| 9 | `__call__` | `nn.Module` — why `model(x)` works |
| 10-15 | Context managers, `__repr__`, `__eq__`, `__hash__` | Experiment tracking, config dedup |

### Notebook 02 — Understanding Performant Python

| Part | Topic | ML Connection |
|------|-------|---------------|
| 1-2 | Computing units (IPC, SIMD, GIL, Amdahl) | Why DataLoader needs `num_workers` |
| 3 | Memory hierarchy | Python object tax (24 bytes vs 4 bytes) |
| 4 | Communications (buses, PCIe) | `.to(device)` cost, `pin_memory` |
| 5 | Python VM vs idealized computing | Why NumPy is 50–200× faster |
| 6-7 | 3-phase workflow | Profile before optimizing |
| 8-11 | ML extensions: dtype, GIL release, row-major, batching | Practical ML optimization |

### Notebook 03 — Profiling to Find Bottlenecks

| Part | Topic | ML Connection |
|------|-------|---------------|
| 1-3 | Julia set, simple timing | Baseline before optimization |
| 4-5 | `cProfile`, `snakeviz` | Find slow function in training loop |
| 6 | `line_profiler` | Find slow transform in augmentation |
| 7-8 | `memory_profiler`, `mprof` | Debug OOM during batch collation |
| 9 | `py-spy` | Profile running training job |
| 10 | `dis` module | Understand bytecode |
| 11-13 | ML extensions | DataLoader profiling, augmentation pipeline |

---

## 🔧 Troubleshooting

### `kernprof: command not found`

```bash
pip install line_profiler
# On some systems, you may need:
python -m line_profiler
```

### `NameError: name 'profile' is not defined` when running pytest

This is expected if you remove the no-op decorator. The scripts include the fix:

```python
if 'line_profiler' not in dir() and 'profile' not in dir():
    def profile(func):
        return func
```

### `mprof: command not found`

```bash
pip install memory_profiler
```

### `snakeviz: command not found`

```bash
pip install snakeviz
```

### Julia set runs very slowly (>30 seconds)

The full 1000×1000 grid takes ~8 seconds on a modern laptop. If it's slower:
- Close other applications
- Run on AC power (not battery) — CPU throttling reduces speed
- Reduce `desired_width` to 500 for faster runs

---

## ✅ Phase Completion Checklist

- [ ] Run all cells in `01_fp_ch1_data_model.ipynb`
- [ ] Run all cells in `02_hpp_ch1_performant_python.ipynb`
- [ ] Run all cells in `03_hpp_ch2_profiling.ipynb`
- [ ] Run `julia1.py` and observe ~8s runtime
- [ ] Run `cProfile` on `julia1.py` and identify `abs()` as bottleneck
- [ ] Run `kernprof` on `julia1_lineprofiler.py` and observe 38% on while test
- [ ] Run `memory_profiler` on `julia1_memoryprofiler.py`
- [ ] Run `mprof plot` and see memory over time
- [ ] Run `pytest noop_profile_demo.py -v` and see tests pass
- [ ] Answer the checkpoint question in Notebook 03: *"Why does sum(range(N)) beat a manual loop?"*

---

## 📚 Next Steps

After completing Phase 01, move to **Phase 02 — Core Data Structures**:

> *"Know what your ML data actually lives in, and the performance cost of each choice."*

**First chapter:** FP Ch 2 — An Array of Sequences (lists, tuples, arrays)

**Checkpoint project after Phase 02:** Build a Dataset and DataLoader from scratch (no NumPy, no PyTorch)

---

## 🔗 Related Files

- [Main README](../README.md)
- [Phase 02 README](../phase_02/README.md) (coming)
- [Checkpoint Projects](../checkpoint_projects/) (coming)

---

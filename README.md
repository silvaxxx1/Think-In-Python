## File 1: `README.md` — Main Repository Root

```markdown
# Python Mastery Hub

[![Phase 01 Complete](https://img.shields.io/badge/Phase_01-Complete-brightgreen)](./phase_01/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **From ML engineer to production Python.**  
> A 16-week, project-based curriculum covering the Python data model, high-performance computing, data structures, iterators, classes, concurrency, and async — all with direct ML/DL applications.

---

## 📍 Phase Status

| Phase | Title | Status | Checkpoint | Notebooks | Scripts |
|-------|-------|--------|------------|-----------|---------|
| **01** | The Foundation | ✅ **Complete** | — | 3 | 4 |
| **02** | Core Data Structures | ⬜ Planned | Dataset + DataLoader | 7 | — |
| **03** | Functions, Types & Decorators | ⬜ Planned | — | 3 | — |
| **04** | Iterators, NumPy & Compilation | ⬜ Planned | NumPy trainer + Numba | 5 | — |
| **05** | Classes & Protocols | ⬜ Planned | Tiny nn.Module API | 5 | — |
| **T** | Testing & Debugging | ⬜ Planned | — | (off-book) | — |
| **06** | Concurrency & Async | ⬜ Planned | FastAPI + process pool | 5 | — |

---

## 🎯 What This Repo Is

A **working reference** — not just notes, not just book summaries. Every concept is:

- **Explained** — with the book's original examples and terminology
- **Coded** — runnable notebooks and scripts you can execute
- **Extended** — each Python concept mapped directly to ML/DL (PyTorch, DataLoader, tensors, configs, context managers, profiling)

**The audience:** ML engineers with solid Python basics who want to write production-grade code — efficient, testable, maintainable, and Pythonic.

**The source material:**
- *Fluent Python*, 1st ed. (Ramalho, O'Reilly 2015)
- *High Performance Python*, 2nd ed. (Gorelick & Ozsvald, O'Reilly 2020)
- *Python Notes for Professionals* (GoalKicker)

---

## 📁 Repository Structure

```
python-mastery-hub/
│
├── README.md                      # This file
│
├── phase_01/                      # ✅ COMPLETE
│   ├── README.md                  # Phase 01 overview (see below)
│   ├── 01_fp_ch1_data_model.ipynb
│   ├── 02_hpp_ch1_performant_python.ipynb
│   ├── 03_hpp_ch2_profiling.ipynb
│   │
│   └── scripts/                   # Companion scripts for profiling
│       ├── julia1.py
│       ├── julia1_lineprofiler.py
│       ├── julia1_memoryprofiler.py
│       └── noop_profile_demo.py
│
├── phase_02/                      # ⬜ Coming
├── phase_03/                      # ⬜ Coming
├── phase_04/                      # ⬜ Coming
├── phase_05/                      # ⬜ Coming
├── phase_t/                       # ⬜ Coming
├── phase_06/                      # ⬜ Coming
│
└── checkpoint_projects/           # ⬜ Coming
    ├── 01_dataset_dataloader/
    ├── 02_numpy_trainer/
    ├── 03_tiny_nn_module/
    └── 04_fastapi_inference/
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/python-mastery-hub.git
cd python-mastery-hub
```

### 2. Set up a virtual environment

```bash
# Using uv (recommended — fast)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Or using venv
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Launch Jupyter

```bash
jupyter notebook
# or
jupyter lab
```

### 4. Start with Phase 01

Open `phase_01/01_fp_ch1_data_model.ipynb`

---

## 📦 Dependencies

```txt
# requirements.txt
jupyter>=1.0.0
numpy>=1.24.0
matplotlib>=3.7.0
pytest>=7.0.0

# Profiling tools (optional but recommended)
line_profiler>=4.0.0
memory_profiler>=0.61.0
snakeviz>=2.2.0
py-spy>=0.3.0

# ML libraries (for extension sections)
torch>=2.0.0
scikit-learn>=1.3.0
```

Install all at once:

```bash
pip install -r requirements.txt
```

---

## 📖 How to Use This Repo

### For Self-Study

1. **Read the book chapter first** — these notebooks are references, not replacements
2. **Open the notebook** — read the markdown explanations
3. **Run every code cell** — break things, modify parameters, see what changes
4. **Run the companion scripts** — especially for profiling (terminal commands)
5. **Do the checkpoint projects** — they separate "read a book" from "can ship"

### For Teaching / Workshops

- Each notebook is **standalone** — you can assign individual phases
- The **ML Extension sections** are clearly separated from Python foundation
- **Companion scripts** include detailed comments and run instructions

---

## 🧪 Running the Companion Scripts

Phase 01 includes 4 profiling scripts. From the `phase_01/scripts/` directory:

```bash
# Baseline
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

# Unit test with @profile decorator
pytest noop_profile_demo.py -v
```

---

## ✅ Checkpoint Projects

| # | Project | Deliverable | Phase |
|---|---------|-------------|-------|
| 1 | Dataset + DataLoader from scratch | Module + 5 tests + README | 02 |
| 2 | NumPy minibatch trainer + Numba speedup | Notebook with 3 timings | 04 |
| 3 | Tiny nn.Module-style API | ~150 LOC framework + training script | 05 |
| 4 | FastAPI inference endpoint with warm pool | API + load test results | 06 |

---

## 📚 Book Edition Notes

This repo uses **Fluent Python 1st edition** (2015). Three 2nd-edition chapters are absent from the PDF and have substitutes:

| Missing 2nd-ed chapter | Substitute |
|------------------------|-------------|
| Ch 5 — Data Class Builders | Python `dataclasses` docs |
| Ch 8 — Type Hints | PNP Ch 87 + `mypy` docs |
| Ch 15 — More Type Hints | PNP Ch 87 + `typing` docs |

Chapter number mapping is provided inside each notebook.

---

## 🤝 Contributing

This is a personal learning repository, but issues and suggestions are welcome.

- **Found an error?** Open an issue
- **Have a better ML extension example?** Submit a PR
- **Script not working on your OS?** Let me know

---

## 📄 License

MIT — use freely, attribution appreciated.

---

## 🙏 Acknowledgments

- **Luciano Ramalho** — *Fluent Python* (the data model changed how I think about Python)
- **Micha Gorelick & Ian Ozsvald** — *High Performance Python* (profiling first, always)
- **GoalKicker** — *Python Notes for Professionals* (quick reference)
- **The Python community** — for building tools that make this kind of learning possible

---

## 📬 Contact

For questions about this repository:

- Open an issue on GitHub
- Or reach out directly (add your contact info here)

---

**Start with Phase 01 → [`phase_01/README.md`](./phase_01/README.md)**
```

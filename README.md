# A Mechanism-Informed Gene Signature for Regenerative vs. Fibrotic Tendon Healing 

Sunnybrook Research Institute × University of Guelph (MBINF)

Student: Fangyi Li

Supervisor: Dr. Wilder Scott


## Progress so far

Check for [current progress](docs/progress.md)


## Reproducing the environment

The environment specification lives in [`environments/`](environments/).

To recreate the analysis environment (Python 3.14.5) and run the notebooks:

```bash
python -m venv .venv
.venv\Scripts\activate                        # Windows
# source .venv/bin/activate                   # macOS / Linux
pip install -r environments/analysis.txt
jupyter lab
```

The work used three separate environments — the analysis notebooks, the poster
build, and the pySCENIC step on Alliance Canada. All three are documented in
[`environments/README.md`](environments/README.md), along with the non-Python
dependencies (Cell Ranger, the mm10 reference, and the cisTarget databases).
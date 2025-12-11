# IPL Analytics Project

This repository contains data processing, feature engineering, analysis notebooks, and models for IPL analytics. Follow the steps below to clone the repo, create a Python environment, install dependencies, and run the notebooks to reproduce outputs.

## Prerequisites
- Linux or WSL on Windows with bash shell
- Python 3.10 or newer
- Git
- VS Code with the Python and Jupyter extensions (recommended)

## Clone the Repository
```bash
git clone https://github.com/PrajwalpGM256/ipl.git
cd ipl
```

If you already have the project folder open in VS Code, ensure your terminal path is the repo root (the directory containing `data/`, `src/`, `notebooks/`).

## Create a Python Environment
You can use `venv` (built-in) or `conda`. Choose one.

### Option A: Using venv (recommended for simplicity)
```bash
# From the repo root
python3 -m venv .venv
source .venv/bin/activate

# Verify Python and pip
python --version
pip --version
```

To deactivate later:
```bash
deactivate
```

### Option B: Using Conda
```bash
conda create -n ipl-analysis python=3.10 -y
conda activate ipl-analysis
```

## Install Dependencies
If a `requirements.txt` exists, use it. If not, install the common packages used by the notebooks.

### Using requirements.txt (preferred)
```bash
pip install -r requirements.txt
```

### If requirements.txt is missing
Install typical dependencies for data analysis and plotting:
```bash
pip install pandas numpy matplotlib seaborn plotly scikit-learn jupyter ipykernel tqdm
```

Register the environment as a Jupyter kernel (helps VS Code/Jupyter find it):
```bash
python -m ipykernel install --user --name "ipl-env" --display-name "Python (ipl-env)"
```

## Project Structure
- `data/raw/`: Original datasets (`matches.csv`, `deliveries.csv`)
- `data/processed/`: Cleaned and engineered datasets used by notebooks
- `notebooks/`: Step-by-step notebooks from exploration to modeling
- `src/`: Python modules for reusable processing and analysis
- `models/`, `results/`, `reports/`: Outputs, figures, and artifacts

## Running the Notebooks
You can run notebooks in VS Code or with Jupyter.

### In VS Code
1. Open the repo folder in VS Code.
2. Ensure your environment is active in the VS Code terminal: `source .venv/bin/activate` or `conda activate ipl-analysis`.
3. Open a notebook under `notebooks/` (e.g., `01_Data_exploration.ipynb`).
4. In the top-right kernel picker, select the kernel that matches your env (e.g., `Python (ipl-env)` or `.venv`).
5. Run cells sequentially or use “Run All”.

### Using Jupyter CLI
```bash
# With env activated
jupyter notebook
# or
jupyter lab
```
Open the desired notebook from the `notebooks/` folder and run cells.

## Data Availability
The notebooks expect the following files to be present:
- `data/raw/matches.csv`
- `data/raw/deliveries.csv`

Processed files are generated into `data/processed/` by the cleaning and feature engineering notebooks. Ensure paths in notebooks and `src/` scripts point to the `data/` directory relative to repo root.

## Reproducing End-to-End Outputs
Run the notebooks in this order:
1. `01_Data_exploration.ipynb`
2. `02_Data_Cleaning.ipynb`
3. `03_DA_season_analysis.ipynb` and `03_DA_H2H_analysis.ipynb`
4. `04_Feature_Engineering.ipynb`
5. `05_Player_clustering.ipynb`
6. `06_Match_winner_prediction.ipynb`
7. `07_Score_prediction.ipynb`

This sequence will populate `data/processed/`, generate figures under `reports/figures/`, and produce results under `results/` where applicable.

## Troubleshooting
- Kernel not found: Re-run `python -m ipykernel install ...` and pick the correct kernel in VS Code.
- Permission errors on Jupyter kernel install: Add `--user` or run from an environment where you have write access.
- Missing packages: Run `pip install -r requirements.txt` again, or install the specific missing package.
- Path issues: Run notebooks from the repo root; avoid moving the `data/` folders.

## Notes
- Use bash commands as shown above (Linux/WSL).
- If you use Windows PowerShell/CMD, adapt `source .venv/bin/activate` to `.venv\Scripts\activate`.

# (m,k)-firm Scheduling addition into SimSo

The idea of this project is to:
1. Simulate (m,k)-firm RMS, (m,k)-firm EDF, and (m,k)-firm EDF with DBP (Distance-based Priority) using [SimSo](https://github.com/MaximeCheramy/simso) simulation framework.
2. Once I have shown it works, submit a PR for SimSo to add it into the framework for future people to use.

# After cloning
1. This repo uses submodules, run this after cloning: `git submodule update --init --recursive`
2. Install required packages: `pip install -r requirements.txt`, I recommend using a venv, just cus.

# How to run?
### In command line:
1. To run EDF run: `python edf_runner.py`
2. To run (m,k)-firm DBP run: `python mk_dbp_runner.py`
3. To run (m,k)-firm EDF run: `python mk_edf_runner.py`
4. To run (m,k)-firm RMS run: `python mk_rms_runner.py`
5. To run RMS run: `python rms_runner.py`

### In VSCode:
1. Make sure you have the Python extension installed.
2. The stuff in `.vscode` should let you debug the code and link to the `simso` submodule properly.

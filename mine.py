import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# Point Python to the *repo root* that contains simso/
sys.path.insert(0, str(ROOT / "simso"))

from simso.core import Model
from simso.configuration import Configuration

# Build configuration in code
cfg = Configuration()
# Sim duration: 500 ms
cfg.duration = 1000 * cfg.cycles_per_ms

# One CPU
cfg.add_processor(name="CPU 1",
                  identifier=1,
                  cs_overhead=0,
                  cl_overhead=0,
                  migration_overhead=0,
                  speed=1.0)

# Task set, below task set is 100% utilization
cfg.add_task(name="T1", identifier=1, period=20, wcet=5, deadline=20, m=1, k=1)       # 25%, period, deadline unit in ms
cfg.add_task(name="T2", identifier=2, period=50, wcet=10, deadline=50, m=1, k=1)      # 20%
cfg.add_task(name="T3", identifier=3, period=100, wcet=15, deadline=100, m=1, k=1)    # 15%
cfg.add_task(name="T4", identifier=4, period=10, wcet=2, deadline=10, m=1, k=1)       # 20%
cfg.add_task(name="T5", identifier=5, period=30, wcet=6, deadline=30, m=1, k=1)       # 20%

# Use the built-in uniprocessor EDF
cfg.scheduler_info.clas = "simso.schedulers.EDF"
# cfg.scheduler_info.clas = "simso.schedulers.RM"
# cfg.scheduler_info.clas = "simso.schedulers.FP"
# cfg.scheduler_info.clas = "simso.schedulers.LLF"

cfg.check_all()     # Sanity-check config
model = Model(cfg)  # Build model
model.run_model()   # Run model

# Quick report
misses = []
for task in model.results.tasks.values():
    for job in task.jobs:
        if job.exceeded_deadline:
            misses.append((job.name, job.absolute_deadline))

print("Missed deadlines:", misses if misses else "None")
for task in model.results.tasks.values():
    print(f"{task.name}: preemptions={task.preemption_count}, jobs={len(task.jobs)}")

# TODO deadline miss ratio
# performance overhead
# fraction of windows that satisfy (mk) time
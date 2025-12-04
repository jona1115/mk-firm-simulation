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
cfg.duration = 500 * cfg.cycles_per_ms
# cfg.duration = 1000000 * cfg.cycles_per_ms
cfg.duration = 35 * cfg.cycles_per_ms

# One CPU
cfg.add_processor(name="CPU 1",
                  identifier=1,
                  cs_overhead=0,
                  cl_overhead=0,
                  migration_overhead=0,
                  speed=1.0)

# Task set 1, below task set is 100% utilization
# cfg.add_task(name="T1", identifier=1, period=20, wcet=5, deadline=20, m=5, k=5)       # 25%, period, deadline unit in ms
# cfg.add_task(name="T2", identifier=2, period=50, wcet=10, deadline=50, m=9, k=9)      # 20%
# cfg.add_task(name="T3", identifier=3, period=100, wcet=15, deadline=100, m=4, k=4)    # 15%
# cfg.add_task(name="T4", identifier=4, period=10, wcet=2, deadline=10, m=3, k=3)       # 20%
# cfg.add_task(name="T5", identifier=5, period=30, wcet=6, deadline=30, m=3, k=3)       # 20%

# Task set 2, this is from homework 3' QC 2b
cfg.add_task(name="T1", identifier=1, period=4, wcet=1, deadline=4, m=3, k=3)
cfg.add_task(name="T2", identifier=2, period=6, wcet=3, deadline=6, m=2, k=2)
cfg.add_task(name="T3", identifier=3, period=9, wcet=3, deadline=9, m=3, k=3)


# Use the built-in uniprocessor EDF
cfg.scheduler_info.clas = "simso.schedulers.MK_RMS"

cfg.check_all()     # Sanity-check config
model = Model(cfg)  # Build model
model.run_model()   # Run model

# print("Logs: ")
# for m in model.logs:
#     print(f"{m}")

# Quick report
misses = []
miss_count = 0
for task in model.results.tasks.values():
    for job in task.jobs:
        if job.exceeded_deadline:
            misses.append((job.name, job.absolute_deadline))
            miss_count += 1

print(f"Total missed: {miss_count}")
print("Missed deadlines:", misses if misses else "None")

print("Task Report:")
for task in model.results.tasks.values():
    print(f"  {task.name}: preemptions={task.preemption_count}, jobs={len(task.jobs)}")

total_jobs = sum(len(task.jobs) for task in model.results.tasks.values())
miss_ratio = miss_count / total_jobs if total_jobs else 0.0
print(f"Deadline miss ratio: {miss_ratio:.4f}")

scheduler = model.results.scheduler
sched_overhead = (scheduler.schedule_overhead +
                  scheduler.activate_overhead +
                  scheduler.terminate_overhead)
proc_overhead = sum(proc.context_save_overhead + proc.context_load_overhead
                    for proc in model.results.processors.values())
total_overhead = sched_overhead + proc_overhead
duration = cfg.duration or 1  # cfg.duration already in cycles
overhead_ratio = total_overhead / duration
overhead_ms = total_overhead / cfg.cycles_per_ms
print("Overhead report:")
print(f"  Scheduler overhead (cycles): {sched_overhead}")
print(f"  Processor overhead (cycles): {proc_overhead}")
print(f"  Total overhead: {total_overhead} cycles ({overhead_ms:.3f} ms)")
print(f"  Overhead ratio: {overhead_ratio:.6f}")

mk_windows = 0
mk_windows_satisfied = 0
for task in model.results.tasks.values():
    task_obj = getattr(task, "task", None)
    task_info = getattr(task_obj, "_task_info", None)
    if task_info is None:
        continue
    m = getattr(task_info, "m", 0)
    k = getattr(task_info, "k", 0)
    jobs = task.jobs
    if not k or len(jobs) < k:
        continue

    window_successes = sum(0 if job.exceeded_deadline else 1
                           for job in jobs[:k])
    total_windows = len(jobs) - k + 1
    mk_windows += total_windows
    if window_successes >= m:
        mk_windows_satisfied += 1

    for idx in range(k, len(jobs)):
        if not jobs[idx].exceeded_deadline:
            window_successes += 1
        if not jobs[idx - k].exceeded_deadline:
            window_successes -= 1
        if window_successes >= m:
            mk_windows_satisfied += 1

mk_fraction = (mk_windows_satisfied / mk_windows) if mk_windows else 0.0
print(f"(m,k) satisfaction fraction: {mk_fraction:.4f} "
      f"({mk_windows_satisfied}/{mk_windows} windows)")

from simso.core import Model
from simso.configuration import Configuration

# Build configuration in code
cfg = Configuration()
# Sim duration: 500 ms
cfg.duration = 500 * cfg.cycles_per_ms

# One CPU
cfg.add_processor(name="CPU 1", identifier=1)

# Periodic tasks:  (name, id, period, wcet, deadline)
cfg.add_task(name="T1", identifier=1, period=20, wcet=5, deadline=20)
cfg.add_task(name="T2", identifier=2, period=50, wcet=10, deadline=50)
cfg.add_task(name="T3", identifier=3, period=100, wcet=15, deadline=100)

# Use the built-in uniprocessor EDF
cfg.scheduler_info.clas = "simso.schedulers.EDF"

# Sanity-check config, build model, run
cfg.check_all()
model = Model(cfg)
model.run_model()

# Quick report
misses = []
for task in model.results.tasks.values():
    for job in task.jobs:
        if job.exceeded_deadline:
            misses.append((job.name, job.absolute_deadline))

print("Missed deadlines:", misses if misses else "None")
for task in model.results.tasks.values():
    print(f"{task.name}: preemptions={task.preemption_count}, jobs={len(task.jobs)}")


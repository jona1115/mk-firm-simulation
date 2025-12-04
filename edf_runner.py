from runner_common import create_configuration, run_and_report

SIM_DURATION_MS = 35  # raise to 500+ for longer runs
cfg = create_configuration(SIM_DURATION_MS, "simso.schedulers.EDF")

# Task set 1, below task set is 100% utilization
# cfg.add_task(name="T1", identifier=1, period=20, wcet=5, deadline=20, m=5, k=5)       # 25%, period, deadline unit in ms
# cfg.add_task(name="T2", identifier=2, period=50, wcet=10, deadline=50, m=9, k=9)      # 20%
# cfg.add_task(name="T3", identifier=3, period=100, wcet=15, deadline=100, m=4, k=4)    # 15%
# cfg.add_task(name="T4", identifier=4, period=10, wcet=2, deadline=10, m=3, k=3)       # 20%
# cfg.add_task(name="T5", identifier=5, period=30, wcet=6, deadline=30, m=3, k=3)       # 20%

# Task set 2, this is from homework 3' QC 2b
cfg.add_task(name="T1", identifier=1, period=4, wcet=1, deadline=4, m=2, k=3)
cfg.add_task(name="T2", identifier=2, period=6, wcet=3, deadline=6, m=1, k=2)
cfg.add_task(name="T3", identifier=3, period=9, wcet=3, deadline=9, m=2, k=3)


run_and_report(cfg)

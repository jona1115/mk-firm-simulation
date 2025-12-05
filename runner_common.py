import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SIMSO_ROOT = ROOT / "simso"
if str(SIMSO_ROOT) not in sys.path:
    sys.path.insert(0, str(SIMSO_ROOT))

from simso.core import Model
from simso.configuration import Configuration


def create_configuration(duration_ms, scheduler_class):
    cfg = Configuration()
    cfg.duration = duration_ms * cfg.cycles_per_ms
    cfg.add_processor(name="CPU 1",
                      identifier=1,
                      cs_overhead=0,
                      cl_overhead=0,
                      migration_overhead=0,
                      speed=1.0)
    cfg.scheduler_info.clas = scheduler_class
    return cfg


def run_and_report(cfg):
    cfg.check_all()
    model = Model(cfg)
    model.run_model()
    _print_results(cfg, model)
    return model


def _print_results(cfg, model):
    misses, miss_count = _collect_miss_stats(model)

    print(f"Total missed: {miss_count}")
    print("Missed deadlines:", misses if misses else "None")

    print("Task Report:")
    for task in model.results.tasks.values():
        print(f"  {task.name}: preemptions={task.preemption_count}, jobs={len(task.jobs)}")

    total_jobs = sum(len(task.jobs) for task in model.results.tasks.values())
    miss_ratio = miss_count / total_jobs if total_jobs else 0.0
    print(f"Deadline miss ratio: {miss_ratio:.4f}")

    # scheduler = model.results.scheduler
    # sched_overhead = (scheduler.schedule_overhead +
    #                   scheduler.activate_overhead +
    #                   scheduler.terminate_overhead)
    # proc_overhead = sum(proc.context_save_overhead + proc.context_load_overhead
    #                     for proc in model.results.processors.values())
    # total_overhead = sched_overhead + proc_overhead
    # duration = cfg.duration or 1
    # overhead_ratio = total_overhead / duration
    # overhead_ms = total_overhead / cfg.cycles_per_ms
    # print("Overhead report:")
    # print(f"  Scheduler overhead (cycles): {sched_overhead}")
    # print(f"  Processor overhead (cycles): {proc_overhead}")
    # print(f"  Total overhead: {total_overhead} cycles ({overhead_ms:.3f} ms)")
    # print(f"  Overhead ratio: {overhead_ratio:.6f}")

    mk_satisfied, mk_total = _mk_window_stats(model)
    mk_fraction = (mk_satisfied / mk_total) if mk_total else 0.0
    print(f"(m,k) satisfaction fraction: {mk_fraction:.4f} "
          f"({mk_satisfied}/{mk_total} windows)")


def _collect_miss_stats(model):
    misses = []
    miss_count = 0
    for task in model.results.tasks.values():
        for job in task.jobs:
            if job.exceeded_deadline:
                misses.append((job.name, job.absolute_deadline))
                miss_count += 1
    return misses, miss_count


def _mk_window_stats(model):
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

        window_successes = sum(not job.exceeded_deadline for job in jobs[:k])
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
    return mk_windows_satisfied, mk_windows

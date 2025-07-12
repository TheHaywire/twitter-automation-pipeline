import schedule
import time
from typing import Callable, List

def schedule_jobs(job: Callable, times: List[str]):
    """
    Schedule a job to run at specified times (24h format strings).
    """
    for t in times:
        schedule.every().day.at(t).do(job)

def run_scheduler():
    """
    Run the scheduler loop.
    """
    while True:
        schedule.run_pending()
        time.sleep(1)

"""
store jobs id and status
"""

from typing import Literal


class JobIdStore:
    def __init__(self):
        self.store: dict[str, Literal["Pending", "Running", "Completed", "Failed"]] = {}

    def create(self, job_id: str):
        self.store[job_id] = "Pending"

    def update(
        self, job_id: str, status: Literal["Pending", "Running", "Completed", "Failed"]
    ):
        self.store[job_id] = status

    def read(
        self, job_id: str
    ) -> Literal["Pending", "Running", "Completed", "Failed", "NotFound"]:
        return self.store.get(job_id, "NotFound")

    def clear(self):
        self.store.clear()


job_id_store = JobIdStore()

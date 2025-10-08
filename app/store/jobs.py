"""
store jobs id and status
"""

from typing import Any, Literal


class JobIdStore:
    def __init__(self):
        self.store: dict[str, dict[str, Any]] = {}

    def create(self, job_id: str):
        self.store[job_id] = {
            "status": "Pending",
            "result": None,
            "error": None,
        }

    def update_status(
        self, job_id: str, status: Literal["Pending", "Running", "Completed", "Failed"]
    ):
        self.store[job_id]["status"] = status

    def read_status(
        self, job_id: str
    ) -> Literal["Pending", "Running", "Completed", "Failed", "NotFound"]:
        if self.store.get(job_id, None) is None:
            return "NotFound"
        return self.store[job_id]["status"]

    def save_result(self, job_id: str, result: dict):
        self.store[job_id]["result"] = result

    def store_error(self, job_id: str, error: str):
        self.store[job_id]["error"] = error

    def clear(self):
        self.store.clear()


job_id_store = JobIdStore()

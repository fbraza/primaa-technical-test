import pytest

from app.db import job_id_store


@pytest.fixture(autouse=True)
def clear_store():
    job_id_store.clear()


@pytest.fixture
def set_fake_db():
    jobs = ["job_01", "job_02", "job_03", "job_04"]
    status = ["Pending", "Running", "Completed", "Failed"]

    for job_id in jobs:
        job_id_store.create(job_id=job_id)

    for job_id, _status in zip(jobs, status):
        job_id_store.update(job_id=job_id, status=_status)  # type: ignore

    return job_id_store

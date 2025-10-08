from fastapi import APIRouter
from models import JobStatusResponse

from app.db import job_id_store

router = APIRouter()


@router.get("/status/{job_id}")
def get_job_status(
    job_id: str,
) -> JobStatusResponse:
    """
    Collect the status "Pending", "Running", "Completed" or "Failed" of a job.
    If job does not exist status will be "NotFound"
    """
    if job_id_store.read_status(job_id) == "NotFound":
        return JobStatusResponse(
            code=404,
            status="NotFound",
            job_id=None,
        )
    return JobStatusResponse(
        code=200,
        status=job_id_store.read_status(job_id),
        job_id=job_id,
    )

from uuid import uuid4

from fastapi import APIRouter, Body
from models import JobStatusResponse, JobSubmissionRequest
from pydantic import ValidationError

from app.db import job_id_store

router = APIRouter()


@router.post("/job-submission")
def submit_job(
    payload: dict = Body(...),
) -> JobStatusResponse:
    """
    Submit processing job
    """
    job_id = str(uuid4())
    job_id_store.create(job_id)

    try:
        _ = JobSubmissionRequest(**payload)
    except ValidationError as exc:
        job_id_store.update_status(job_id=job_id, status="Failed")
        job_id_store.store_error(job_id=job_id, error=str(exc))

        return JobStatusResponse(
            code=404,
            job_id=job_id,
            status=job_id_store.read_status(job_id),
            error=str(exc),
        )

    # background job

    return JobStatusResponse(
        code=200, job_id=job_id, status=job_id_store.read_status(job_id)
    )

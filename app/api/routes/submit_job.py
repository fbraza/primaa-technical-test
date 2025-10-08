from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, Body
from pydantic import ValidationError

from app.config.models import JobStatusResponse, JobSubmissionRequest
from app.primaalgo import process
from app.store.jobs import job_id_store

router = APIRouter()


@router.post("/job-submission")
def submit_job(
    worker: BackgroundTasks,
    payload: dict = Body(...),
) -> JobStatusResponse:
    """
    Submit processing job
    """
    job_id = str(uuid4())
    job_id_store.create(job_id)

    try:
        request = JobSubmissionRequest(**payload)
    except ValidationError as exc:
        job_id_store.update_status(job_id=job_id, status="Failed")
        job_id_store.store_error(job_id=job_id, error=str(exc))

        return JobStatusResponse(
            code=404,
            job_id=job_id,
            status=job_id_store.read_status(job_id),
            error=str(exc),
        )

    worker.add_task(func=process.job, job_request=request, job_id=job_id)

    return JobStatusResponse(
        code=200, job_id=job_id, status=job_id_store.read_status(job_id)
    )

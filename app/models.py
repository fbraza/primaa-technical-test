from typing import Literal

from pydantic import BaseModel


class JobStatusResponse(BaseModel):
    code: int
    job_id: str | None
    status: Literal["Pending", "Running", "Completed", "Failed", "NotFound"]

import re
from typing import Literal

from pydantic import BaseModel, model_validator

VALID_URL_PATTERN = r"^https:\/\/[A-Za-z0-9.-]+(?:\/[^\s]*)?$"


class JobStatusResponse(BaseModel):
    code: int
    job_id: str | None
    status: Literal["Pending", "Running", "Completed", "Failed", "NotFound"]
    error: str | None = None


class JobSubmissionRequest(BaseModel):
    image_url: str
    callback_url: str
    callback_token: str
    algorithm_name: str

    @model_validator(mode="after")
    def check_urls(self):
        if not re.match(pattern=VALID_URL_PATTERN, string=self.image_url):
            raise ValueError(f"Invalid email for image at : {self.image_url}")

        if not re.match(pattern=VALID_URL_PATTERN, string=self.callback_url):
            raise ValueError(f"Invalid email for callback at : {self.callback_url}")

        return self

    @model_validator(mode="after")
    def check_algorithm(self):
        valid_algorithms = ["poi_detection", "roi_detection"]
        if self.algorithm_name not in valid_algorithms:
            raise ValueError(
                f"'{self.algorithm_name}' is invalid : available algorithms are '{valid_algorithms}'"
            )

        return self

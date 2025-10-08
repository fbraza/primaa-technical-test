import pytest
from fastapi import FastAPI, testclient

from app.api.routes import get_job_id

app = FastAPI(title="testing API")
app.include_router(get_job_id.router)

client = testclient.TestClient(app)


@pytest.mark.parametrize(
    "job_id,expected,http_code",
    [
        ("job_01", "Pending", 200),
        ("job_02", "Running", 200),
        ("job_03", "Completed", 200),
        ("job_04", "Failed", 200),
        ("job_05", "NotFound", 404),
    ],
)
def test_status(set_fake_db, job_id, expected, http_code):
    res = client.get(f"/status/{job_id}")
    assert res.json()["code"] == http_code
    assert res.json()["status"] == expected

from fastapi import FastAPI, testclient

from app import db
from app.api.routes import submit_job

app = FastAPI(title="testing API")
app.include_router(submit_job.router)

client = testclient.TestClient(app)


def test_submit_job_with_valid_payload():
    payload = {
        "image_url": "https://www.icm.unicancer.fr/sites/default/files/resources/images/Image%204%20HE",
        "callback_url": "https://api.partnera.com/receive_result",
        "callback_token": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "algorithm_name": "poi_detection",
    }
    response = client.post("/job-submission", json=payload)
    assert response.json()["code"] == 200
    assert response.json()["status"] == "Pending"

    assert len(db.job_id_store.store.keys()) == 1


def test_submit_job_with_invalid_payload():
    payload = {
        "image_url": "ftp://www.icm.unicancer.fr/sites/default/files/resources/images/Image%204%20HE",
        "callback_url": "https://api.partnera.com/receive_result",
        "callback_token": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "algorithm_name": "poi_detection",
    }
    response = client.post("/job-submission", json=payload)
    assert response.json()["code"] == 404
    assert response.json()["status"] == "Failed"

    assert len(db.job_id_store.store.keys()) == 1

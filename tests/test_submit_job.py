import time

from fastapi import FastAPI, testclient

from app.api.routes import submit_job
from app.store import jobs

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

    assert len(jobs.job_id_store.store.keys()) == 1


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

    assert len(jobs.job_id_store.store.keys()) == 1


def test_submit_job_poi(fake_callback_post):
    payload = {
        "image_url": "https://www.inotiv.com/hs-fs/hubfs/18-Bronchus-edited.jpeg?width=2132&height=1596&name=18-Bronchus-edited.jpeg",
        "callback_url": "https://api.partnera.com/receive_result",
        "callback_token": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "algorithm_name": "poi_detection",
    }

    response = client.post("/job-submission", json=payload)
    assert response.json()["code"] == 200

    time.sleep(1)
    assert len(jobs.job_id_store.store.keys()) == 1

    for job_id in jobs.job_id_store.store.keys():
        assert jobs.job_id_store.read_status(job_id=job_id) == "Completed"
        assert jobs.job_id_store.store[job_id]["result"] == {
            "type": "Feature",
            "geometry": {
                "type": "MultiPoint",
                "coordinates": [
                    [30.0, 10.0],
                    [40.0, 40.0],
                ],
            },
            "properties": {
                "job_id": job_id,
                "algorithm_name": "poi_detection",
                "image_url": "https://www.inotiv.com/hs-fs/hubfs/18-Bronchus-edited.jpeg?width=2132&height=1596&name=18-Bronchus-edited.jpeg",
            },
        }

    assert fake_callback_post["status_code"] == 200


def test_submit_job_roi(fake_callback_post):
    payload = {
        "image_url": "https://www.inotiv.com/hs-fs/hubfs/18-Bronchus-edited.jpeg?width=2132&height=1596&name=18-Bronchus-edited.jpeg",
        "callback_url": "https://api.partnera.com/receive_result",
        "callback_token": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "algorithm_name": "roi_detection",
    }

    response = client.post("/job-submission", json=payload)
    assert response.json()["code"] == 200

    time.sleep(1)
    assert len(jobs.job_id_store.store.keys()) == 1

    for job_id in jobs.job_id_store.store.keys():
        assert jobs.job_id_store.read_status(job_id=job_id) == "Completed"
        assert jobs.job_id_store.store[job_id]["result"] == {
            "type": "Feature",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [180.0, 40.0],
                            [180.0, 50.0],
                            [170.0, 50.0],
                            [170.0, 40.0],
                            [180.0, 40.0],
                        ]
                    ],
                    [
                        [
                            [-170.0, 40.0],
                            [-170.0, 50.0],
                            [-180.0, 50.0],
                            [-180.0, 40.0],
                            [-170.0, 40.0],
                        ]
                    ],
                ],
            },
            "properties": {
                "job_id": job_id,
                "algorithm_name": "roi_detection",
                "image_url": "https://www.inotiv.com/hs-fs/hubfs/18-Bronchus-edited.jpeg?width=2132&height=1596&name=18-Bronchus-edited.jpeg",
            },
        }

    assert fake_callback_post["status_code"] == 200


def test_submit_job_with_invalid_img_url(fake_callback_post):
    payload = {
        "image_url": "https://www.icm.unicancer.fr/sites/default/files/resources/images/Image%204%20HE",
        "callback_url": "https://api.partnera.com/receive_result",
        "callback_token": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "algorithm_name": "roi_detection",
    }

    response = client.post("/job-submission", json=payload)
    assert response.json()["code"] == 200
    assert len(jobs.job_id_store.store.keys()) == 1

    for job_id in jobs.job_id_store.store.keys():
        assert jobs.job_id_store.read_status(job_id=job_id) == "Failed"
        assert jobs.job_id_store.store[job_id]["error"] == "Error: Image not Found"
        assert jobs.job_id_store.store[job_id]["result"] is None

    assert fake_callback_post.get("status_code", None) is None


def test_two_job_submission(fake_callback_post):
    payload_poi = {
        "image_url": "https://www.inotiv.com/hs-fs/hubfs/18-Bronchus-edited.jpeg?width=2132&height=1596&name=18-Bronchus-edited.jpeg",
        "callback_url": "https://api.partnera.com/receive_result",
        "callback_token": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "algorithm_name": "poi_detection",
    }

    payload_roi = {
        "image_url": "https://www.inotiv.com/hs-fs/hubfs/18-Bronchus-edited.jpeg?width=2132&height=1596&name=18-Bronchus-edited.jpeg",
        "callback_url": "https://api.partnera.com/receive_result",
        "callback_token": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "algorithm_name": "poi_detection",
    }

    response_poi = client.post("/job-submission", json=payload_poi)
    response_roi = client.post("/job-submission", json=payload_roi)

    assert response_poi.json()["code"] == 200
    assert response_roi.json()["code"] == 200

    time.sleep(2)

    assert len(jobs.job_id_store.store.keys()) == 2
    for job_id in jobs.job_id_store.store.keys():
        assert jobs.job_id_store.read_status(job_id=job_id) == "Completed"

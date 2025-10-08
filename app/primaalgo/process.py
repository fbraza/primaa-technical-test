import io
import json

import geojson
import requests
from PIL import Image
from shapely import wkt
from shapely.geometry import mapping

from app.config.models import JobSubmissionRequest
from app.primaalgo import poi_detection as poi
from app.primaalgo import roi_detection as roi
from app.store.jobs import job_id_store


def job(job_request: JobSubmissionRequest, job_id: str):
    """
    Worker job. This the background job running.
    We assumed at this step image and callback url are valid and well formed
    """
    result: geojson.Feature | str | None = None
    req_img = requests.get(url=job_request.image_url, stream=True, timeout=30)

    if req_img.status_code == 200:
        img = Image.open(io.BytesIO(req_img.content))
    else:
        job_id_store.update_status(job_id=job_id, status="Failed")
        job_id_store.store_error(job_id=job_id, error="Error: Image not Found")
        return

    job_properties = {
        "job_id": job_id,
        "algorithm_name": job_request.algorithm_name,
        "image_url": job_request.image_url,
    }

    job_id_store.update_status(job_id=job_id, status="Running")

    if job_request.algorithm_name == "poi_detection":
        try:
            mapping_for_geojson = mapping(wkt.loads(poi.process(image=img)))
            result = geojson.Feature(
                geometry=mapping_for_geojson, properties=job_properties
            )
            job_id_store.update_status(job_id=job_id, status="Completed")
        except Exception as exc:
            # not the cleanest to use Exception would adapt with custom error
            job_id_store.update_status(job_id=job_id, status="Failed")
            job_id_store.store_error(job_id=job_id, error=str(exc))
    elif job_request.algorithm_name == "roi_detection":
        try:
            result = roi.process(image=img)
            result["properties"] = job_properties  # type: ignore
            job_id_store.update_status(job_id=job_id, status="Completed")

        except Exception as exc:
            # not the cleanest to use Exception would adapt with custom error
            job_id_store.update_status(job_id=job_id, status="Failed")
            job_id_store.store_error(job_id=job_id, error=str(exc))

    if result is None:
        return

    dump_result = json.loads(geojson.dumps(result, indent=4))
    job_id_store.save_result(job_id=job_id, result=dump_result)

    requests.post(
        url=job_request.callback_url,
        json=dump_result,
        headers={"Authorization": f"Bearer {job_request.callback_token}"},
        timeout=30,
    )

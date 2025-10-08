import time

import geojson
from PIL import Image


def process(image: Image.Image) -> geojson.Feature:
    """
    Detects Regions of Interest (ROIs) in an image.
    The result is a geojson Feature containing a MultiPolygon geometry.
    """
    time.sleep(0.5)
    return geojson.Feature(
        geometry={
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
    )

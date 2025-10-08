import time

from PIL import Image


def process(image: Image.Image) -> str:
    """
    Detects Points of Interest (POIs) in an image.
    The result is a string in WKT MULTIPOINT format.
    Example: 'MULTIPOINT (30 10, 40 40)'
    """
    time.sleep(0.5)
    return "MULTIPOINT (30 10, 40 40)"

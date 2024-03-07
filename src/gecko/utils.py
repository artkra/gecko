from typing import List

from PIL.JpegImagePlugin import JpegImageFile
from IPython import display


def create_gif(images: List[JpegImageFile], output_path: str) -> None:
    images[0].save(output_path, save_all=True, append_images=images, loop=2<<10)
    return


def display_gif(gif_path):
    return display.Image(filename=gif_path, embed=True)

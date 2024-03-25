from typing import List

from IPython import display

from .data import SOHOImage


def create_gif(images: List[SOHOImage], output_path: str) -> None:
    _images = [x.image for x in images]
    _images[0].save(output_path, save_all=True, append_images=_images, loop=2<<10)
    return


def display_gif(gif_path):
    return display.Image(filename=gif_path, embed=True)

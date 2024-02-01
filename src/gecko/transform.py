from functools import reduce
from typing import List, Optional

from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile


class Blender:
    """
    This transformer creates a single image out of an array of images by blending their opaque versions.
    The level of transparency for each image is either calculated automatically or is set default by class initialization.

    -------

    Args:
        alpha: Optional[int]=None
            Level of transparency applied to every image(integer, 0 < alpha < 255).
        
    -------

    Methods:
        blend(images: List[JpegImageFile]) -> JpegImageFile
            Compose image by blending an array of images.

    -------

    Example:

    >>> from gecko.transform import Blender
    >>> blender = Blender(alpha=70)
    >>> composed_image = blender.blend(images=[image1, image2, image3, image4, image5])
    >>> composed_image
    |  .........  |
    |  ...some..  |
    |  ..pretty.  |
    |  .image...  |
    |  .........  |

    """
    def __init__(self, alpha: Optional[int]=None) -> None:
        self.alpha = alpha
        if self.alpha is None:
            return

        if alpha < 0 or alpha > 255:
            raise ValueError(f'Alpha value must be an integer between 0 and 255')
        self.alpha = round(alpha)

    def blend(self, images: List[JpegImageFile]) -> JpegImageFile:
        alpha = self.alpha or round(255/len(images)) + 5
        for img in images:
            img.putalpha(alpha)
        return reduce(Image.alpha_composite, images)

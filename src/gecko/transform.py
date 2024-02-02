from functools import reduce
from typing import List, Optional

import numpy as np
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile


class Simplifier:
    """
    This transformer simplifies the picture by making glowing dots black and everything below chosen 'glowing' level white.
    It also can enlarge the dots by couple of pixels to ease the search.

    -------

    Args:
        level: Optional[int]=150
            White out the pixel if its 'brightness' (RGB channels) is below this level (integer, 0 < level < 255).
        add_pixels: Optional[int]=1
            How many surrounding pixels to add to increase the contrast.
        
    -------

    Methods:
        transform(image: JpegImageFile) -> JpegImageFile
            Compose image by blending an array of images.

    -------

    Example:

    >>> from gecko.transform import Simplifier
    >>> simplifier = Simplifier(level=100, add_pixels=3)
    >>> simple_image = simplifier.transform(image)
    >>> simple_image
    |  .   .   .  |
    |  . .some..  |
    |  ..simple.  |
    |   image. .  |
    |      . . .  |

    """
    def __init__(self, level:int=150, add_pixels:int=1) -> None:
        if level < 0 or level > 255:
            raise ValueError(f'Level value must be an integer between 0 and 255. Given: {level}')
        
        if add_pixels < 0 or add_pixels > 10:
            raise ValueError(
                f'`add_pixels` value must be a small positive integer below 10. Otherwise it will ruin the image. Given: {add_pixels}'
            )

        self.level = level
        self.add_pixels = add_pixels
    
    def transform(self, image: JpegImageFile) -> JpegImageFile:
        img_pil = image.convert('RGBA') 
        image_arr = np.asarray(img_pil)
        img_copy = image_arr.copy()
        img_copy.setflags(write=1)
        for i in range(img_copy.shape[0]):
            for j in range(img_copy.shape[1]):
                if all([img_copy[i][j][0] > self.level, img_copy[i][j][1] > self.level, img_copy[i][j][2] > self.level]):
                    img_copy[i][j] = [0, 0, 0, 255]
                    for i_delta in range(-self.add_pixels, self.add_pixels):
                        for j_delta in range(-self.add_pixels, self.add_pixels):
                            try:
                                img_copy[i+i_delta][j+j_delta] = [0, 0, 0, 255]
                            except:
                                pass
                else:
                    img_copy[i][j] = [255, 255, 255, 255]

        return Image.fromarray(img_copy)


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
            raise ValueError(f'Alpha value must be an integer between 0 and 255. Given: {alpha}')
        self.alpha = round(alpha)

    def blend(self, images: List[JpegImageFile]) -> JpegImageFile:
        alpha = self.alpha or round(255/len(images)) + 5
        img_copies = []
        for img in images:
            img_copy = img.copy()
            img_copy.putalpha(alpha)
            img_copies.append(img_copy)
        return reduce(Image.alpha_composite, img_copies)
    

class Amplifier:
    """
    The class 
    """

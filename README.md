# gecko

It's a small tool for working with 'SOHO' mission images. Aims to help the "Sungrazer" comet hunting project.

<img src="test.gif" height=500 width=500/>

Currently available features:

- image data loader
```python
import datetime
from gecko.data import JPEGDataLoader


loader = JPEGDataLoader(camera='c3')  # instantiate data loader with specified camera (c2/c3)

# choose your datetime slice
start_datetime = datetime.datetime(2008, 7, 8, 7, 41, 0)
end_datetime = datetime.datetime(2008, 7, 8, 15, 45, 0)

images_paths = loader.ls_images(start_datetime, end_datetime)  # list all images available for the period
images = [loader.get_image(x) for x in images_paths]  # load them as PIL.JpegImagePlugin.JpegImageFile objects

first_image = images[0]
first_image  # when in Jupyter Notebook you'll be able to render the image just like that
```
- simplify image
```python
from gecko.transform import Simplifier

# this thing inverts colors to only white and black to keep the picture simple.
#   `level=150` this tells the handler to whit out the pixel if its 'brightness' (RGB channels) is below this level (integer, 0 < level < 255)
#   `add_pixels=<NUMBER_OF_PIXELS>` adds additional pixels around black ones so it's easier to track them with your eyes
simplifier = Simplifier(level=150, add_pixels=0)  
simplified_images = [simplifier.transform(x) for x in images]  # suppose we have `images` list of objects from the example above

first_simplified_image = simplified_images[0]
first_simplified_image  # when in Jupyter Notebook you'll be able to render the image just like that
```
- create gif
```python
from gecko.utils import create_gif

create_gif(images, 'test.gif')  # suppose we have `images` list of objects from the example above
```
- display gif
```python
from gecko.utils import display_gif

display_gif('test.gif')  # display the gif inside the Jupyter Notebook
```

Working on:
- automated search
- validator
- report generator

Contacts: artkrasnyy@gmail.com

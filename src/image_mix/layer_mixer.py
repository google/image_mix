# Copyright 2022 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A module for mixing image & text layers to generate an image creative."""
from typing import Sequence, Tuple

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from image_mix import base_layer
from image_mix import image_layer
from image_mix import text_layer

_IMAGE_MODE = 'RGBA'
_DEFAULT_BACKGROUND_RGBA_COLOR_WHITE = (255, 255, 255, 0)


class LayerMixer:
  """A class to mix image & text layers and save the generated image creative."""

  def __init__(self, size: Tuple[int, int]):
    """Constructor.

    Args:
      size: Size of image to generate. A tuple with format (width, height).
    """
    self._image = Image.new(_IMAGE_MODE, size,
                            _DEFAULT_BACKGROUND_RGBA_COLOR_WHITE)

  def add_layers(self, layers: Sequence[base_layer.BaseLayer]) -> None:
    """Adds a layer on top of the image.

    Args:
      layers: Layers to add on top of the image. The layers are added to the
        image in the same order of the sequence.
    """
    for layer in layers:
      if isinstance(layer, image_layer.ImageLayer):
        self._add_image_layer(layer)
      if isinstance(layer, text_layer.TextLayer):
        self._add_text_layer(layer)

  def _add_image_layer(self, layer: image_layer.ImageLayer) -> None:
    """Adds an image layer on top of the image.

    Args:
      layer: An image layer to add on top of the image.
    """
    image_binary = Image.open(layer.file_path)
    image_binary = image_binary.resize(layer.size())
    layer_to_add = Image.new(_IMAGE_MODE, self._image.size,
                             _DEFAULT_BACKGROUND_RGBA_COLOR_WHITE)
    layer_to_add.paste(image_binary, layer.position())
    self._image = Image.alpha_composite(self._image, layer_to_add)

  def _add_text_layer(self, layer: text_layer.TextLayer) -> None:
    """Adds a text layer on top of the image.

    Args:
      layer: A text layer to add on top of the image.
    """
    font = ImageFont.truetype(layer.font_file_path, layer.font_size)
    draw = ImageDraw.Draw(self._image)
    draw.text(layer.position(), layer.text_content, layer.rgb_color(), font)

  def save_image(self, path: str) -> None:
    """Saves the image creative as a PNG file at the provided path.

    Args:
      path: Path where we save our image creative file.
    """
    self._image.save(path, quality=95, format='PNG')

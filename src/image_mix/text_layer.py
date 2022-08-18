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

"""Module defining the TextLayer data class."""
import dataclasses
from typing import Tuple

from image_mix import base_layer


@dataclasses.dataclass(frozen=True)
class TextLayer(base_layer.BaseLayer):
  """Class to store the details about the text layer information.

  color_r, color_g, color_b must be between 0 and 255.
  """
  font_size: int
  font_file_path: str
  color_r: int
  color_g: int
  color_b: int
  text_content: str

  def __post_init__(self):
    super().__post_init__()

    if not self.font_file_path:
      raise ValueError('font_file_path should not be empty.')

    if self.color_r > 255 or self.color_r < 0:
      raise ValueError('color_r must be between 0 and 255 included.')

    if self.color_g > 255 or self.color_g < 0:
      raise ValueError('color_g must be between 0 and 255 included.')

    if self.color_b > 255 or self.color_b < 0:
      raise ValueError('color_b must be between 0 and 255 included.')

    if not self.text_content:
      raise ValueError('text_content should not be empty.')

  def rgb_color(self) -> Tuple[int, int, int]:
    """Returns a tuple representing the RGB color of the text.

    The format is (Red, Green, Blue).
    """
    return self.color_r, self.color_g, self.color_b

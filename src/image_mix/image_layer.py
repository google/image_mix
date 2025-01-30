# Copyright 2024 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module defining the ImageLayer data class."""
import dataclasses

from image_mix import base_layer


@dataclasses.dataclass(frozen=True)
class ImageLayer(base_layer.BaseLayer):
  """Class to store the details about the image layer information."""

  width: int
  height: int
  file_path: str

  def __post_init__(self):
    super().__post_init__()
    if not self.file_path:
      raise ValueError('file_path cannot be empty')

    for element in [self.width, self.height]:
      if element < 0:
        raise ValueError('%s must be a positive number' % element)

  def size(self) -> tuple[int, int]:
    """Returns a tuple representing the size of the layer.

    The format is (Width, Height).
    """
    return self.width, self.height

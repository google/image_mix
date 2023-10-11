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

"""Module defining the BaseLayer data class."""
import abc
import dataclasses
from typing import Tuple


@dataclasses.dataclass(frozen=True)
class BaseLayer(abc.ABC):
  """Base class to store the details about the layer information."""
  layer_id: str
  position_x: int  # X position of top left of the image.
  position_y: int  # Y position of top left of the image.

  def __post_init__(self) -> None:
    if not self.layer_id:
      raise ValueError('layer_id cannot be empty')

    for element in [self.position_x, self.position_y]:
      if element < 0:
        raise ValueError('%s must be a positive number' % element)

  def position(self) -> Tuple[int, int]:
    """Returns a tuple representing the position of the layer.

    The format is (X, Y).
    """
    return self.position_x, self.position_y

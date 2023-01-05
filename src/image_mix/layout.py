# Copyright 2023 Google LLC.
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

"""Module defining the Layout data class."""
import dataclasses
from typing import List

from image_mix import base_layer
from image_mix import canvas


@dataclasses.dataclass(frozen=True)
class Layout:
  """Class to store the details about the Layout of our creative."""
  canvas: canvas.Canvas
  output_filename: str
  layers: List[base_layer.BaseLayer]

  def __post_init__(self):
    if not self.output_filename:
      raise ValueError('output_finemame cannot be empty.')

    if not self.canvas:
      raise ValueError('canvas cannot be empty.')

    if not self.layers:
      raise ValueError('layers cannot be empty.')

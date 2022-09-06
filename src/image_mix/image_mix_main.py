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

"""This module defines the ImageMixMain class.

The ImageMixMain class uses the SpreadsheetLoader and the LayerMixer to
generate creatives.

Typical usage:
  image_mixer = image_mix_main.ImageMixMain(
      spreadsheet_url,
      image_directory_path,
      default_font_file_path,
      output_path)

  image_mixer.generate_creatives()
"""

import os

from image_mix import layer_mixer as layer_mixer_lib
from image_mix import spreadsheet_loader as spreadsheet_loader_lib


class ImageMixMain:
  """Reads layouts from the spreadsheet and generate creatives."""

  def __init__(self, spreadsheet_url: str, image_directory_path: str,
               default_font_file_path: str, output_path: str):
    """Constructor for the ImageMixMain class.

    Args:
      spreadsheet_url: The url to the imagemix spreadsheet config.
      image_directory_path: Path to the directory where the images are read
        from.
      default_font_file_path: Path to the font to be used by the generated
        text for text layer's text.
      output_path: Directory path where we save the generated creatives.

    Raises:
      ValueError: If the spreadsheet_url is empty or invalid or if
      image_directory_path or output_file or default_font_file_path are empty.
    """
    self._spreadsheet_url = spreadsheet_url
    self._image_directory_path = image_directory_path
    self._default_font_file_path = default_font_file_path
    if not output_path:
      raise ValueError('output_path cannot be empty')
    self._output_path = output_path
    self._spreadsheet_loader = spreadsheet_loader_lib.SpreadSheetLoader(
        self._spreadsheet_url, self._image_directory_path,
        self._default_font_file_path)

  def generate_creatives(self):
    """Generates creatives by mixing layers and saves them to the output dir.

    Creates the output directory if it doesn't exist.

    Raises:
      ValueError: When the spreadsheet format is invalid.
      FileNotFoundError: When an image layer image cannot be found at the
        specified path.
      OSError: When the font file specified cannot be found.
               When writing the creative to the specified output directory
               encounter an issue.
    """
    layouts = self._spreadsheet_loader.get_layouts()
    os.makedirs(self._output_path, exist_ok=True)

    for layout in layouts:
      layer_mixer = layer_mixer_lib.LayerMixer(
          (layout.canvas.width, layout.canvas.height))
      layer_mixer.add_layers(layout.layers)
      output_file_path = os.path.join(self._output_path, layout.output_filename)
      layer_mixer.save_image(output_file_path)

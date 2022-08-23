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

"""This module defines the SpreadSheetLoader class.

Typical usage example:
sheet_loader = SpreadSheetLoader('https://docs.google.com/spreadsheets/d/1y',
                                 'imagemix/images',
                                 'font/font.ttf')

layouts = sheet_loader.get_layouts()
"""

import os
from typing import List

from google import auth as default_auth
from google.colab import auth as colab_auth
import gspread

from image_mix import canvas as canvas_lib
from image_mix import image_layer as image_layer_lib
from image_mix import text_layer as text_layer_lib


_TEXT_LAYER_TAB = 'TEXT_LAYER'
_IMAGE_LAYER_TAB = 'IMAGE_LAYER'
_CANVAS_TAB = 'CANVAS'

_TEXT_LAYER_ID_COLUMN = 0
_TEXT_LAYER_FONT_SIZE_COLUMN = 1
_TEXT_LAYER_COLOR_R_COLUMN = 2
_TEXT_LAYER_COLOR_G_COLUMN = 3
_TEXT_LAYER_COLOR_B_COLUMN = 4
_TEXT_LAYER_POSITION_X_COLUMN = 5
_TEXT_LAYER_POSITION_Y_COLUMN = 6
_TEXT_LAYER_TEXT_CONTENT_COLUMN = 7

_IMAGE_LAYER_ID_COLUMN = 0
_IMAGE_LAYER_WIDTH_COLUMN = 1
_IMAGE_LAYER_HEIGHT_COLUMN = 2
_IMAGE_LAYER_POSITION_X_COLUMN = 3
_IMAGE_LAYER_POSITION_Y_COLUMN = 4
_IMAGE_LAYER_FILE_NAME_COLUMN = 5

_LAYER_ID_COLUMN_HEADER = 'layer_id'

_CANVAS_ID_COLUMN_HEADER = 'canvas_id'
_CANVAS_ID_COLUMN = 0
_CANVAS_WIDTH_COLUMN = 1
_CANVAS_HEIGHT_COLUMN = 2


class SpreadSheetLoader:
  """Gets the information contained in the Google Sheet used by ImageMix.

  The spreadsheet provided is the input for the ImageMix colab solution.
  This class can extract the layouts, text_layers, image_layers, canvas
  from the sheet and return objects directly (Layout, ImageLayer, etc).
  """

  def __init__(self, spreadsheet_url: str, image_directory_path: str,
               default_font_file_path: str):
    """Initializes the object, authenticate the user, authorize the colab.

    Authenticate the user and autorize the colab to access the user's Google
    Drive.

    Args:
      spreadsheet_url: The Google Spreadsheet URL.
      image_directory_path: Path of the directory containing the images.
      default_font_file_path: Path to the font to use.

    Raises:
      ValueError: If the spreadsheet_url, image_firectory_path,
        default_font_file_path is empty.
      errors.AuthorizationError: If authorization fails.
      google.auth.exceptions.DefaultCredentialsError: If no credentials were
         found, or if the credentials found were invalid.
    """
    if not spreadsheet_url:
      raise ValueError('spreadsheet_url cannot be empty')

    if not image_directory_path:
      raise ValueError('image_directory_path cannot be empty')

    if not default_font_file_path:
      raise ValueError('default_font_file_path cannot be empty')

    self._spreadsheet_url = spreadsheet_url
    self._image_directory_path = image_directory_path
    self._default_font_file_path = default_font_file_path

    self._gspread = self._authorize_spreasheet_access()
    self._spreadsheet = self._gspread.open_by_url(self._spreadsheet_url)

  def _authorize_spreasheet_access(self) -> gspread.Client:
    """Authenticates the user and get authorization to access Drive.

    Returns:
      A gspread.SpreadSheet object representing our Spreadsheer given in
      spreadsheet_url.

    """
    colab_auth.authenticate_user()
    creds, _ = default_auth.default()
    return gspread.authorize(creds)

  def get_text_layers(self) -> List[text_layer_lib.TextLayer]:
    """Returns a list of TextLayer from the spreadsheet.

    Returns:
      A list of TextLayer objects made from the information found in the
      spreadsheet TEXT_LAYER tab.

    Raises:
      gspread.WorksheetNotFound: if no tab TEXT_LAYER is present in the
        spreadsheet.
      ValueError: if a row contains incorrect information to create a TextLayer
        object.
    """
    all_rows_text_layer = self._get_all_values_for_tab(_TEXT_LAYER_TAB)

    text_layers = []
    for index, row in enumerate(all_rows_text_layer):
      if row[_TEXT_LAYER_ID_COLUMN] == _LAYER_ID_COLUMN_HEADER:
        continue

      try:
        text_layer = text_layer_lib.TextLayer(
            layer_id=row[_TEXT_LAYER_ID_COLUMN],
            position_x=int(row[_TEXT_LAYER_POSITION_X_COLUMN]),
            position_y=int(row[_TEXT_LAYER_POSITION_Y_COLUMN]),
            font_size=int(row[_TEXT_LAYER_FONT_SIZE_COLUMN]),
            font_file_path=self._default_font_file_path,
            color_r=int(row[_TEXT_LAYER_COLOR_R_COLUMN]),
            color_g=int(row[_TEXT_LAYER_COLOR_G_COLUMN]),
            color_b=int(row[_TEXT_LAYER_COLOR_B_COLUMN]),
            text_content=row[_TEXT_LAYER_TEXT_CONTENT_COLUMN])
        text_layers.append(text_layer)

      except (ValueError, IndexError) as error:
        raise ValueError(
            (f'Failed to create text layer object from row {index+1} in the '
             'TEXT_LAYER tab please double check this row\'s value')) from error

    return text_layers

  def get_image_layers(self) -> List[image_layer_lib.ImageLayer]:
    """Returns a list of ImageLayer from the spreadsheet.

    Returns:
      A list of ImageLayer objects made from the information found in the
      spreadsheet IMAGE_LAYER tab.

    Raises:
      ValueError: if a row contains incorrect information to create a ImageLayer
        object.
      gspread.WorksheetNotFound: if IMAGE_LAYER tab is not present in the
        spreadsheet.
    """
    all_rows_image_layer = self._get_all_values_for_tab(_IMAGE_LAYER_TAB)

    image_layers = []
    for index, row in enumerate(all_rows_image_layer):
      if row[_IMAGE_LAYER_ID_COLUMN] == _LAYER_ID_COLUMN_HEADER:
        continue

      try:
        image_layer = image_layer_lib.ImageLayer(
            layer_id=row[_IMAGE_LAYER_ID_COLUMN],
            position_x=int(row[_IMAGE_LAYER_POSITION_X_COLUMN]),
            position_y=int(row[_IMAGE_LAYER_POSITION_Y_COLUMN]),
            width=int(row[_IMAGE_LAYER_WIDTH_COLUMN]),
            height=int(row[_IMAGE_LAYER_HEIGHT_COLUMN]),
            file_path=os.path.join(self._image_directory_path,
                                   row[_IMAGE_LAYER_FILE_NAME_COLUMN]))
        image_layers.append(image_layer)

      except (ValueError, IndexError) as error:
        raise ValueError((
            f'Failed to create image layer object from row {index+1} in the '
            'IMAGE_LAYER tab please double check this row\'s value')) from error

    return image_layers

  def get_canvases(self) -> List[canvas_lib.Canvas]:
    """Returns a list of Canvas from the spreadsheet.

    Returns:
      A list of Canvas object made from the information found in the
      CANVAS tab in the spreadsheet.

    Raises:
      gspread.WorksheetNotFound: if CANVAS tab is not present in the
        spreadsheet.
    """
    all_rows_canvas = self._get_all_values_for_tab(_CANVAS_TAB)

    canvases = []
    for index, row in enumerate(all_rows_canvas):
      if row[_CANVAS_ID_COLUMN] == _CANVAS_ID_COLUMN_HEADER:
        continue

      try:
        canvas = canvas_lib.Canvas(
            canvas_id=row[_CANVAS_ID_COLUMN],
            width=int(row[_CANVAS_WIDTH_COLUMN]),
            height=int(row[_CANVAS_HEIGHT_COLUMN]))
        canvases.append(canvas)

      except (ValueError, IndexError) as error:
        raise ValueError((
            f'Failed to create canvas object from row {index+1} in the '
            'CANVAS tab please double check this row\'s value')) from error

    return canvases

  def _get_all_values_for_tab(self, tab_name: str) -> List[List[str]]:
    """Returns all values from the specified tab.

    Args:
      tab_name: Name of the tab we want to get the values from.

    Raises:
      gspread.WorksheetNotFound: if tab_name is not present in the spreadsheet.
    """
    return self._spreadsheet.worksheet(tab_name).get_all_values()

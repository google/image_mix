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

from typing import List

from google import auth as default_auth
from google.colab import auth as colab_auth
import gspread

from image_mix import text_layer as text_layer_lib

_TEXT_LAYER_TAB = 'TEXT_LAYER'

_TEXT_LAYER_ID_COLUMN = 0
_FONT_SIZE_COLUMN = 1
_COLOR_R_COLUMN = 2
_COLOR_G_COLUMN = 3
_COLOR_B_COLUMN = 4
_POSITION_X_COLUMN = 5
_POSITION_Y_COLUMN = 6
_TEXT_CONTENT_COLUMN = 7

_LAYER_ID_COLUMN_HEADER = 'layer_id'


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
    text_layer_worksheet = self._spreadsheet.worksheet(_TEXT_LAYER_TAB)
    all_rows_text_layer = text_layer_worksheet.get_all_values()

    number_of_rows = len(all_rows_text_layer)
    if number_of_rows <= 1:
      return []

    text_layers = []
    for index, row in enumerate(all_rows_text_layer):
      if row[_TEXT_LAYER_ID_COLUMN] == _LAYER_ID_COLUMN_HEADER:
        continue

      try:
        text_layer = text_layer_lib.TextLayer(
            layer_id=row[_TEXT_LAYER_ID_COLUMN],
            position_x=int(row[_POSITION_X_COLUMN]),
            position_y=int(row[_POSITION_Y_COLUMN]),
            font_size=int(row[_FONT_SIZE_COLUMN]),
            font_file_path=self._default_font_file_path,
            color_r=int(row[_COLOR_R_COLUMN]),
            color_g=int(row[_COLOR_G_COLUMN]),
            color_b=int(row[_COLOR_B_COLUMN]),
            text_content=row[_TEXT_CONTENT_COLUMN])
        text_layers.append(text_layer)

      except ValueError as error:
        raise ValueError(
            (f'Fail to create text layer object from row {index+1} in the '
             'TEXT_LAYER tab please double check this row\'s value')) from error

    return text_layers

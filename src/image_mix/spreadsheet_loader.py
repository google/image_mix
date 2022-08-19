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

from google import auth as default_auth

from google.colab import auth as colab_auth
import gspread


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

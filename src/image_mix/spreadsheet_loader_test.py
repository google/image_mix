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

"""Tests for spreadsheet_loader."""

from unittest import mock


from google import auth as default_auth
from google.colab import auth as colab_auth
import gspread

from image_mix import spreadsheet_loader
from absl.testing import absltest


_SHEET_URL = 'https://docs.google.com/spreadsheets/d/1qgWhMMOfedeK2DMeLxqlr7xD1Jbclyo5_mnKOBqerPs/edit#gid=0'
_IMAGE_DIRECTORY_PATH = 'IMAGEMIX/images'

_DEFAULT_FONT_FILE_PATH = 'fonts/dummy-font.ttf'


class SpreadsheetLoaderTest(absltest.TestCase):

  def test_sheetloader_constructor_empty_sheet_url_raises_value_error(self):
    with self.assertRaises(ValueError):
      spreadsheet_loader.SpreadSheetLoader('', _IMAGE_DIRECTORY_PATH,
                                           _DEFAULT_FONT_FILE_PATH)

  def test_sheetloader_constructor_empty_image_directory_path_raises_error(
      self):
    with self.assertRaises(ValueError):
      spreadsheet_loader.SpreadSheetLoader(
          spreadsheet_url=_SHEET_URL,
          image_directory_path='',
          default_font_file_path=_DEFAULT_FONT_FILE_PATH)

  def test_sheetloader_constructor_empty_default_font_file_path_raises_error(
      self):
    with self.assertRaises(ValueError):
      spreadsheet_loader.SpreadSheetLoader(
          spreadsheet_url=_SHEET_URL,
          image_directory_path=_IMAGE_DIRECTORY_PATH,
          default_font_file_path='')

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_sheetloader_constructor_user_authenticated_no_error(
      self, mock_gspead, mock_colab_auth, mock_google_auth):
    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)
    mock_gspead.return_value.open_by_url = mock.Mock()

    spreadsheet_loader.SpreadSheetLoader(_SHEET_URL, _IMAGE_DIRECTORY_PATH,
                                         _DEFAULT_FONT_FILE_PATH)

    mock_colab_auth.assert_called_once()
    mock_google_auth.assert_called_once()
    mock_gspead.assert_called_once()


if __name__ == '__main__':
  absltest.main()

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

"""Tests for spreadsheet_loader."""

from unittest import mock

from google import auth as default_auth
from google.colab import auth as colab_auth
import gspread
from gspread import exceptions as gspread_exceptions

from image_mix import canvas as canvas_lib
from image_mix import image_layer
from image_mix import layout
from image_mix import spreadsheet_loader
from image_mix import text_layer
from absl.testing import absltest


_SHEET_URL = 'https://docs.google.com/spreadsheets/d/1qgWhMMOfedeK2DMeLxqlr7xD1Jbclyo5_mnKOBqerPs/edit#gid=0'
_IMAGE_DIRECTORY_PATH = 'My drive/IMAGEMIX/images'

_DEFAULT_FONT_FILE_PATH = 'fonts/dummy-font.ttf'
_TAB_HEADER_TEXT_LAYER = [
    'layer_id', 'font_size', 'color_r', 'color_g', 'color_b', 'position_x',
    'position_y', 'text_content'
]

_TAB_HEADER_IMAGE_LAYER = [
    'layer_id', 'width', 'height', 'position_x', 'position_y', 'filename'
]

_TAB_HEADER_CANVAS = ['canvas_id', 'width', 'height']

_TAB_HEADER_LAYOUT = [
    'output_filename', 'canvas_id', 'layer_1', 'layer_2', 'layer_3', 'layer_4',
    'layer_5', 'layer_6', 'layer_7', 'layer_8', 'layer_9', 'layer_10',
    'layer_11', 'layer_12', 'layer_13', 'layer_14', 'layer_15', 'layer_16',
    'layer_17', 'layer_18', 'layer_19', 'layer_20', 'layer_21', 'layer_22',
    'layer_23', 'layer_24', 'layer_25', 'layer_26', 'layer_27', 'layer_28',
    'layer_29', 'layer_30'
]

_ROW_ONE_TEXT_LAYER = [
    'text_layer1',  # layer_id
    '94',  # font_size
    '50',  # color_r
    '60',  # color_g
    '251',  # color_b
    '252',  # position_x
    '253',  # position_y
    '東京で今最も売れているモノは？'  # text_content
]

_ROW_TWO_TEXT_LAYER = [
    'buy_me_text',  # layer_id
    '48',  # font_size
    '255',  # color_r
    '255',  # color_g
    '255',  # color_b
    '232',  # position_x
    '158',  # position_y
    'レディースファッションおすすめ'  # text_content
]

_TEXT_LAYER_WORKSHEET_VALUES = [_TAB_HEADER_TEXT_LAYER,
                                _ROW_ONE_TEXT_LAYER,
                                _ROW_TWO_TEXT_LAYER]

_TEXT_LAYER_1 = text_layer.TextLayer(
    layer_id='text_layer1',
    position_x=252,
    position_y=253,
    font_size=94,
    font_file_path=_DEFAULT_FONT_FILE_PATH,
    color_r=50,
    color_g=60,
    color_b=251,
    text_content='東京で今最も売れているモノは？')

_TEXT_LAYER_2 = text_layer.TextLayer(
    layer_id='buy_me_text',
    position_x=232,
    position_y=158,
    font_size=48,
    font_file_path=_DEFAULT_FONT_FILE_PATH,
    color_r=255,
    color_g=255,
    color_b=255,
    text_content='レディースファッションおすすめ')

_ROW_ONE_IMAGE_LAYER = [
    'background_square',  # layer_id
    '1200',  # width
    '1100',  # height
    '0',  # position_x
    '1',  # position_y
    'background.png'  # filename
]

_ROW_TWO_IMAGE_LAYER = [
    'blue_bird',  # layer_id
    '1500',  # width
    '1600',  # height
    '500',  # position_x
    '400',  # position_y
    'blue_bird.png'  # filename
]

_IMAGE_LAYER_WORKSHEET_VALUES = [_TAB_HEADER_IMAGE_LAYER,
                                 _ROW_ONE_IMAGE_LAYER,
                                 _ROW_TWO_IMAGE_LAYER]

_IMAGE_LAYER_1 = image_layer.ImageLayer(
    layer_id='background_square',
    position_x=0,
    position_y=1,
    width=1200,
    height=1100,
    file_path=f'{_IMAGE_DIRECTORY_PATH}/background.png')

_IMAGE_LAYER_2 = image_layer.ImageLayer(
    layer_id='blue_bird',
    position_x=500,
    position_y=400,
    width=1500,
    height=1600,
    file_path=f'{_IMAGE_DIRECTORY_PATH}/blue_bird.png')

_CANVAS_WIDE = canvas_lib.Canvas(
    canvas_id='canvas_wide', width=1200, height=1100)
_CANVAS_NARROW = canvas_lib.Canvas(
    canvas_id='canvas_narrow', width=800, height=600)

_ONE_ROW_CANVAS = [
    'canvas_square',  # canvas_id
    '1200',  # width
    '628'  # height
]

_CANVAS_OBJECT_CANVAS_SQUARE = canvas_lib.Canvas(
    canvas_id='canvas_square', width=1200, height=628)


_NUMBER_OF_COLUMNS_IN_LAYOUT = 32

_LAYOUT_FIRST_THREE_VALUE = [
    'template_c_square2',  # output_filename
    'canvas_square',  #  canvas id
    'background_square',  # layer_1
]

_ONE_VALID_ROW_LAYOUT_ONE_LAYER = _LAYOUT_FIRST_THREE_VALUE + [''] * (
    _NUMBER_OF_COLUMNS_IN_LAYOUT - len(_LAYOUT_FIRST_THREE_VALUE))

_MAX_NUMBER_LAYERS = _NUMBER_OF_COLUMNS_IN_LAYOUT - 2

_LAYOUT_ROW_ONE_IMAGE_ONE_TEXT_LAYER = [
    'template_c_square2',  # output_filename
    'canvas_square',  #  canvas id
    'background_square',  # layer_1
    'buy_me_text',  # layer_2
]

_LAYOUT_ROW_ONE_IMAGE_ONE_TEXT_LAYER = _LAYOUT_ROW_ONE_IMAGE_ONE_TEXT_LAYER + [
    ''
] * (
    _NUMBER_OF_COLUMNS_IN_LAYOUT - len(_LAYOUT_ROW_ONE_IMAGE_ONE_TEXT_LAYER))

# To test that we can handle a row with all the layers filed.
_VALID_ROW_LAYOUT_WITH_MAX_LAYERS = [
    'template_c_square2',  # output_filename
    'canvas_square',  #  canvas id
] + ['background_square'] * _MAX_NUMBER_LAYERS


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

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_text_layers_two_rows_become_two_text_layer_objects(
      self, mock_gspead, mock_colab_auth, mock_google_auth):
    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)
    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.return_value = _TEXT_LAYER_WORKSHEET_VALUES

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)

    actual_text_layers = sheet_loader.get_text_layers()

    expected_text_layers = [_TEXT_LAYER_2, _TEXT_LAYER_1]
    self.assertCountEqual(expected_text_layers, actual_text_layers)

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_text_layers_no_layers_info_return_empty_array(
      self, mock_gspead, mock_colab_auth, mock_google_auth):

    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)
    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.return_value = [
        _TAB_HEADER_TEXT_LAYER
    ]

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)

    actual_text_layers = sheet_loader.get_text_layers()

    expected_text_layers = []
    self.assertEqual(expected_text_layers, actual_text_layers)

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_text_layers_no_text_layer_tab_raises_worksheet_not_found(
      self, mock_gspead, mock_colab_auth, mock_google_auth):

    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)
    mock_gspead.return_value.open_by_url.return_value.worksheet.side_effect = gspread_exceptions.WorksheetNotFound(
    )

    with self.assertRaises(gspread_exceptions.WorksheetNotFound):
      sheet_loader = spreadsheet_loader.SpreadSheetLoader(
          _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)
      sheet_loader.get_text_layers()

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_text_layer_incomplete_text_layer_in_sheet_raises_value_error(
      self, mock_gspead, mock_colab_auth, mock_google_auth):

    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)
    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.return_value = [
        _TAB_HEADER_TEXT_LAYER,
        [
            'buy_me_text',  # layer_id
            '48',  # font_size
            '255',  # color_r
            '255',  # color_g
            '255',  # color_b
            '232',  # position_x
                    # position_y MISSING!!!
            'レディースファッションおすすめ'  # text_content
        ]
    ]

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)

    with self.assertRaises(ValueError):
      sheet_loader.get_text_layers()

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_image_layers_no_image_layer_tab_raises_worksheet_not_found(
      self, mock_gspead, mock_colab_auth, mock_google_auth):

    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)
    mock_gspead.return_value.open_by_url.return_value.worksheet.side_effect = gspread_exceptions.WorksheetNotFound(
    )

    with self.assertRaises(gspread_exceptions.WorksheetNotFound):
      sheet_loader = spreadsheet_loader.SpreadSheetLoader(
          _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)
      sheet_loader.get_image_layers()

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_image_layers_tab_has_header_only_but_no_values_return_empty_arr(
      self, mock_gspead, mock_colab_auth, mock_google_auth):

    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)
    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.return_value = [
        _TAB_HEADER_IMAGE_LAYER
    ]

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)
    actual_text_layers = sheet_loader.get_text_layers()

    self.assertEqual([], actual_text_layers)

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_image_layer_incomplete_image_layer_in_sheet_raises_value_error(
      self, mock_gspead, mock_colab_auth, mock_google_auth):

    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)
    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.return_value = [
        _TAB_HEADER_IMAGE_LAYER,
        [
            'background_square',  # layer_id
            '1200',  # width
            '1100',  # height
            '0',  # position_x
            '1',  # position_y
                  # filename MISSING!
        ]
    ]

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)

    with self.assertRaises(ValueError):
      sheet_loader.get_image_layers()

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_layer_images_two_valid_rows_in_sheet_result_two_valid_objects(
      self, mock_gspead, mock_colab_auth, mock_google_auth):

    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)
    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.return_value = _IMAGE_LAYER_WORKSHEET_VALUES

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)

    actual_image_layers = sheet_loader.get_image_layers()

    expected_image_layers = [_IMAGE_LAYER_2, _IMAGE_LAYER_1]
    self.assertCountEqual(expected_image_layers, actual_image_layers)

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_canvases_no_canvas_tab_raises_worksheet_not_found(
      self, mock_gspead, mock_colab_auth, mock_google_auth):

    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)
    mock_gspead.return_value.open_by_url.return_value.worksheet.side_effect = gspread_exceptions.WorksheetNotFound(
    )

    with self.assertRaises(gspread_exceptions.WorksheetNotFound):
      sheet_loader = spreadsheet_loader.SpreadSheetLoader(
          _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)
      sheet_loader.get_canvases()

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_canvases_no_rows_in_tab_return_empty_array(
      self, mock_gspead, mock_colab_auth, mock_google_auth):

    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)
    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.return_value = [
        _TAB_HEADER_CANVAS
    ]

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)

    actual_image_layers = sheet_loader.get_canvases()

    self.assertEqual([], actual_image_layers)

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_canvases_information_missing_from_row_raises_value_error(
      self, mock_gspead, mock_colab_auth, mock_google_auth):

    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)
    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.return_value = [
        _TAB_HEADER_CANVAS,
        [
            'canvas_wide',  # canvas_id
            '1200',  # width
            '',  # height Missing!
        ]
    ]

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)

    with self.assertRaises(ValueError):
      sheet_loader.get_canvases()

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_canvases_tab_has_two_valid_rows_returns_two_valid_canvases(
      self, mock_gspead, mock_colab_auth, mock_google_auth):

    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)
    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.return_value = [
        _TAB_HEADER_CANVAS,
        [
            'canvas_wide',  # canvas_id
            '1200',  # width
            '1100',  # height
        ],
        [
            'canvas_narrow',  # canvas_id
            '800',  # width
            '600',  # height
        ]
    ]

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)
    actual_canvases = sheet_loader.get_canvases()

    self.assertCountEqual(actual_canvases, [_CANVAS_WIDE, _CANVAS_NARROW])

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_layouts_no_layout_sheet_raises_worksheet_error(
      self, mock_gspead, mock_colab_auth, mock_google_auth):

    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)
    mock_gspead.return_value.open_by_url.return_value.worksheet.side_effect = gspread_exceptions.WorksheetNotFound(
    )

    with self.assertRaises(gspread_exceptions.WorksheetNotFound):
      sheet_loader = spreadsheet_loader.SpreadSheetLoader(
          _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)
      sheet_loader.get_layouts()

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_layouts_no_information_in_layout_sheet_raises_value_error(
      self, mock_gspead, mock_colab_auth, mock_google_auth):
    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)
    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.return_value = []

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)

    with self.assertRaises(ValueError):
      sheet_loader.get_layouts()

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_layouts_no_layers_info_raises_value_error(
      self, mock_gspead, mock_colab_auth, mock_google_auth):
    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)

    layout_row_with_no_layer_info = ['template_c_square', 'canvas_square']

    layout_row_with_no_layer_info = layout_row_with_no_layer_info + [''] * (
        _NUMBER_OF_COLUMNS_IN_LAYOUT - len(layout_row_with_no_layer_info))

    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.side_effect = [
        # Layout layer
        [
            _TAB_HEADER_LAYOUT,
            layout_row_with_no_layer_info  # No layer info --> error
        ],
        #  TEXT LAYER
        [
            _TAB_HEADER_TEXT_LAYER,
            _ROW_ONE_TEXT_LAYER
        ],
        # IMAGE LAYER
        [
            _TAB_HEADER_IMAGE_LAYER,
            _ROW_ONE_IMAGE_LAYER
        ],
        # CANVAS
        [
            _TAB_HEADER_CANVAS,
            _ONE_ROW_CANVAS
        ]
    ]
    expected_assertion_message = ('A layout row should have at least the three '
                                  'first columns with values. We need to have '
                                  'at least one layer. Please check row ')

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)

    with self.assertRaises(ValueError) as error:
      sheet_loader.get_layouts()
    self.assertTrue(
        str(error.exception).startswith(expected_assertion_message))

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_layouts_layer_canvas_id_is_not_found_in_canvas_tab_raises_error(
      self, mock_gspead, mock_colab_auth, mock_google_auth):
    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)

    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.side_effect = [
        # Layout layer
        [
            _TAB_HEADER_LAYOUT,
            # canvas id is 'canvas_square' and is not present in the canvas
            # tab -> error
            _ONE_VALID_ROW_LAYOUT_ONE_LAYER
        ],
        #  TEXT LAYER
        [
            _TAB_HEADER_TEXT_LAYER,
            _ROW_ONE_TEXT_LAYER,
        ],
        # IMAGE LAYER
        [_TAB_HEADER_IMAGE_LAYER, _ROW_ONE_IMAGE_LAYER],
        # CANVAS
        [
            _TAB_HEADER_CANVAS,
            [
                'canvas_different',  # canvas_id not present in layout
                '1200',  # width
                '628'  # height
            ]
        ]
    ]

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)

    with self.assertRaises(ValueError) as error:
      sheet_loader.get_layouts()
    self.assertEqual(
        'Failed to create a layout object from row number 2. Please check the '
        'spreadsheet\'s LAYOUT tab on that particular row.',
        str(error.exception))

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_layouts_layer_1_not_be_found_in_image_or_text_layer_raises_error(
      self, mock_gspead, mock_colab_auth, mock_google_auth):

    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)

    layout_row = [
        'template_c_square2',  # output_filename
        'canvas_square',  #  canvas id
        'blue_jeans',  # layer_1 not found in text or image layers!!
    ]

    remaining_empty_rows = [''] * (
        _NUMBER_OF_COLUMNS_IN_LAYOUT - len(layout_row))
    layout_row = layout_row + remaining_empty_rows

    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.side_effect = [
        # Layout layer
        [
            _TAB_HEADER_LAYOUT,
            layout_row  # layer_1 not found in text or image layers!!
        ],
        #  TEXT LAYER
        [
            _TAB_HEADER_TEXT_LAYER,
            _ROW_ONE_TEXT_LAYER,  # layer_id='text_layer1'
        ],
        # IMAGE LAYER
        [
            _TAB_HEADER_IMAGE_LAYER,
            _ROW_ONE_IMAGE_LAYER  # layer_id=background_square
        ],
        # CANVAS
        [
            _TAB_HEADER_CANVAS,
            _ONE_ROW_CANVAS
        ]
    ]

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)
    with self.assertRaises(ValueError) as error:
      sheet_loader.get_layouts()
    self.assertEqual(
        'Failed to create a layout object from row number 2. Please check the '
        'spreadsheet\'s LAYOUT tab on that particular row.',
        str(error.exception))

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_layouts_layer_1_is_found_twice_in_image_layers_raises_error(
      self, mock_gspead, mock_colab_auth, mock_google_auth):
    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)

    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.side_effect = [
        # Layout layer
        [
            _TAB_HEADER_LAYOUT,
            _ONE_VALID_ROW_LAYOUT_ONE_LAYER  # layer_1 = background_square
        ],
        #  TEXT LAYER
        [
            _TAB_HEADER_TEXT_LAYER,
            _ROW_ONE_TEXT_LAYER,
        ],
        # IMAGE LAYER
        [
            _TAB_HEADER_IMAGE_LAYER,
            _ROW_ONE_IMAGE_LAYER,  # layer_id = background_square!
            _ROW_ONE_IMAGE_LAYER   # layer_id = background_square! twice!
        ],
        # CANVAS
        [
            _TAB_HEADER_CANVAS,
            _ONE_ROW_CANVAS
        ]
    ]

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)
    with self.assertRaises(ValueError) as error:
      sheet_loader.get_layouts()
    self.assertEqual(
        'Failed to create a layout object from row number 2. Please check the '
        'spreadsheet\'s LAYOUT tab on that particular row.',
        str(error.exception))

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_layouts_layer_1_is_found_twice_in_text_layers_raises_error(
      self, mock_gspead, mock_colab_auth, mock_google_auth):
    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)

    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.side_effect = [
        # Layout layer
        [
            _TAB_HEADER_LAYOUT,
            # layer_1 = background_square - image layer
            # layer_2 = buy_me_text - text layer found twice in text layer!
            _LAYOUT_ROW_ONE_IMAGE_ONE_TEXT_LAYER
        ],
        #  TEXT LAYER
        [
            _TAB_HEADER_TEXT_LAYER,
            _ROW_ONE_TEXT_LAYER,
            _ROW_TWO_TEXT_LAYER,  # layer id buy_me_text
            _ROW_TWO_TEXT_LAYER  # layer id buy_me_text twice! -> error
        ],
        # IMAGE LAYER
        [
            _TAB_HEADER_IMAGE_LAYER,
            _ROW_ONE_IMAGE_LAYER,  # layer_id = background_square!
        ],
        # CANVAS
        [
            _TAB_HEADER_CANVAS,
            _ONE_ROW_CANVAS
        ]
    ]

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)
    with self.assertRaises(ValueError) as error:
      sheet_loader.get_layouts()
    self.assertEqual(
        'Failed to create a layout object from row number 2. Please check the '
        'spreadsheet\'s LAYOUT tab on that particular row.',
        str(error.exception))

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_layouts_layer_1_is_found_in_text_layer_and_image_layer_raise(
      self, mock_gspead, mock_colab_auth, mock_google_auth):
    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)

    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.side_effect = [
        # Layout layer
        [
            _TAB_HEADER_LAYOUT,
            # layer 1 background_square is found in image and text layer
            _LAYOUT_ROW_ONE_IMAGE_ONE_TEXT_LAYER
        ],
        #  TEXT LAYER
        [
            _TAB_HEADER_TEXT_LAYER,
            [
                'background_square',  # layer_id
                '94',  # font_size
                '50',  # color_r
                '60',  # color_g
                '251',  # color_b
                '252',  # position_x
                '253',  # position_y
                'Nice background!'  # text_content
            ]
        ],
        # IMAGE LAYER
        [
            _TAB_HEADER_IMAGE_LAYER,
            _ROW_ONE_IMAGE_LAYER,  # layer_id = background_square!
        ],
        # CANVAS
        [
            _TAB_HEADER_CANVAS,
            _ONE_ROW_CANVAS
        ]
    ]

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)
    with self.assertRaises(ValueError) as error:
      sheet_loader.get_layouts()
    self.assertEqual(
        'Failed to create a layout object from row number 2. Please check the '
        'spreadsheet\'s LAYOUT tab on that particular row.',
        str(error.exception))

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_layouts_two_valid_layouts_records_return_two_valid_layouts(
      self, mock_gspead, mock_colab_auth, mock_google_auth):
    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)

    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.side_effect = [
        # Layout layer
        [
            _TAB_HEADER_LAYOUT,
            _LAYOUT_ROW_ONE_IMAGE_ONE_TEXT_LAYER
        ],
        #  TEXT LAYER
        [
            _TAB_HEADER_TEXT_LAYER,
            _ROW_ONE_TEXT_LAYER,
            _ROW_TWO_TEXT_LAYER
        ],
        # IMAGE LAYER
        [
            _TAB_HEADER_IMAGE_LAYER,
            _ROW_ONE_IMAGE_LAYER,
        ],
        # CANVAS
        [
            _TAB_HEADER_CANVAS,
            _ONE_ROW_CANVAS
        ]
    ]

    expected_layouts = [
        layout.Layout(
            canvas=_CANVAS_OBJECT_CANVAS_SQUARE,
            output_filename='template_c_square2',
            layers=[_IMAGE_LAYER_1, _TEXT_LAYER_2])
    ]

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)
    actual_layouts = sheet_loader.get_layouts()

    self.assertEqual(expected_layouts, actual_layouts)

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_layouts_more_than_one_canvas_id_match_raises_value_error(
      self, mock_gspead, mock_colab_auth, mock_google_auth):

    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)

    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.side_effect = [
        # Layout layer
        [
            _TAB_HEADER_LAYOUT,
            # canvas_id=canvas_square and will match twice in the canvas tab.
            _LAYOUT_ROW_ONE_IMAGE_ONE_TEXT_LAYER
        ],
        #  TEXT LAYER
        [
            _TAB_HEADER_TEXT_LAYER,
            _ROW_ONE_TEXT_LAYER,
            _ROW_TWO_TEXT_LAYER],
        # IMAGE LAYER
        [
            _TAB_HEADER_IMAGE_LAYER,
            _ROW_ONE_IMAGE_LAYER,
        ],
        # CANVAS
        [
            _TAB_HEADER_CANVAS,
            _ONE_ROW_CANVAS,  # canvas_id=canvas_square
            _ONE_ROW_CANVAS   # canvas_id=canvas_square twice!
        ]
    ]

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(_SHEET_URL,
                                                        _IMAGE_DIRECTORY_PATH,
                                                        _DEFAULT_FONT_FILE_PATH)

    with self.assertRaises(ValueError) as error:
      sheet_loader.get_layouts()
    self.assertEqual(
        'Failed to create a layout object from row number 2. Please check the '
        'spreadsheet\'s LAYOUT tab on that particular row.',
        str(error.exception))

  @mock.patch.object(default_auth, 'default', autospec=True)
  @mock.patch.object(colab_auth, 'authenticate_user', autospec=True)
  @mock.patch.object(gspread, 'authorize', autospec=True)
  def test_get_layouts_with_max_number_layers_to_test_limits(
      self, mock_gspead, mock_colab_auth, mock_google_auth):
    mock_colab_auth.return_value = None
    mock_google_auth.return_value = (mock.Mock(), None)

    mock_gspead.return_value.open_by_url.return_value.worksheet.return_value.get_all_values.side_effect = [
        # Layout layer
        [
            _TAB_HEADER_LAYOUT,
            _VALID_ROW_LAYOUT_WITH_MAX_LAYERS
        ],
        #  TEXT LAYER
        [
            _TAB_HEADER_TEXT_LAYER,
            _ROW_ONE_TEXT_LAYER,
            _ROW_TWO_TEXT_LAYER
        ],
        # IMAGE LAYER
        [
            _TAB_HEADER_IMAGE_LAYER,
            _ROW_ONE_IMAGE_LAYER,
        ],
        # CANVAS
        [
            _TAB_HEADER_CANVAS,
            _ONE_ROW_CANVAS
        ]
    ]

    expected_layouts = [
        layout.Layout(
            canvas=_CANVAS_OBJECT_CANVAS_SQUARE,
            output_filename='template_c_square2',
            layers=[_IMAGE_LAYER_1] * _MAX_NUMBER_LAYERS)
    ]

    sheet_loader = spreadsheet_loader.SpreadSheetLoader(
        _SHEET_URL, _IMAGE_DIRECTORY_PATH, _DEFAULT_FONT_FILE_PATH)
    actual_layouts = sheet_loader.get_layouts()

    self.assertEqual(expected_layouts, actual_layouts)

if __name__ == '__main__':
  absltest.main()

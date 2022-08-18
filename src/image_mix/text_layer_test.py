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

"""Tests for text_layer."""

from image_mix import text_layer as text_layer_lib
from absl.testing import absltest


_DUMMY_LAYER_ID = 'layer_id_1'
_DUMMY_FONT_SIZE = 12
_DUMMY_FONT_FILE_PATH = 'fonts/dummy-font.ttf'
_DUMMY_COLOR_R = 199
_DUMMY_COLOR_G = 20
_DUMMY_COLOR_B = 10
_DUMMY_POSITION_X = 100
_DUMMY_POSITION_Y = 200
_DUMMY_TEXT_CONTENT = 'Buy it!'


class TextLayerTest(absltest.TestCase):

  def test_text_layer_constructor_produces_correct_values(self):

    text_layer = text_layer_lib.TextLayer(
        layer_id=_DUMMY_LAYER_ID,
        font_size=_DUMMY_FONT_SIZE,
        font_file_path=_DUMMY_FONT_FILE_PATH,
        color_r=_DUMMY_COLOR_R,
        color_g=_DUMMY_COLOR_G,
        color_b=_DUMMY_COLOR_B,
        position_x=_DUMMY_POSITION_X,
        position_y=_DUMMY_POSITION_Y,
        text_content=_DUMMY_TEXT_CONTENT)

    self.assertEqual(_DUMMY_LAYER_ID, text_layer.layer_id)
    self.assertEqual(_DUMMY_FONT_SIZE, text_layer.font_size)
    self.assertEqual(_DUMMY_FONT_FILE_PATH, text_layer.font_file_path)
    self.assertEqual(_DUMMY_COLOR_R, text_layer.color_r)
    self.assertEqual(_DUMMY_COLOR_G, text_layer.color_g)
    self.assertEqual(_DUMMY_COLOR_B, text_layer.color_b)
    self.assertEqual(_DUMMY_POSITION_X, text_layer.position_x)
    self.assertEqual(_DUMMY_POSITION_Y, text_layer.position_y)
    self.assertEqual(_DUMMY_TEXT_CONTENT, text_layer.text_content)

  def test_text_layer_font_file_path_empty_raises_value_error(self):

    with self.assertRaises(ValueError):
      text_layer_lib.TextLayer(
          layer_id=_DUMMY_LAYER_ID,
          font_file_path='',
          font_size=_DUMMY_FONT_SIZE,
          color_r=_DUMMY_COLOR_R,
          color_g=_DUMMY_COLOR_G,
          color_b=_DUMMY_COLOR_B,
          position_x=_DUMMY_POSITION_X,
          position_y=_DUMMY_POSITION_Y,
          text_content=_DUMMY_TEXT_CONTENT)

  def test_text_layer_color_r_more_than_255_raises_value_error(self):

    with self.assertRaises(ValueError):
      text_layer_lib.TextLayer(
          layer_id=_DUMMY_LAYER_ID,
          font_size=_DUMMY_FONT_SIZE,
          font_file_path=_DUMMY_FONT_FILE_PATH,
          color_r=260,
          color_g=_DUMMY_COLOR_G,
          color_b=_DUMMY_COLOR_B,
          position_x=_DUMMY_POSITION_X,
          position_y=_DUMMY_POSITION_Y,
          text_content=_DUMMY_TEXT_CONTENT)

  def test_text_layer_text_content_empty_raises_value_error(self):

    with self.assertRaises(ValueError):
      text_layer_lib.TextLayer(
          layer_id=_DUMMY_LAYER_ID,
          font_size=_DUMMY_FONT_SIZE,
          font_file_path=_DUMMY_FONT_FILE_PATH,
          color_r=_DUMMY_COLOR_R,
          color_g=_DUMMY_COLOR_G,
          color_b=_DUMMY_COLOR_B,
          position_x=_DUMMY_POSITION_X,
          position_y=_DUMMY_POSITION_Y,
          text_content='')

  def test_text_layer_layer_id_empty_raises_value_error(self):

    with self.assertRaises(ValueError):
      text_layer_lib.TextLayer(
          layer_id='',
          font_size=_DUMMY_FONT_SIZE,
          font_file_path=_DUMMY_FONT_FILE_PATH,
          color_r=_DUMMY_COLOR_R,
          color_g=_DUMMY_COLOR_G,
          color_b=_DUMMY_COLOR_B,
          position_x=_DUMMY_POSITION_X,
          position_y=_DUMMY_POSITION_Y,
          text_content=_DUMMY_TEXT_CONTENT)

  def test_rgb_color_returns_rgb_color_as_tuple(self):
    text_layer = text_layer_lib.TextLayer(
        layer_id=_DUMMY_LAYER_ID,
        font_size=_DUMMY_FONT_SIZE,
        font_file_path=_DUMMY_FONT_FILE_PATH,
        color_r=_DUMMY_COLOR_R,
        color_g=_DUMMY_COLOR_G,
        color_b=_DUMMY_COLOR_B,
        position_x=_DUMMY_POSITION_X,
        position_y=_DUMMY_POSITION_Y,
        text_content=_DUMMY_TEXT_CONTENT)

    expected_rgb_color = (_DUMMY_COLOR_R, _DUMMY_COLOR_G, _DUMMY_COLOR_B)
    self.assertEqual(expected_rgb_color, text_layer.rgb_color())


if __name__ == '__main__':
  absltest.main()

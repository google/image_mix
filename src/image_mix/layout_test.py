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

"""Tests for layout."""

from image_mix import canvas as canvas_lib
from image_mix import image_layer as image_layer_lib
from image_mix import layout as layout_lib
from image_mix import text_layer as text_layer_lib
from absl.testing import absltest


OUTPUT_FILENAME = 'creative.jpg'

TEXT_LAYER_ID_1 = 'layer_id_01'
IMAGE_LAYER_ID_1 = 'layer_id_02'
TEXT_LAYER_ID_1_FONT_SIZE = 12
FONT_FILE_PATH = 'fonts/dummy-font.ttf'
TEXT_LAYER_ID_1_COLOR_R = 199
TEXT_LAYER_ID_1_COLOR_G = 10
TEXT_LAYER_ID_1_COLOR_B = 11
TEXT_LAYER_ID_1_POSITION_X = 100
TEXT_LAYER_ID_1_POSITION_Y = 200
TEXT_LAYER_ID_1_CONTENT = 'Buy it!'

TEXT_LAYER_1 = text_layer_lib.TextLayer(
    layer_id=TEXT_LAYER_ID_1,
    font_size=TEXT_LAYER_ID_1_FONT_SIZE,
    font_file_path=FONT_FILE_PATH,
    color_r=TEXT_LAYER_ID_1_COLOR_R,
    color_g=TEXT_LAYER_ID_1_COLOR_G,
    color_b=TEXT_LAYER_ID_1_COLOR_B,
    position_x=TEXT_LAYER_ID_1_POSITION_X,
    position_y=TEXT_LAYER_ID_1_POSITION_Y,
    text_content=TEXT_LAYER_ID_1_CONTENT)

IMAGE_LAYER_1_WIDTH = 1000
IMAGE_LAYER_1_HEIGHT = 2000
IMAGE_LAYER_1_POSITION_X = 100
IMAGE_LAYER_1_POSITION_Y = 200
IMAGE_LAYER_1_FILE_PATH = 'image.jpg'

IMAGE_LAYER_1 = image_layer_lib.ImageLayer(
    layer_id=IMAGE_LAYER_ID_1,
    width=IMAGE_LAYER_1_WIDTH,
    height=IMAGE_LAYER_1_HEIGHT,
    position_x=IMAGE_LAYER_1_POSITION_X,
    position_y=IMAGE_LAYER_1_POSITION_Y,
    file_path=IMAGE_LAYER_1_FILE_PATH)

DUMMY_CANVAS = canvas_lib.Canvas(
    canvas_id='canvas_id_1', width=1000, height=200)


class LayoutTest(absltest.TestCase):

  def test_layout_object_creation(self):
    layout = layout_lib.Layout(
        canvas=DUMMY_CANVAS,
        output_filename=OUTPUT_FILENAME,
        layers=[TEXT_LAYER_1, IMAGE_LAYER_1])

    self.assertEqual(DUMMY_CANVAS, layout.canvas)
    self.assertEqual(OUTPUT_FILENAME, layout.output_filename)
    self.assertEqual(TEXT_LAYER_1, layout.layers[0])
    self.assertEqual(IMAGE_LAYER_1, layout.layers[1])

  def test_layout_object_creation_output_filename_empty_raises_valueerror(self):
    with self.assertRaises(ValueError):
      layout_lib.Layout(
          canvas=DUMMY_CANVAS,
          output_filename='',
          layers=[TEXT_LAYER_1, IMAGE_LAYER_1])

  def test_layout_creation_empty_layers_raises_value_error(self):
    with self.assertRaises(ValueError):
      layout_lib.Layout(
          canvas=DUMMY_CANVAS, output_filename=OUTPUT_FILENAME, layers=[])


if __name__ == '__main__':
  absltest.main()

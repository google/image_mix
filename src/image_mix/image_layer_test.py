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

from image_mix import image_layer as image_layer_lib
from absl.testing import absltest


_DUMMY_LAYER_ID = 'layer_123'
_DUMMY_WIDTH = 1000
_DUMMY_HEIGHT = 2000
_DUMMY_POSITION_X = 100
_DUMMY_POSITION_Y = 200
_DUMMY_FILE_PATH = 'assets/image.jpg'


class ImageLayerTest(absltest.TestCase):

  def test_image_layer_building_object(self):
    image_layer = image_layer_lib.ImageLayer(
        layer_id=_DUMMY_LAYER_ID,
        width=_DUMMY_WIDTH,
        height=_DUMMY_HEIGHT,
        position_x=_DUMMY_POSITION_X,
        position_y=_DUMMY_POSITION_Y,
        file_path=_DUMMY_FILE_PATH)

    self.assertEqual(_DUMMY_LAYER_ID, image_layer.layer_id)
    self.assertEqual(_DUMMY_WIDTH, image_layer.width)
    self.assertEqual(_DUMMY_HEIGHT, image_layer.height)
    self.assertEqual(_DUMMY_POSITION_X, image_layer.position_x)
    self.assertEqual(_DUMMY_POSITION_Y, image_layer.position_y)
    self.assertEqual(_DUMMY_FILE_PATH, image_layer.file_path)

  def test_image_layer_negative_x_position_raises_value_error(self):
    with self.assertRaises(ValueError):
      image_layer_lib.ImageLayer(
          layer_id=_DUMMY_LAYER_ID,
          width=_DUMMY_WIDTH,
          height=_DUMMY_HEIGHT,
          position_x=-100,
          position_y=_DUMMY_POSITION_Y,
          file_path=_DUMMY_FILE_PATH)

  def test_image_layer_empty_image_file_raises_value_error(self):
    with self.assertRaises(ValueError):
      image_layer_lib.ImageLayer(
          layer_id=_DUMMY_LAYER_ID,
          width=_DUMMY_WIDTH,
          height=_DUMMY_HEIGHT,
          position_x=_DUMMY_POSITION_X,
          position_y=_DUMMY_POSITION_Y,
          file_path='')

  def test_image_layer_empty_layer_id_raises_value_error(self):
    with self.assertRaises(ValueError):
      image_layer_lib.ImageLayer(
          layer_id='',
          width=_DUMMY_WIDTH,
          height=_DUMMY_HEIGHT,
          position_x=_DUMMY_POSITION_X,
          position_y=_DUMMY_POSITION_Y,
          file_path=_DUMMY_FILE_PATH)

  def test_size_returns_size_as_tuple(self):
    image_layer = image_layer_lib.ImageLayer(
        layer_id=_DUMMY_LAYER_ID,
        width=_DUMMY_WIDTH,
        height=_DUMMY_HEIGHT,
        position_x=_DUMMY_POSITION_X,
        position_y=_DUMMY_POSITION_Y,
        file_path=_DUMMY_FILE_PATH)

    expected_size = (_DUMMY_WIDTH, _DUMMY_HEIGHT)
    self.assertEqual(expected_size, image_layer.size())


if __name__ == '__main__':
  absltest.main()


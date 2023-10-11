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

"""Tests for base_layer.py."""
from image_mix import base_layer
from absl.testing import absltest

_DUMMY_LAYER_ID = 'dummy_layer'
_DUMMY_POSITION_X = 100
_DUMMY_POSITION_Y = 200


class BaseLayerTest(absltest.TestCase):

  def test_base_layer_building_object(self):
    layer = base_layer.BaseLayer(
        layer_id=_DUMMY_LAYER_ID,
        position_x=_DUMMY_POSITION_X,
        position_y=_DUMMY_POSITION_Y)

    self.assertEqual(_DUMMY_LAYER_ID, layer.layer_id)
    self.assertEqual(_DUMMY_POSITION_X, layer.position_x)
    self.assertEqual(_DUMMY_POSITION_Y, layer.position_y)

  def test_base_layer_empty_layer_id_raises_value_error(self):
    with self.assertRaises(ValueError):
      base_layer.BaseLayer(
          layer_id='',
          position_x=_DUMMY_POSITION_Y,
          position_y=_DUMMY_POSITION_Y)

  def test_base_layer_negative_position_raises_value_error(self):
    with self.assertRaises(ValueError):
      base_layer.BaseLayer(
          layer_id=_DUMMY_LAYER_ID, position_x=_DUMMY_POSITION_X, position_y=-1)

  def test_position_returns_position_as_tuple(self):
    layer = base_layer.BaseLayer(
        layer_id=_DUMMY_LAYER_ID,
        position_x=_DUMMY_POSITION_X,
        position_y=_DUMMY_POSITION_Y)

    expected_position = (_DUMMY_POSITION_X, _DUMMY_POSITION_Y)
    self.assertEqual(expected_position, layer.position())


if __name__ == '__main__':
  absltest.main()

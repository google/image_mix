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

"""Tests for layer_mixer.py."""
from unittest import mock

from image_mix import image_layer
from image_mix import layer_mixer
from image_mix import text_layer
from absl.testing import absltest

_DUMMY_IMAGE_WIDTH = 1500
_DUMMY_IMAGE_HEIGHT = 3000
_DUMMY_IMAGE_LAYER = image_layer.ImageLayer(
    layer_id='dummy-image',
    position_x=100,
    position_y=200,
    width=1000,
    height=2000,
    file_path='dummy/image.png')
_DUMMY_TEXT_LAYER = text_layer.TextLayer(
    layer_id='dummy-text',
    position_x=300,
    position_y=400,
    font_size=12,
    font_file_path='fonts/a_font.ttf',
    color_r=1,
    color_g=2,
    color_b=3,
    text_content='dummy-text')


class LayerMixerTest(absltest.TestCase):

  def setUp(self):
    super(LayerMixerTest, self).setUp()
    self._mock_image = self.enter_context(
        mock.patch(
            'google3.corp.gtech.ads.solutions.image_mix.src.image_mix.layer_mixer.Image',
            autospec=True))
    self._mock_image_draw = self.enter_context(
        mock.patch(
            'google3.corp.gtech.ads.solutions.image_mix.src.image_mix.layer_mixer.ImageDraw',
            autospec=True))
    self._mock_image_font = self.enter_context(
        mock.patch(
            'google3.corp.gtech.ads.solutions.image_mix.src.image_mix.layer_mixer.ImageFont',
            autospec=True))
    self._layer_mixer = layer_mixer.LayerMixer(
        (_DUMMY_IMAGE_WIDTH, _DUMMY_IMAGE_HEIGHT))

  def test_image_is_created_with_given_size(self):
    self._mock_image.new.assert_called_with(
        'RGBA', (_DUMMY_IMAGE_WIDTH, _DUMMY_IMAGE_HEIGHT), (255, 255, 255, 0))

  def test_image_layer_is_added(self):
    self._layer_mixer._image = mock.MagicMock()
    self._layer_mixer.add_layers([_DUMMY_IMAGE_LAYER])

    self._mock_image.open.assert_called_once_with(_DUMMY_IMAGE_LAYER.file_path)
    self._mock_image.open.return_value.resize.assert_called_once_with(
        _DUMMY_IMAGE_LAYER.size())
    self._mock_image.alpha_composite.assert_called_once()

  def test_text_layer_is_added(self):
    self._layer_mixer.add_layers([_DUMMY_TEXT_LAYER])

    self._mock_image_font.truetype.assert_called_once_with(
        _DUMMY_TEXT_LAYER.font_file_path, _DUMMY_TEXT_LAYER.font_size)
    self._mock_image_draw.Draw.return_value.text.assert_called_once_with(
        _DUMMY_TEXT_LAYER.position(), _DUMMY_TEXT_LAYER.text_content,
        _DUMMY_TEXT_LAYER.rgb_color(), mock.ANY)

  def test_add_multiple_layers(self):
    self._layer_mixer._add_image_layer = mock.MagicMock()
    self._layer_mixer._add_text_layer = mock.MagicMock()

    layer_list_2_images_and_1_text = [
        _DUMMY_IMAGE_LAYER, _DUMMY_TEXT_LAYER, _DUMMY_IMAGE_LAYER
    ]
    self._layer_mixer.add_layers(layer_list_2_images_and_1_text)

    self.assertEqual(2, self._layer_mixer._add_image_layer.call_count)
    self.assertEqual(1, self._layer_mixer._add_text_layer.call_count)

  def test_save_image(self):
    dummy_output_path = 'dummy/creative.png'
    self._layer_mixer._image = mock.MagicMock()

    self._layer_mixer.save_image(dummy_output_path)

    self._layer_mixer._image.save.assert_called_once_with(
        dummy_output_path, quality=95, format='PNG')


if __name__ == '__main__':
  absltest.main()

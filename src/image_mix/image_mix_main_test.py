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

"""Tests for image_mix_main."""

import os
from unittest import mock

from image_mix import canvas as canvas_lib
from image_mix import image_layer
from image_mix import image_mix_main
from image_mix import layer_mixer
from image_mix import layout
from image_mix import spreadsheet_loader
from image_mix import text_layer
from absl.testing import absltest


_CANVAS_OBJECT_CANVAS_SQUARE = canvas_lib.Canvas(
    canvas_id='canvas_square', width=1200, height=628)

_IMAGE_DIRECTORY_PATH = 'My drive/IMAGEMIX/images'

_IMAGE_LAYER_1 = image_layer.ImageLayer(
    layer_id='background_square',
    position_x=0,
    position_y=1,
    width=1200,
    height=1100,
    file_path=f'{_IMAGE_DIRECTORY_PATH}/background.png')

_DEFAULT_FONT_FILE_PATH = 'fonts/dummy-font.ttf'

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

_ONE_LAYOUT_TWO_LAYERS = layout.Layout(
    canvas=_CANVAS_OBJECT_CANVAS_SQUARE,
    output_filename='template_c_square2.jpg',
    layers=[_IMAGE_LAYER_1, _TEXT_LAYER_2])

_ANOTHER_LAYOUT_TWO_LAYERS = layout.Layout(
    canvas=_CANVAS_OBJECT_CANVAS_SQUARE,
    output_filename='creative_bags.jpg',
    layers=[_IMAGE_LAYER_1, _TEXT_LAYER_2])


class ImageMixerMainTest(absltest.TestCase):

  def test_constructor_empty_url_path_raises_value_error(self):
    with self.assertRaises(ValueError):
      image_mix_main.ImageMixMain(
          spreadsheet_url='',
          output_path='~/image_mix_output',
          default_font_file_path='~/font.tff',
          image_directory_path='~/imagemix-images')

  def test_constructor_empty_image_directory_path_raises_value_error(self):
    with self.assertRaises(ValueError):
      image_mix_main.ImageMixMain(
          spreadsheet_url='http://www.google.com/skf',
          output_path='~/image_mix_output',
          default_font_file_path='~/font.tff',
          image_directory_path='')

  def test_constructor_empty_default_font_file_path_raises_value_error(self):
    with self.assertRaises(ValueError):
      image_mix_main.ImageMixMain(
          spreadsheet_url='http://www.google.com/skf',
          output_path='~/image_mix_output',
          default_font_file_path='',
          image_directory_path='~/imagemix-images')

  def test_constructor_empty_output_path_raises_value_error(self):
    with self.assertRaises(ValueError):
      image_mix_main.ImageMixMain(
          spreadsheet_url='http://www.google.com/skf',
          output_path='',
          default_font_file_path='~/font.tff',
          image_directory_path='~/imagemix-images')

  @mock.patch.object(spreadsheet_loader, 'SpreadSheetLoader', autospec=True)
  def test_constructor_invalid_spreadsheet_url_raises_value_error(
      self, mock_spreadsheet_loader):

    mock_spreadsheet_loader.side_effect = ValueError()

    with self.assertRaises(ValueError):
      image_mix_main.ImageMixMain(
          spreadsheet_url='http://invalid-url',
          output_path='~/image_mix_output',
          default_font_file_path='~/font.tff',
          image_directory_path='~/imagemix-images')

  @mock.patch.object(spreadsheet_loader, 'SpreadSheetLoader', autospec=True)
  def test_generate_creatives_spreadsheet_is_invalid_raises_value_error(
      self, mock_spreadsheet_loader):

    mock_spreadsheet_loader.return_value.get_layouts.side_effect = ValueError()

    with self.assertRaises(ValueError):
      image_mixer = image_mix_main.ImageMixMain(
          spreadsheet_url='http://www.google.com/xyz',
          output_path='~/image_mix_output',
          default_font_file_path='~/font.tff',
          image_directory_path='~/imagemix-images')
      image_mixer.generate_creatives()

  @mock.patch.object(os, 'makedirs', autospec=True)
  @mock.patch.object(layer_mixer, 'LayerMixer', autospec=True)
  @mock.patch.object(spreadsheet_loader, 'SpreadSheetLoader', autospec=True)
  def test_generate_creatives_spreadsheet_no_layout_no_image_get_written(
      self, mock_spreadsheet_loader, layer_mixer_mock, _):
    mock_spreadsheet_loader.return_value.get_layouts.return_value = []

    image_mixer = image_mix_main.ImageMixMain(
        spreadsheet_url='http://www.google.com/xyz',
        output_path='~/image_mix_output',
        default_font_file_path='~/font.tff',
        image_directory_path='~/imagemix-images')
    image_mixer.generate_creatives()

    layer_mixer_mock.save_image.assert_not_called()

  @mock.patch.object(os, 'makedirs', autospec=True)
  @mock.patch.object(layer_mixer, 'LayerMixer', autospec=True)
  @mock.patch.object(spreadsheet_loader, 'SpreadSheetLoader', autospec=True)
  def test_generate_creatives_an_image_cannot_be_found_raises_error(
      self, mock_spreadsheet_loader, layer_mixer_mock, _):
    mock_spreadsheet_loader.return_value.get_layouts.return_value = [
        _ONE_LAYOUT_TWO_LAYERS
    ]

    # If an image file path cannot be found it raises FileNotFoundError
    # as layer_mixer relies on Image.open()
    layer_mixer_mock.return_value.add_layers.side_effect = FileNotFoundError()

    with self.assertRaises(FileNotFoundError):
      image_mixer = image_mix_main.ImageMixMain(
          spreadsheet_url='http://www.google.com/xyz',
          output_path='~/image_mix_output',
          default_font_file_path='~/font.tff',
          image_directory_path='~/imagemix-images')
      image_mixer.generate_creatives()

  @mock.patch.object(layer_mixer, 'LayerMixer', autospec=True)
  @mock.patch.object(spreadsheet_loader, 'SpreadSheetLoader', autospec=True)
  def test_generate_creatives_text_font_cannot_be_read_raises_value_error(
      self, mock_spreadsheet_loader, layer_mixer_mock):

    mock_spreadsheet_loader.return_value.get_layouts.return_value = [
        _ONE_LAYOUT_TWO_LAYERS
    ]

    # If the layer_mixer cannot open the font file it raises an OSError
    # as it relies on the method ImageFont.truetype()
    layer_mixer_mock.return_value.add_layers.side_effect = OSError()

    with self.assertRaises(OSError):
      image_mixer = image_mix_main.ImageMixMain(
          spreadsheet_url='http://www.google.com/xyz',
          output_path='~/image_mix_output',
          default_font_file_path='~/cannot-be-read-font.tff',
          image_directory_path='~/imagemix-images')
      image_mixer.generate_creatives()

  @mock.patch.object(layer_mixer, 'LayerMixer', autospec=True)
  @mock.patch.object(spreadsheet_loader, 'SpreadSheetLoader', autospec=True)
  def test_generate_creatives_saving_output_raises_os_error(
      self, mock_spreadsheet_loader, layer_mixer_mock):

    mock_spreadsheet_loader.return_value.get_layouts.return_value = [
        _ONE_LAYOUT_TWO_LAYERS
    ]

    # If the layer_mixer cannot save an image it raises an OSError
    # as it relies on the method Image.save()
    layer_mixer_mock.return_value.save_image.side_effect = OSError()

    with self.assertRaises(OSError):
      image_mixer = image_mix_main.ImageMixMain(
          spreadsheet_url='http://www.google.com/xyz',
          output_path='~/image_mix_output',
          default_font_file_path='~/font.tff',
          image_directory_path='~/imagemix-images')
      image_mixer.generate_creatives()

  @mock.patch.object(os, 'makedirs', autospec=True)
  @mock.patch.object(layer_mixer, 'LayerMixer', autospec=True)
  @mock.patch.object(spreadsheet_loader, 'SpreadSheetLoader', autospec=True)
  def test_generate_creatives_two_layouts_generates_two_creatives(
      self, mock_spreadsheet_loader, layer_mixer_mock, _):
    mock_spreadsheet_loader.return_value.get_layouts.return_value = [
        _ONE_LAYOUT_TWO_LAYERS, _ANOTHER_LAYOUT_TWO_LAYERS
    ]

    image_mixer = image_mix_main.ImageMixMain(
        spreadsheet_url='http://www.google.com/xyz',
        output_path='~/image_mix_output',
        default_font_file_path='~/font.tff',
        image_directory_path='~/imagemix-images')
    image_mixer.generate_creatives()

    layer_mixer_mock.return_value.save_image.assert_has_calls(
        [mock.call('~/image_mix_output/template_c_square2.jpg'),
         mock.call('~/image_mix_output/creative_bags.jpg')])


if __name__ == '__main__':
  absltest.main()

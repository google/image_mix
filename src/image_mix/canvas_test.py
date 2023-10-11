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

"""Tests for canvas."""

from image_mix import canvas as canvas_lib
from absl.testing import absltest


CANVAS_ID = 'canvas_id_123'


class CanvasTest(absltest.TestCase):

  def test_canvas_constructor(self):
    canvas = canvas_lib.Canvas(canvas_id=CANVAS_ID, width=1000, height=500)

    self.assertEqual(CANVAS_ID, canvas.canvas_id)
    self.assertEqual(1000, canvas.width)
    self.assertEqual(500, canvas.height)

  def test_canvas_constructor_canvas_id_empty_raises_value_error(self):
    with self.assertRaises(ValueError):
      canvas_lib.Canvas(canvas_id='', width=1000, height=500)


if __name__ == '__main__':
  absltest.main()

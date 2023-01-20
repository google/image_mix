# ImageMix

This is not an officially supported Google product

## What is ImageMix
ImageMix helps you generate image creatives that can be used in your Google
Display Network for example.

## How to run ImageMix
The code of ImageMix is to be run in a Google Colaboratory and the code has
to be imported in your Colab.
ImageMix needs
- A Google Sheet that is used as a template to define the size of your creative,
the images that compose your creative as well as the text of your creative.
- An image folder path in Google Drive that contains the images
to be mixed together to make your creative.
- A path to a font file
- An output Google Drive folder where your creatives will be saved.

You can use the image_mix_notebook.ipynb Colaboratory file to see how to import
and run the code.

## Details about the template Spreadsheet
The template Spreadsheet is defined as follow.
The Spreadsheet contains 4 Sheets.

### The LAYOUT Sheet is made of a few columns in this order:
- "output_filename" is the name of the image file generated once we mix images
and text together.
- "canvas_id" refers to a canvas (the main frame of your image) that is defined
in the "CANVAS" sheet.
- layer_1 ... layer_30 refers to an image or some text defined in the TEXT_LAYER
or the IMAGE_LAYER sheet.
The image is made by having a canvas and adding one by one on the top of each
other layers of images and texts.

### The CANVAS sheet is made of the following columns in order:
- "canvas_id" Is a name given to the canvas that we can refer to in LAYOUT
sheet.
- "width" the width in pixel of your canvas.
- "height" the height in pixel of your canvas.

### The TEXT_LAYER sheet is made of the following columns in order:
- "layer_id" define the name of that layer that can be used in the LAYOUT sheet.
- "font_size" sets the size of the text font to be used.
- "color_r" sets the red color of your text (between 0 and 255).
- "color_g" sets the green color of your text (between 0 and 255).
- "color_b" set the blue color of your text (between 0 and 255).
- "position_x" sets the abscissa of the lower left point of your text.
- "position_y" sets the ordinate of the lower left point of your text.
- "text_content" is the text content of your text layer.

### The IMAGE_LAYER is made of the following columns in order:
- "layer_id" is the name of your image layer that can be referred to in the
LAYOUT sheet.
- "width" defines the width in pixel of your image layer.
- "height" defines the height in pixel of your image layer.
- "position_x" defines the abscissa of the lower left corner if your image
layer.
- "position_y" defines the ordinate of the lower left corner of your image
layer.
- filename is the name of your image file in the Google Drive folder given to
imageMix.

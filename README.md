# Image to ASCII converter

*Work still in progress*

Generate ASCII art from an image.

## Demo

[Original image](https://unsplash.com/photos/W_MUqtuHwyY) by _Dawson Lovell_ taken from [Unsplash](https://unsplash.com)

![Demo image of conversion](images/ascii_demo.png)

part of the image blown up

![Demo image of conversion](images/ascii_demo_2.png)

## Implementation

The image is first converted to its intensity values in a greyscale version. Then ASCII characters corresponding to the intensity are added to the text file. The characters used here are `' .:;+?#%@$'` sorted by increasing brightness. [This article](http://paulbourke.net/dataformats/asciiart/) by *Paul Bourke* is a very good resource for further reference.

## Dependancies

Pillow for importing and writing out images and Numpy for manipulating image data

```
pip install numpy
  
pip install pillow
```

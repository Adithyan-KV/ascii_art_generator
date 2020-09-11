from PIL import Image
import numpy as np
import os
import sys


class Converter():

    def __init__(self, *args, **kwargs):
        path = sys.argv[1]
        if os.path.exists(path):
            self.filepath = path
            self.basename = os.path.basename
        else:
            raise OSError(f"File not found: the file {path} couldn't be found")
        self.generate_ascii_from_image(self.filepath)

    def generate_ascii_from_image(self, filename, *args, **kwargs):
        filename = sys.argv[1]
        image = Image.open(f'{filename}')
        pre_processed_data = self.preprocess(image)
        ascii_data = self.convert_to_ascii(pre_processed_data)
        self.write_to_file(ascii_data, f'{filename}')

    def preprocess(self, image, *args):
        """Preprocesses the image before being processed to convert to ascii. Image
        is resized and converted to greyscale values

        Args:
            image (PIL image): The image to be preprocessed

        Returns:
            nparray: The resized, greyscale image data matrix
        """
        if args:
            print(len(args))
        width, height = image.size
        image = image.resize((width//10, height//20))
        data = np.asarray(image)
        # weights chosen in accordance with
        # https://en.wikipedia.org/wiki/Luma_(video)
        weight_array = np.array([0.3, 0.59, 0.11])
        luma_value_data = np.matmul(data, weight_array)
        return luma_value_data

    def convert_to_ascii(self, image_data):
        """Take an image data matrix and generate the ASCII data to be written out
        to a file

        Args:
            image_data (nparray): Image pixel data to be coverted to ASCII

        Returns:
            nparray: ASCII character data for the image ready to be written out
        """
        # sorted from light to dark (assuming light background)
        # character set selected from http://paulbourke.net/dataformats/asciiart/
        characters_used = [' ', '.', ':', ';', '+', '?', '#', '%', '@', '$']
        height, width = np.shape(image_data)
        ascii_data = np.zeros_like(image_data, dtype=str)
        for i in range(height):
            for j in range(width):
                value = self.normalize(image_data[i, j], 0, 9)
                ascii_data[i, j] = characters_used[value]
        print(ascii_data)
        return ascii_data

    def normalize(self, value, lower_bound, upper_bound):
        """Normalize pixel values between 0-255 to a range between upper and lower 
        bound values, so as to correspond to number of ASCII intensity values used

        Args:
            value (int): The value to be normalized
            lower_bound (int): The lower bound of the range of normalization
            upper_bound (int): The upper bound of the range of normalization

        Returns:
            int: The normalized value between lower and upper bounds
        """
        normalized_value = round(value/255*(upper_bound-lower_bound))
        return normalized_value

    def write_to_file(self, data, filename):
        """Write out the ASCII data to a text file

        Args:
            data (nparray): The ASCII character data to be written to file
        """
        height, width = np.shape(data)
        with open(f'{filename}.txt', 'w') as fopen:
            for i in range(height):
                for j in range(width):
                    fopen.write(data[i, j])
                fopen.write('\n')


if __name__ == "__main__":
    converter = Converter(sys.argv)

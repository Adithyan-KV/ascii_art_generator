from PIL import Image
import numpy as np
import os
import sys


class Converter():

    def __init__(self, args):
        path = args[1]
        dimension_args = args[2:]
        if os.path.exists(path):
            self.filepath = path
            self.basename = os.path.basename
        else:
            raise OSError(f"File not found: the file {path} couldn't be found")

        self.generate_ascii_from_image(self.filepath, dimension_args)

    def generate_ascii_from_image(self, filename, dimension_args):
        image = Image.open(f'{filename}')
        pre_processed_data = self.preprocess(image, dimension_args)
        ascii_data = self.convert_to_ascii(pre_processed_data)
        self.write_to_file(ascii_data, f'{os.path.splitext(filename)[0]}')

    def preprocess(self, image, dimension_args):
        """Preprocesses the image before being processed to convert to ascii. Image
        is resized and converted to greyscale values

        Args:
            image (PIL image): The image to be preprocessed

        Returns:
            nparray: The resized, greyscale image data matrix
        """
        img_width, img_height = image.size
        if dimension_args:
            flag = dimension_args[0]
            print(flag)
            arg_number = len(dimension_args)
            if not flag:
                # defaults to original image size
                flag = '-o'
            if flag == '-h':
                if arg_number != 2:
                    if arg_number < 2:
                        raise ValueError("Missing argument [height] after -h")
                    else:
                        raise ValueError(
                            f"Too many arguments, one argument was expected after -h, but {arg_number} were provided")
                else:
                    try:
                        output_height = int(dimension_args[1])
                        output_width = round(
                            output_height*(img_width/img_height))
                    except Exception:
                        raise TypeError("Height must be a number")
            elif flag == '-w':
                if arg_number != 2:
                    if arg_number < 2:
                        raise ValueError("Missing argument [height] after -h")
                    else:
                        raise ValueError(
                            f"Too many arguments, one argument was expected after -w, but {arg_number} were provided")
                else:
                    try:
                        output_width = int(dimension_args[1])
                        output_height = round(
                            output_width*(img_height/img_width))
                    except Exception:
                        raise TypeError("Height must be a number")
            elif flag == '-o':
                if arg_number != 1:
                    raise ValueError(
                        f"Too many arguments, No arguments expected after -o, but {arg_number} were provided")
                output_width = img_width
                output_height = img_height
            elif flag == '-c':
                if arg_number != 3:
                    if arg_number < 3:
                        raise ValueError(
                            "Missing arguments after -h, two arguments [width],[height] expected")
                    else:
                        raise ValueError(
                            f"Too many arguments, one argument was expected after -w, but {arg_number} were provided")
                else:
                    try:
                        output_width = int(dimension_args[1])
                        output_height = int(dimension_args[2])
                    except Exception:
                        raise TypeError("Height must be a number")
            else:
                raise ValueError(f'invalid flag "{flag}"')
        image = image.resize((output_width, output_height))
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

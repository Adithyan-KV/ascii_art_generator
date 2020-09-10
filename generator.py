from PIL import Image
import numpy as np


def main():
    image = Image.open('image.jpg')
    pre_processed_data = preprocess(image)
    ascii_data = convert_to_ascii(pre_processed_data)
    write_to_file(ascii_data)


def preprocess(image):
    """Preprocesses the image before being processed to convert to ascii. Image
    is resized and converted to greyscale values

    Args:
        image (PIL image): The image to be preprocessed

    Returns:
        nparray: The resized, greyscale image data matrix
    """
    width, height = image.size
    image = image.resize((width//10, height//10))
    data = np.asarray(image)
    # weights chosen in accordance with
    # https://en.wikipedia.org/wiki/Luma_(video)
    weight_array = np.array([0.3, 0.59, 0.11])
    luma_value_data = np.matmul(data, weight_array)
    return luma_value_data


def convert_to_ascii(image_data):
    # sorted from light to dark (assuming light background)
    # character set selected from http://paulbourke.net/dataformats/asciiart/
    characters_used = [' ', '.', ':', ';', '+', '?', '#', '%', '@', '$']
    height, width = np.shape(image_data)
    ascii_data = np.zeros_like(image_data, dtype=str)
    for i in range(height):
        for j in range(width):
            value = normalize(image_data[i, j], 0, 9)
            ascii_data[i, j] = characters_used[value]
    print(ascii_data)
    return ascii_data


def normalize(value, lower_bound, upper_bound):
    normalized_value = round(value/255*(upper_bound-lower_bound))
    return normalized_value


def write_to_file(data):
    height, width = np.shape(data)
    with open('test.txt', 'w') as fopen:
        for i in range(height):
            for j in range(width):
                fopen.write(data[i, j])
            fopen.write('\n')


if __name__ == "__main__":
    main()

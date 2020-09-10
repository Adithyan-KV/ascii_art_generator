from PIL import Image
import numpy as np


def main():
    image = Image.open('image.jpg')
    processed_image = preprocess(image)


def preprocess(image):
    """Preprocesses the image before being processed to convert to ascii. Image
    is resized and converted to greyscale values

    Args:
        image (PIL image): The image to be preprocessed

    Returns:
        PIL image: The resized, greyscale image
    """
    width, height = image.size
    image = image.resize((width//10, height//10))
    data = np.asarray(image)
    # weights chosen in accordance with
    # https://en.wikipedia.org/wiki/Luma_(video)
    weight_array = np.array([0.3, 0.59, 0.11])
    luma_value_data = np.matmul(data, weight_array)
    luma_value_image = Image.fromarray(luma_value_data)
    luma_value_image.show()
    return luma_value_image


if __name__ == "__main__":
    main()

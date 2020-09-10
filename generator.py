from PIL import Image
import numpy as np


def main():
    image = Image.open('image.jpg')
    width, height = image.size
    image = image.resize((width//10, height//10))
    # image.show()
    data = np.asarray(image)
    # weights chosen in accordance with
    # https://en.wikipedia.org/wiki/Luma_(video)
    weight_array = np.array([0.3, 0.59, 0.11])
    print(np.shape(data))
    print(np.shape(weight_array))
    luma_value_data = np.matmul(image, weight_array)
    luma_value_image = Image.fromarray(luma_value_data)
    luma_value_image.show()


if __name__ == "__main__":
    main()

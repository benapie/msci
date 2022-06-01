import cv2
import numpy as np

##############################################################

# These parameter values are indicative. You should choose your own
# according to properties of the method you want to demonstrate

h = 14
templateWindowSize = 7


searchWindowSize = 21

##############################################################

""" Functions """


def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

""" Main code """

original_image = cv2.imread("alley.png")
noisy_image = cv2.imread("alley-highNoise.png")

mse_list = []  # (h, mse)
i = 10
for i in [5, 7, 9, 11, 13, 17, 21]:
    denoised_image = cv2.fastNlMeansDenoisingColored(noisy_image, None, h, h, templateWindowSize, i)
    mse_list.append((i, mse(original_image, denoised_image)))
    print(i)
    i += 1

for i in mse_list:
    print(i)

# cv2.imwrite('alley-denoised.png', dst)



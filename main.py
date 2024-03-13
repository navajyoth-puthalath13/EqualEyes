import cv2 as cv
import numpy as np
from PIL import ImageGrab
from time import time
l_time = time()
while(True):
    screenshot = ImageGrab.grab()
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)
    cv.imshow('cv', screenshot)

    print('fps {}'.format(1 / (time() - l_time)))

    if cv.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cv.destroyAllWindows()
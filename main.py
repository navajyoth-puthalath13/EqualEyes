import cv2 as cv
import numpy as np
from PIL import ImageGrab
from time import time
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

l_time = time()
while(True):
    screenshot = ImageGrab.grab()
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)
    cv.imshow('cv', screenshot)

    # print('fps {}'.format(1 / (time() - l_time)))
    # Path to the image you want to detect objects in
    image_path = screenshot


    # Perform object detection
    results = model(image_path)

    # Access the first detection (assuming you want the first one)
    for result in results:
        probs = result.probs  # Probs object for classification outputs

        if probs is not None:
            # Iterate over each detection
            for i in range(len(probs)):
                class_id = probs[i].argmax()  # Get the class ID with the highest probability
                class_name = model.names[class_id]  # Look up the class name using the class ID
                print(f"Detected object: {class_name}")
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cv.destroyAllWindows()
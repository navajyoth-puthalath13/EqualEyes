import cv2 as cv
import numpy as np
from time import time
import pyttsx3
from ultralytics import YOLO
import win32ui, win32con, win32gui

x = 40  # X-coordinate of the top-left corner of the ROI
y = 164  # Y-coordinate of the top-left corner of the ROI
width = 1180  # Width of the ROI
height = 665  # Height of the ROI

def audio( sv,sd):
    engine = pyttsx3.init(driverName='sapi5')
    engine.say(f"{sd}")

def win_capture( bbox ):
    x, y, x2, y2 = bbox
    w, h = x2 - x, y2 - y

    hwnd = None

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (x, y), win32con.SRCCOPY)

    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    # Convert RGBA to RGB
    img = cv.cvtColor(img, cv.COLOR_RGBA2RGB)

    return img



model = YOLO("yolov8n.pt")

l_time = time()
while True:
    screenshot = win_capture((x, y, x + width, y + height))

    cv.imshow('cv', screenshot)

    print('fps {}'.format(1 / (time() - l_time)))
    l_time = time()

    # Perform object detection
    results = model(screenshot)

    num_objects = 0
    class_names = []

    if results is not None:  # Check if any detections were made
        for detection in results:  # Assuming results is a list of detections
            num_objects += 1

            # Access class ID and convert it to class name using model.names
            class_id = int(detection.boxes.cls[0])  # Assuming class is the first element
            class_name = model.names[class_id]

            class_names.append(class_name)

        print(f"Number of objects detected: {num_objects}")
        print(f"Class names: {class_names}")



    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()

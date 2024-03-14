import cv2 as cv
import numpy as np
from time import time
from ultralytics import YOLO
import win32ui , win32con, win32gui

x = 40  # X-coordinate of the top-left corner of the ROI
y = 164  # Y-coordinate of the top-left corner of the ROI
width = 1180  # Width of the ROI
height = 665  # Height of the ROI



def win_capture(bbox):
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

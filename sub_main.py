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

def audio(text):
    engine = pyttsx3.init(driverName='sapi5')
    engine.say(text)
    engine.runAndWait()

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



def detect_objects(model, screenshot):
    # Function to perform object detection and return the number of objects detected
    # and their corresponding class names

    # Perform object detection
    results = model(screenshot)

    num_objects = 0
    class_names = []

    if results is not None:  # Check if any detections were made
        for detection in results:  # Assuming results is a list of detections
            if len(detection.boxes.cls) > 0:  # Check if class IDs are not empty
                num_objects += 1
                class_id = int(detection.boxes.cls[0])  # Assuming class is the first element
                class_name = model.names[class_id]
                class_names.append(class_name)
            else:
                # Handle case when no class IDs are available
                class_names.append("Unknown")

    return num_objects, class_names

def speak_result(num_objects, class_names):
    # Function to speak out the result in audio format
    # Convert num_objects and class_names into text
    num_objects_text = str(num_objects)
    class_names_text = ", ".join(class_names)

    # Create the text to be spoken
    text_to_speak = f"There are {num_objects_text} {class_names_text}"

    # Speak the text
    audio(text_to_speak)


# Load the YOLO model
model = YOLO("yolov8n.pt")

l_time = time()
while True:
    screenshot = win_capture((x, y, x + width, y + height))

    cv.imshow('cv', screenshot)

    print('fps {}'.format(1 / (time() - l_time)))
    l_time = time()

    num_objects, class_names = detect_objects(model, screenshot)

    print(f"Number of objects detected: {num_objects}")
    print(f"Class names: {class_names}")

    speak_result(num_objects, class_names)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
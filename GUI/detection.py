from PyQt import PyQtApp
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import threading
import cv2
import torch
import pandas as pd

img = None

def opencv_to_image(image) -> QtGui.QImage:
    image = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
    return QtGui.QPixmap.fromImage(image)

def show_frame_in_display(image_path : str, fit_image : bool = True) -> None:
    app.window.label1.setPixmap(QPixmap(image_path))
    app.window.label1.setScaledContents(fit_image)

def show_stream():
    webcam = cv2.VideoCapture(0)
    while webcam.isOpened():
        if app.window.checkbox1.checkState() == 2: #fix issue with checkbox
            ret, img = webcam.read()
            app.window.label1.setPixmap(opencv_to_image(img))
            app.window.label1.setScaledContents(True)

def detect(Img) -> None: #TODO: separate this into a thread
    global img
    img = Img.copy()
    app.window.label1.setText("Detecting...")
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
    result = model(img, size=3072)
    print(result.pandas().xyxy)
    # print(len(result.pandas().xyxy[0]))
    for i in range(len(result.pandas().xyxy[0])):
        xm,ym = int(result.pandas().xyxy[0]["xmin"][i]), int(result.pandas().xyxy[0]["ymin"][i])
        xM, yM = int(result.pandas().xyxy[0]["xmax"][i]), int(result.pandas().xyxy[0]["ymax"][i])
        cv2.putText(img, str(round(result.pandas().xyxy[0]["confidence"][i],3)), (xm, ym), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)
        cv2.rectangle(img, (xm, ym), (xM, yM), (0,0,255), 4)
    show_frame_in_display(opencv_to_image(img))

def loadImage():
    #open file open dialog
    fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open Image", "", "Image Files (*.jpg *.png *.bmp)")
    if fileName:
        img = cv2.imread(fileName)
        img = detect(img)
        #add thread for detection here

def saveImage():
    fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save Image", "", "Image Files (*.jpg *.png *.bmp)")
    if fileName:
        cv2.imwrite(fileName, img)

def snapImage():
    # add this functionality with pi camera
    pass

def main():
    stream = threading.Thread(target=show_stream)
    # stream.daemon = True
    # stream.start()
    app.window.button1.clicked.connect(loadImage)
    app.window.button2.clicked.connect(saveImage)
    app.window.button3.clicked.connect(snapImage)
    app.window.button4.clicked.connect(app.window.close)
    app.execute()

if __name__ == "__main__":
    app = PyQtApp("GUI/layout.ui")
    main()
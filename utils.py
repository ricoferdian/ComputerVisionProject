import cv2
import numpy as np
import matplotlib.pyplot as plt

def returnCameraIndexes():
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr

def convertQImageToMat(incomingImage):
    '''  Converts a QImage into an opencv MAT format  '''

    incomingImage = incomingImage.convertToFormat(13)

    width = incomingImage.width()
    height = incomingImage.height()
    print("QTMAT h",height)
    print("QTMAT w",width)
    print("QTMAT hwc",height*width*3)

    ptr = incomingImage.bits()
    ptr.setsize(incomingImage.byteCount())
    arr = np.array(ptr).reshape(height, width, 3)  #  Copies the data
    return arr

def getB(img, height, width, color):
    temp = [[[0 for i in range(color)] for j in range(width)] for k in range(height)]
    for i in range(height):
        for j in range(width):
            for k in range(color):
                if k is 2:
                    temp[i][j][k] = img[i, j, 2]
                else:
                    temp[i][j][k] = np.uint8(0)
    result = np.array(temp)
    return result


def getG(img, height, width, color):
    temp = [[[0 for i in range(color)] for j in range(width)] for k in range(height)]
    for i in range(height):
        for j in range(width):
            for k in range(color):
                if k is 1:
                    temp[i][j][k] = img[i, j, 1]
                else:
                    temp[i][j][k] = np.uint8(0)
    result = np.array(temp)
    #     plt.imshow(result)
    return result


def getR(img, height, width, color):
    temp = [[[0 for i in range(color)] for j in range(width)] for k in range(height)]
    for i in range(height):
        for j in range(width):
            for k in range(color):
                if k is 0:
                    temp[i][j][k] = img[i, j, 0]
                else:
                    temp[i][j][k] = np.uint8(0)
    result = np.array(temp)
    return result

def plotHisto(x):
    plt.hist(x.ravel(),256,[0,256])
    plt.show()

def getLeftPanelSize(w, h):
    return int(w * 0.4),int(h * 0.8)

def getCenterPanelSize(w, h):
    return int(w * 0.4),int(h * 0.8)

def getRightPanelSize(w, h):
    return int(w * 0.2), int(h * 0.8)
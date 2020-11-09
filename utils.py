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

def rgba2rgb( rgba, background=(255,255,255) ):
    row, col, ch = rgba.shape
    print('row, col, ch',row, col, ch)
    if ch == 3:
        return rgba

    assert ch == 4, 'RGBA image has 4 channels.'

    rgb = np.zeros( (row, col, 3), dtype='float32' )
    r, g, b, a = rgba[:,:,0], rgba[:,:,1], rgba[:,:,2], rgba[:,:,3]

    a = np.asarray( a, dtype='float32' ) / 255.0

    R, G, B = background

    print('r',r)
    print('g',g)
    print('b',b)
    print('alpha',a)
    rgb[:,:,0] = r * a + (1.0 - a) * R
    rgb[:,:,1] = g * a + (1.0 - a) * G
    rgb[:,:,2] = b * a + (1.0 - a) * B
    print('rgb result',rgb)
    return np.asarray(rgb, dtype='uint8')

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
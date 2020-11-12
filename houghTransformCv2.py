import cv2
import numpy as np

def houghTransformLine(img, max_slider, minLineLength=10, maxLineGap=250):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite("hasilbgr.jpg",img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("hasilgray.jpg",gray)
    # Find the edges in the image using canny detector
    gray = cv2.medianBlur(gray, 5)
    cv2.imwrite("hasilblur.jpg",gray)
    edges = cv2.Canny(gray, 50, 200)
    cv2.imwrite("hasilcanny.jpg",edges)
    # Detect points that form a line
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, max_slider, minLineLength=minLineLength, maxLineGap=maxLineGap)
    # Draw lines on the image
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
    # Show result
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return gray

def houghTransformCircle(img, param1=200, param2=10,minRadius=30, maxRadius=40):
    print('p1,p2,min,max',param1,param2,minRadius,maxRadius)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("HASILGRAY.jpg",gray)
    # Blur the image to reduce noise
    img_blur = cv2.medianBlur(gray, 5)
    img_blur = cv2.Canny(img_blur, 50, 200)
    cv2.imwrite("HASILCANNY.jpg",img_blur)
    # Apply hough transform on the image
    circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, img.shape[0] / 64, param1=param1, param2=param2, minRadius=minRadius,
                               maxRadius=maxRadius)
    # Draw detected circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Draw outer circle
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # Draw inner circle
            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
    # Show result
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return gray
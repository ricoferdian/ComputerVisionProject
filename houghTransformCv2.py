import cv2
import numpy as np

def erosiCitra(img):
    # Threshold the image
    ret, img = cv2.threshold(img, 127, 255, 0)

    # Step 1: Create an empty skeleton
    size = np.size(img)
    skel = np.zeros(img.shape, np.uint8)

    # Get a Cross Shaped Kernel
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    # Repeat steps 2-4
    while True:
        # Step 2: Open the image
        open = cv2.morphologyEx(img, cv2.MORPH_OPEN, element)
        # Step 3: Substract open from the original image
        temp = cv2.subtract(img, open)
        # Step 4: Erode the original image and refine the skeleton
        eroded = cv2.erode(img, element)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()
        # Step 5: If there are no white pixels left ie.. the image has been completely eroded, quit the loop
        if cv2.countNonZero(img) == 0:
            break
    return skel

def houghTransformLine(img, max_slider=0, minLineLength=3, maxLineGap=20):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite("hasilbgr.jpg",img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("hasilgray.jpg",gray)
    # Find the edges in the image using canny detector
#     gray = cv2.medianBlur(gray, 5)
#     cv2.imwrite("hasilblur.jpg",gray)
    edges = erosiCitra(gray)
#     edges = cv2.Canny(gray, 50, 200)
#     cv2.imwrite("hasilcanny.jpg",edges)

    # Probabilistic Hough
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, max_slider, minLineLength=minLineLength, maxLineGap=maxLineGap)
    # Draw lines on the image
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 1)
    # Show result
    result = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    return gray, edges, result, lines

def houghTransformCircle(img, param1=200, param2=10,minRadius=20, maxRadius=35):
    print('p1,p2,min,max',param1,param2,minRadius,maxRadius)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite("TAHAP 1.jpg",img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("TAHAP 2.jpg",gray)
    # Blur the image to reduce noise
    img_blur = cv2.medianBlur(gray, 5)
    cv2.imwrite("TAHAP 3.jpg",img_blur)
    img_canny = cv2.Canny(img_blur, 120, 240)
    cv2.imwrite("TAHAP 4.jpg",img_canny)
    # Apply hough transform on the image
    circles = cv2.HoughCircles(img_canny, cv2.HOUGH_GRADIENT, 1, img.shape[0] / 20, param1=param1, param2=param2, minRadius=minRadius,
                               maxRadius=maxRadius)
    cv2.imwrite("TAHAP 5.jpg",circles)
    # Draw detected circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Draw outer circle
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # Draw inner circle
            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
    # Show result
    result = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    img_canny = cv2.cvtColor(img_canny, cv2.COLOR_GRAY2RGB)
    return gray, img_canny, result
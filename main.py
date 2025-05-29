import cv2
import numpy as np
import pyautogui
import time
import matplotlib.pyplot as plt
from config import model, show, image_path

#time.sleep(3)

scale_factor = 1 # Output will be the exact same as the screenshot so keep that in mind!
offset_x = 150
offset_y = 150

image = cv2.imread(image_path, cv2.IMREAD_COLOR)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = cv2.GaussianBlur(image, (5, 5), 1.4)

def sobel(image):
    # Sobel operators
    Gx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    Gy = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

    # Gradient magnitude
    G = np.sqrt(Gx**2 + Gy**2)

    # Normalize to range 0-255
    Gx = np.uint8(255 * np.abs(Gx) / np.max(Gx))
    Gy = np.uint8(255 * np.abs(Gy) / np.max(Gy))
    G = np.uint8(255 * G / np.max(G))
    return G

def canny(image):
    edges = cv2.Canny(image, 100, 200)
    return edges

def postproc(edges):
    # unintentional side effect: lines are actually visible now and no longer dogshit!
    kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    post_edges = cv2.dilate(edges, kernel1, iterations=1)

    kernel2 = np.ones((2, 2), np.uint8)
    final_edge = cv2.morphologyEx(post_edges, cv2.MORPH_CLOSE, kernel2)
    #final_edge = cv2.medianBlur(post_edges, 3.3)
    return final_edge

def display(image):
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 1, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Edge Detection')
    plt.axis('off')
    plt.show()

def draw(edges):
    global scale_factor, offset_x, offset_y

    points = np.column_stack(np.where(edges > 0))

    pyautogui.moveTo(points[0][1] * scale_factor + offset_x, points[0][0] * scale_factor + offset_y)

    pyautogui.PAUSE = 0.02
    start_time = time.time()
    for point in points:
        x, y = point[1], point[0]
        pyautogui.moveTo(x * scale_factor + offset_x, y * scale_factor + offset_y, duration=0.001)
        pyautogui.click()

    end_time = time.time()  # Get the current time again
    elapsed_time = end_time - start_time
    print(f"The process took {elapsed_time:.4f} seconds to complete.")

def main():
    if model == "canny":
        edges = canny(image)
        if show == False:
            draw(edges)
        else:
            edges = postproc(edges)
            display(edges)
    elif model == "sobel":
        edges = sobel(image)
        if show == False:
            draw(edges)
        else:
            edges = postproc(edges)
            display(edges)
    else:
        print("model does not exist, terminating program")
        exit()

main()
    
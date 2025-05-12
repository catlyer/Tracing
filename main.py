import cv2
import numpy as np
import pyautogui
import time
import matplotlib.pyplot as plt

time.sleep(3)

model = "canny"
show = False
image_path = "image.png"
image = cv2.imread(image_path, cv2.IMREAD_COLOR)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 1.4)

def sobel(blurred_image):
    # Sobel operators
    Gx = cv2.Sobel(blurred_image, cv2.CV_64F, 1, 0, ksize=3)
    Gy = cv2.Sobel(blurred_image, cv2.CV_64F, 0, 1, ksize=3)

    # Gradient magnitude
    G = np.sqrt(Gx**2 + Gy**2)

    # Normalize to range 0-255
    Gx = np.uint8(255 * np.abs(Gx) / np.max(Gx))
    Gy = np.uint8(255 * np.abs(Gy) / np.max(Gy))
    G = np.uint8(255 * G / np.max(G))
    return G

def canny(blurred_image):
    edges = cv2.Canny(blurred_image, 100, 200)
    return edges

def display(image):
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 1, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Canny Edge Detection')
    plt.axis('off')
    plt.show()

def draw(edges):
    scale_factor = 1 # Output will be the exact same as the screenshot so keep that in mind!
    offset_x = 720
    offset_y = 280

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

if model == "canny":
    edges = canny(blurred_image)
    if show == False:
        draw(edges)
    else:
        display(edges)
elif model == "sobel":
    edges = sobel(blurred_image)
    if show == False:
        draw(edges)
    else:
        display(edges)
else:
    print("model does not exist, terminating program")
    exit()
    
import pyautogui
import time

time.sleep(3)   
x, y = pyautogui.position()
print(f"Current mouse position: X={x}, Y={y}")
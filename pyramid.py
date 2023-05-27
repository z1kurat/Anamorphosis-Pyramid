import cv2

import sys

import numpy as np

import tkinter as tk
from tkinter import filedialog, messagebox

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(title="Выберите видеофайл",
                                       filetypes=(("Video files", "*.mp4 *.avi *.mkv"), ("all files", "*.*")))

if not file_path:
    sys.exit()

background = messagebox.askyesno("Настройки", "Вырезать задний фон")

cv2.namedWindow('Video Player', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Video Player', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

screen_width = cv2.getWindowImageRect('Video Player')[2]
screen_height = cv2.getWindowImageRect('Video Player')[3]

cap = cv2.VideoCapture(file_path)

alpha = 1

frame_height = int(screen_height // 2.3)
frame_width = int(screen_width // 2.3)

center = (screen_width // 2) - (frame_width // 2)

background_subtractor = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()

    if not ret:
        break

    if background:
        foreground_mask = background_subtractor.apply(frame)
        frame = cv2.bitwise_and(frame, frame, mask=foreground_mask)

    resize_frame = cv2.resize(frame, (frame_width, frame_height))

    flipped_left = cv2.rotate(resize_frame, cv2.ROTATE_90_CLOCKWISE)
    flipped_right = cv2.flip(flipped_left, 1)
    flipped_down = cv2.flip(resize_frame, 0)

    black_frame = np.zeros((screen_height, screen_width, 3), np.uint8)

    black_frame[screen_height - frame_width:screen_height, 0:frame_height] = flipped_left
    black_frame[screen_height - frame_width:screen_height, screen_width - frame_height:screen_width] = flipped_right
    black_frame[0:frame_height, center:center + frame_width] = flipped_down

    cv2.imshow('Video Player', black_frame)

    key = cv2.waitKey(25)
    if key == 27:
        break

cap.release()

cv2.destroyAllWindows()
